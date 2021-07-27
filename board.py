from piece import *
from square import cSquare
from pawn import cPawn
from knight import cKnight
from bishop import cBishop
from rook import cRook
from queen import cQueen
from king import cKing
from square import cSquare
from move import cMove
from constants import *
from icons import *
from lib import *
import re

captures = 0
ep = 0
castles = 0
promotions = 0
checks = 0

class cBoard:
    def __init__(self):
        self.squares = [cSquare(idx, self) for idx in range(64)]
        self.turn = WHITE
        self.white_pieces = []
        self.black_pieces = []
        self.white_sliding_pieces = []
        self.black_sliding_pieces = []
        self.en_passant = None
        self.half_moves = 0
        self.moves = 0
        self.analysis_depth = 0
        self.pieces_recalculated = []
        self.legal_moves = []

    def loadFEN(self, fenstr):
        self.clear()
        
        if not re.match(r'^([rnbqkpRNBQKP1-8]*/){7}[rnbqkpRNBQKP1-8]* [wb] (-|[KQkq]{1,4}) (-|[a-h][36]) [0-9]+ [0-9]+$', fenstr):
            raise ValueError('Invalid FEN position given')

        pieces, turn, castling, en_passant, halves, fulls = fenstr.split()

        i, j = 0, 7
        for c in pieces:
            if c.isnumeric():
                i += int(c)
                continue

            if c == '/':
                if i != 8:
                    raise ValueError('Invalid FEN position given')
                i, j = 0, j - 1
                continue

            piece = letter_to_piece(c.lower())

            color = WHITE if c.isupper() else BLACK
            self.place_piece(i + 8*j, piece, color)
            i += 1

        self.turn = WHITE if turn == 'w' else BLACK

        # if cannot castle, mark the respective rook to have moved
        cornerPiece = self.get_square('h1').piece
        if not 'K' in castling and cornerPiece is not None and cornerPiece.color == WHITE and cornerPiece.kind == ROOK:
            cornerPiece.movesCnt = 1

        cornerPiece = self.get_square('a1').piece
        if not 'Q' in castling and cornerPiece is not None and cornerPiece.color == WHITE and cornerPiece.kind == ROOK:
            cornerPiece.movesCnt = 1

        cornerPiece = self.get_square('h8').piece
        if not 'k' in castling and cornerPiece is not None and cornerPiece.color == BLACK and cornerPiece.kind == ROOK:
            cornerPiece.movesCnt = 1

        cornerPiece = self.get_square('a8').piece
        if not 'q' in castling and cornerPiece is not None and cornerPiece.color == BLACK and cornerPiece.kind == ROOK:
            cornerPiece.movesCnt = 1

        if en_passant != '-':
            self.en_passant = self.get_square_by_idx(en_passant.idx)
        
        self.half_moves = int(halves)
        self.moves = int(fulls)
        
        for piece in self.get_pieces():
            piece.update_attacked_squares()

        self.legal_moves.append(list(self.get_all_moves()))

    def clear(self):
        self.squares = [cSquare(idx, self) for idx in range(64)]
        self.white_pieces = []
        self.black_pieces = []
        self.white_sliding_pieces = []
        self.black_sliding_pieces = []
        self.history = []
        self.half_moves = 0
        self.moves = 0

    def get_square_by_idx(self, idx):
        if idx < 0 or idx > 63:
            return None
        return self.squares[idx]

    def get_square_by_coords(self, col, row):
        if col < 0 or col > 7 or row < 0 or row > 7:
            return None
        return self.squares[col*8 + row]

    # not to be used in the engine - is slower than get_square_by_idx or get_square_by_coords
    # get_square('a1') == get_square(0) == get_square(0, 0) == get_square('a', 1) == get_square('a', '1')
    # get_square('h1') == get_square(7) == get_square(7, 0) == get_square('a', 1) == get_square('a', '1')
    # get_square('a8') == get_square(56) == get_square(0, 7) == get_square('a', 8) == get_square('a', '8')
    # get_square('h8') == get_square(63) == get_square(7, 7) == get_square('h', 8) == get_square('h', '8')
    def get_square(self, col, row=None):
        if type(col) == int and row is None:
            if col < 0 or col > 63:
                return None
            return self.squares[col]

        elif type(col) == int and type(row) == int:
            if col < 0 or col > 7 or row < 0 or row > 7:
                return None
            idx = col*8 + row
        
        else:
            if type(col) == str and row is None:
                row, col = int(col[1]), col[0]

            if col < 'a' or col > 'h' or row < 1 or row > 8:
                return None
            idx = (ord(col) - 97) + (row - 1)*8

        return self.squares[idx]
        
    def place_piece(self, sqr, kind, color):
        square = self.get_square_by_idx(sqr)
        
        if kind == PAWN: square.piece = cPawn(color, square)
        elif kind == KNIGHT: square.piece = cKnight(color, square)
        elif kind == BISHOP: square.piece = cBishop(color, square)
        elif kind == ROOK: square.piece = cRook(color, square)
        elif kind == QUEEN: square.piece = cQueen(color, square)
        elif kind == KING: square.piece = cKing(color, square)
        
        square.piece.square = square
        
        if kind == KING:
            self.get_pieces(color).insert(0, square.piece)
        else:
            self.get_pieces(color).append(square.piece)
            if square.piece.is_sliding:
                self.get_pieces(color, sliding=True).append(square.piece)
        
    def remove_piece(self, piece):
        self.get_pieces(piece.color).remove(piece)
        if piece.is_sliding:
            self.get_pieces(piece.color, sliding=True).remove(piece)
        piece.is_active = False
    
    def perform_move(self, move, analysis=True):
        fromSqr, toSqr, movPiece = move.fromSqr, move.toSqr, move.piece

        #if toSqr.piece is not None or movPiece.kind == PAWN:
            #self.half_moves = 0
        #else:
            #self.half_moves += 1
        if self.en_passant:
            move.pastEP = self.en_passant
        if self.turn == BLACK:
            self.moves += 1

        if toSqr.piece is not None:
            move.pieceTaken = toSqr.piece
            self.remove_piece(toSqr.piece)

        if move.isEnPassant:
            move.pieceTaken = self.en_passant.piece
            self.remove_piece(self.en_passant.piece)
            self.en_passant.piece = None

        toSqr.piece, fromSqr.piece, movPiece.square = movPiece, None, toSqr
        movPiece.movesCnt += 1

        if move.is_castling():
            rookFrom, rookTo = self._get_castle_rook_squares(move)
            self.get_square_by_idx(rookTo).piece = self.get_square_by_idx(rookFrom).piece
            self.get_square_by_idx(rookFrom).piece = None
            self.get_square_by_idx(rookTo).piece.square = self.get_square_by_idx(rookTo)

        self._update_en_passant_rights(move)

        if move.isPromotion:
            self.change_piece_kind(movPiece, move.newPiece)

        self.turn = not self.turn

        self.recalculation(move, analysis)
        self.legal_moves.append(self.get_all_moves())

    def recalculation(self, move, analysis):
        recalc_pieces = {move.piece}
        recalc_pieces.update(piece for piece in move.fromSqr.get_attacked_by() if piece.is_sliding)
        recalc_pieces.update(piece for piece in move.toSqr.get_attacked_by() if piece.is_sliding)

        if move.pieceTaken is not None:
            recalc_pieces.add(move.pieceTaken)
        if move.is_castling():
            rookFrom, rookTo = self._get_castle_rook_squares(move)
            recalc_pieces.update(piece for piece in self.get_square_by_idx(rookFrom).get_attacked_by() if piece.is_sliding)
            recalc_pieces.update(piece for piece in self.get_square_by_idx(rookTo).get_attacked_by() if piece.is_sliding)

        if move.isEnPassant:
            recalc_pieces.update(piece for piece in move.pieceTaken.square.get_attacked_by() if piece.is_sliding)

        self.pieces_recalculated.append(recalc_pieces)

        for piece in recalc_pieces:
            if analysis:
                piece.add_new_calculation()
            piece.update_attacked_squares()

    def undo_move(self, move, analysis=True):
        fromSqr, toSqr, movPiece = move.fromSqr, move.toSqr, move.piece

        # TODO - move counters
        if move.pastEP:
            self.en_passant = move.pastEP

        if move.pieceTaken is not None:
            move.pieceTaken.is_active = True
            if move.isEnPassant:
                # restore the taken piece
                self.en_passant.piece = move.pieceTaken
                # remove the piece from toSqr
                move.toSqr.piece = None
                # place piece to fromSqr
                move.piece.square = fromSqr
                fromSqr.piece = move.piece
            else:
                # restore the taken piece to toSqr
                toSqr.piece = move.pieceTaken
                if move.pieceTaken.is_sliding:
                    self.get_pieces(move.pieceTaken.color, sliding=True).append(move.pieceTaken)

            self.get_pieces(move.pieceTaken.color).append(move.pieceTaken)

        else:
            toSqr.piece = None

        fromSqr.piece = movPiece
        movPiece.square = fromSqr
        movPiece.movesCnt -= 1

        if move.isPromotion:
            self.change_piece_kind(movPiece, PAWN)

        if move.is_castling():
            # rookTo and rookFrom are just switched here
            rookTo, rookFrom = self._get_castle_rook_squares(move)
            self.get_square_by_idx(rookTo).piece = self.get_square_by_idx(rookFrom).piece
            self.get_square_by_idx(rookFrom).piece = None
            self.get_square_by_idx(rookTo).piece.square = self.get_square_by_idx(rookTo)

        for piece in self.pieces_recalculated[-1]:
            if analysis:
                piece.remove_last_calculation()
            else:
                piece.update_attacked_squares()
        self.pieces_recalculated.pop()

        self.turn = not self.turn
        self.legal_moves.pop()

    def _get_castle_rook_squares(self, move):
        if move.toSqr.idx == 6:
            return 7, 5
        elif move.toSqr.idx == 2:
            return 0, 3
        elif move.toSqr.idx == 62:
            return 63, 61
        else:
            return 56, 59

    def change_piece_kind(self, piece, newKind):
        # doesn't work for king
        if piece.is_sliding and newKind in [PAWN, KNIGHT]:
            self.get_pieces(piece.color, sliding=True).remove(piece)
        elif not piece.is_sliding and newKind in [BISHOP, ROOK, QUEEN]:
            self.get_pieces(piece.color, sliding=True).append(piece)
        piece.kind = newKind
        piece.__class__ = [cPawn, cKnight, cBishop, cRook, cQueen, cKing][newKind]
        #piece.__init__(piece.color, piece.square)

        if cPieceWithPS in piece.__class__.__bases__:
            piece.has_PT = True
            piece.potential_squares = [[]]
        else:
            piece.has_PT = False

        piece.is_sliding = newKind in [BISHOP, ROOK, QUEEN]
        piece.is_light = newKind in [KNIGHT, BISHOP]

    def _update_en_passant_rights(self, move):
        if move.piece.kind == PAWN and abs(move.toSqr.idx - move.fromSqr.idx) == 16:
            self.en_passant = move.toSqr
        else:
            self.en_passant = None

    def get_direction(self, sqr1, sqr2):
        if sqr1 == sqr2:
            return None

        if sqr1.colIdx == sqr2.colIdx:
            if sqr1.rowIdx < sqr2.rowIdx:
                return UP
            else:
                return DOWN
            
        if sqr1.rowIdx == sqr2.rowIdx:
            if sqr1.colIdx < sqr2.colIdx:
                return RIGHT
            else:
                return LEFT
            
        if sqr1.colIdx - sqr2.colIdx == sqr1.rowIdx - sqr2.rowIdx:
            if sqr1.colIdx > sqr2.colIdx:
                return DOWN_LEFT
            else:
                return UP_RIGHT
            
        if sqr1.colIdx - sqr2.colIdx == sqr2.rowIdx - sqr1.rowIdx:
            if sqr1.colIdx > sqr2.colIdx:
                return UP_LEFT
            else:
                return DOWN_RIGHT

        return None
        
    def get_pinned_pieces(self, color):
        pinned_pieces = {}
        kingSqr = self.get_king_sqr(color)

        for piece in self.get_pieces(not color, sliding=True):
            if piece.kind == ROOK:
                if not isSameColOrRow(piece.square, kingSqr):
                    continue
            elif piece.kind == BISHOP:
                if not isSameDiag(piece.square, kingSqr):
                    continue
            else: #piece.kind == QUEEN
                if not isSameColOrRow(piece.square, kingSqr) and not isSameDiag(piece.square, kingSqr):
                    continue

            direction = self.get_direction(kingSqr, piece.square)
            firstSquare = self.find_first_piece_in_dir(kingSqr, direction)
            
            if firstSquare is None or firstSquare.piece.color != color:
                continue
            
            secondSquare = self.find_first_piece_in_dir(firstSquare, direction)
            if secondSquare.piece == piece:
                pinned_pieces[firstSquare.piece] = direction
                
        return pinned_pieces

    def get_all_moves(self):
        color = self.turn
        pieces = self.get_pieces(color)
        pinned_pieces = self.get_pinned_pieces(color)
        all_moves = []
        
        if not self.is_in_check(color):
            for piece in pieces:
                if piece in pinned_pieces:
                    all_moves += piece.calc_potential_moves_pinned(pinned_pieces[piece])
                else:
                    if piece.has_PT:
                        all_moves += list(map(lambda sqr: cMove(piece, sqr), piece.get_potential_squares()))
                    else:
                        all_moves += piece.calc_potential_moves()

                    
            # TODO - write this better
            if self.is_castle_possible(color, RIGHT):
                all_moves.append(cMove(self.get_king_sqr(color).piece, self.get_square_by_idx(6 if color == WHITE else 62)))
                    
            if self.is_castle_possible(color, LEFT):
                all_moves.append(cMove(self.get_king_sqr(color).piece, self.get_square_by_idx(2 if color == WHITE else 58)))
        
        else:
            # king is in check
            kingSqr = self.get_king_sqr(color)
            attackers = kingSqr.get_attacked_by(not color)
            
            # can always (attempt to) move the king
            kingMoves = kingSqr.piece.calc_potential_moves()
            invalidSquares = []
            for piece in attackers:
                if piece.is_sliding:
                    # cannot just run from sliding piece in the direction of the attack
                    direction = reverse_dir(self.get_direction(kingSqr, piece.square))
                    row, col = move_in_direction(kingSqr.rowIdx, kingSqr.colIdx, direction)
                    invalidSqr = self.get_square_by_coords(row, col)
                    if invalidSqr is not None:
                        invalidSquares.append(invalidSqr)

            for mv in kingMoves:
                if mv.toSqr not in invalidSquares:
                    all_moves.append(mv)

            if len(attackers) == 1:
                #attacker = attackers.pop()
                #attackers.add(attacker)
                attacker = attackers[0]

                # not double check - can also capture the attacker
                if attacker.is_sliding:
                    # can also block the attacker
                    direction = self.get_direction(kingSqr, attacker.square)
                    target_squares = self.find_first_piece_in_dir(kingSqr, direction, includePath=True)
                else:
                    target_squares = [attacker.square]

                for piece in pieces:
                    if piece.kind != KING and piece not in pinned_pieces:
                        for mv in piece.calc_potential_moves():
                            if mv.toSqr in target_squares:
                                all_moves.append(mv)

                    if self.en_passant is not None and attacker.square == self.en_passant and piece.kind == PAWN and piece.square.rowIdx == self.en_passant.rowIdx and abs(piece.square.idx - self.en_passant.idx) == 1 and (piece not in pinned_pieces or pinned_pieces[piece] not in [UP, DOWN]):
                        all_moves.append(cMove(piece, self.get_square_by_coords(self.en_passant.rowIdx + (1 if piece.color == WHITE else -1), self.en_passant.colIdx), isEnPassant=True))
        return all_moves

    def get_pieces(self, color=None, sliding=False):
        if color == WHITE:
            if sliding:
                return self.white_sliding_pieces
            else:
                return self.white_pieces
        elif color == BLACK:
            if sliding:
                return self.black_sliding_pieces
            else:
                return self.black_pieces
        else:
            if sliding:
                return self.white_sliding_pieces + self.black_sliding_pieces
            else:
                return self.white_pieces + self.black_pieces

    def find_first_piece_in_dir(self, square, direction, includePath=False):
        offsets = [(0, 0), (0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]
        colDiff, rowDiff = offsets[direction]
        
        colIdx, rowIdx = square.colIdx + colDiff, square.rowIdx + rowDiff
        path = []

        while True:
            sqr = self.get_square_by_coords(rowIdx, colIdx)
            if sqr is None or not sqr.is_free():
                return path + [sqr] if includePath else sqr
            elif includePath:
                path.append(sqr)
            colIdx, rowIdx = colIdx + colDiff, rowIdx + rowDiff
            
    def get_king_sqr(self, color):
        if color == WHITE:
            return self.white_pieces[0].square
        return self.black_pieces[0].square

    def is_in_check(self, color):
        kingSqr = self.get_king_sqr(color)
        if not kingSqr:
            return False
        
        return kingSqr.is_attacked_by(not color)
    
    def is_castle_possible(self, color, side):
        if color == WHITE:
            kingSqr = self.get_square_by_idx(4)
            if side == RIGHT:
                rookSqr = self.get_square_by_idx(7)
                passingSqrs = [self.get_square_by_idx(5), self.get_square_by_idx(6)]
            else:
                rookSqr = self.get_square_by_idx(0)
                passingSqrs = [self.get_square_by_idx(2), self.get_square_by_idx(3)]
                rookPassSqr = self.get_square_by_idx(1)
        else:
            kingSqr = self.get_square_by_idx(60)
            if side == RIGHT:
                rookSqr = self.get_square_by_idx(63)
                passingSqrs = [self.get_square_by_idx(61), self.get_square_by_idx(62)]
            else:
                rookSqr = self.get_square_by_idx(56)
                passingSqrs = [self.get_square_by_idx(58), self.get_square_by_idx(59)]
                rookPassSqr = self.get_square_by_idx(57)

        if kingSqr.piece is None or kingSqr.piece.kind != KING or kingSqr.piece.color != color or kingSqr.piece.movesCnt > 0:
            return False

        if rookSqr.piece is None or rookSqr.piece.kind != ROOK or rookSqr.piece.color != color or rookSqr.piece.movesCnt > 0:
            return False

        if self.is_in_check(color):
            return False

        if side == LEFT and rookPassSqr.piece is not None:
            return False

        for sqr in passingSqrs:
            if sqr.piece is not None or sqr.is_attacked_by(not color):
                return False

        return True

    def generate_successors(self, depth):
        if depth == 0:
            return 1

        total = 0
        for move in self.legal_moves[-1]:
            self.analysis_depth += 1
            self.perform_move(move)
            total += self.generate_successors(depth - 1)
            self.analysis_depth -= 1
            self.undo_move(move)

        return total

