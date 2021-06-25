from square import cSquare
from pawn import cPawn
from knight import cKnight
from bishop import cBishop
from rook import cRook
from queen import cQueen
from king import cKing
from square import cSquare
from move import cMove
from displayer import cDisplayer
from constants import *
from icons import *
from lib import *
import re

class cBoard:
    def __init__(self, display):
        self.squares = [cSquare(i, self) for i in range(64)]
        self.turn = WHITE
        self.white_pieces = []
        self.black_pieces = []
        self.white_sliding_pieces = []
        self.black_sliding_pieces = []
        self.castle_white_king = False
        self.castle_black_king = False
        self.castle_white_queen = False
        self.castle_black_queen = False
        self.en_passant = None
        self.half_moves = 0
        self.moves = 0

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
        
        self.castle_white_king = 'K' in castling
        self.castle_white_queen = 'Q' in castling
        self.castle_black_king = 'k' in castling
        self.castle_black_queen = 'q' in castling
        
        self.en_passant = en_passant
        
        self.half_moves = int(halves)
        self.moves = int(fulls)
        
        for piece in self.white_pieces + self.black_pieces:
            piece.calculate_attacking_squares()
        self.legal_moves = self.get_all_moves()

    def clear(self):
        for sqr in self.squares:
            sqr.clear()
            
        self.white_pieces = []
        self.black_pieces = []
        self.white_sliding_pieces = []
        self.black_sliding_pieces = []
        self.history = []
        self.half_moves = 0
        self.moves = 0
        
        self.displayer.clear()
            
    def getSquare(self, col, row=None):
        # getSquare('a1') == getSquare(0) == getSquare(0, 0) == getSquare('a', 1) == getSquare('a', '1')
        # getSquare('h1') == getSquare(7) == getSquare(7, 0) == getSquare('a', 1) == getSquare('a', '1')
        # getSquare('a8') == getSquare(56) == getSquare(0, 7) == getSquare('a', 8) == getSquare('a', '8')
        # getSquare('h8') == getSquare(63) == getSquare(7, 7) == getSquare('h', 8) == getSquare('h', '8')
        if type(col) == int and row is None:
            if col < 0 or col > 63:
                return None
            return self.squares[col]

        if type(col) == int and type(row) == int:
            if col < 0 or col > 7 or row < 0 or row > 7:
                return None
            return self.squares[col*8 + row]
        
        if type(col) == str and row is None:
            row, col = int(col[1]), col[0]

        if col < 'a' or col > 'h' or row < 1 or row > 8:
            return None
        return self.squares[(ord(col) - 97) + (row - 1)*8]
        
        
    def place_piece(self, sqr, kind, color):
        square = self.getSquare(sqr)
        
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
        self.get_pieces(piece.color).remove.(piece)
        if piece.is_sliding:
            self.get_pieces(piece.color, sliding=True).remove.(piece)
            for sqr in piece.attackingSquares:
                sqr.get_attacked_by(piece.color).remove(piece)
    
    def perform_move(self, move):
        fromSqr, toSqr, movPiece = move.fromSqr, move.toSqr, move.piece

        if toSqr.piece is not None or movPiece.kind == PAWN:
            self.half_moves = 0
        else:
            self.half_moves += 1
            
        if self.turn == BLACK:
            self.moves += 1
    
        if toSqr.piece is not None:
            self.remove_piece(toSqr.piece)

        if move.is_en_passant():
            self.remove_piece(self.en_passant.piece, display=True)
            self.en_passant.piece = None

        toSqr.piece, fromSqr.piece, movPiece.square = movPiece, None, toSqr
        movPiece.movesCnt += 1
        
        if movPiece.kind in [KING, ROOK]:
            self._update_casteling_rights(movPiece)
        
        if move.is_castling():
            self._handle_castling(move)
            
        self._update_en_passant_rights(move)
            
        if move.is_promotion():
            _handle_pawn_promotion()

        self.turn = WHITE if self.turn == BLACK else BLACK

        for piece in fromSqr.get_attacked_by().union(toSqr.get_attacked_by()).union({movPiece}):
            if piece.is_sliding or piece == movPiece:
                piece.calculate_attacking_squares()

    def _handle_castling(self, move):
        # the move is casteling, need to move the rook too
        if toSqr.idx == 6:
            rookFrom, rookTo = 7, 5
        elif toSqr.idx == 2:
            rookFrom, rookTo = 0, 3
        elif toSqr.idx == 62:
            rookFrom, rookTo = 63, 61
        else:
            rookFrom, rookTo = 56, 59
        
        self.getSquare(rookTo).piece = self.getSquare(rookFrom).piece
        self.getSquare(rookFrom).piece = None
        self.getSquare(rookTo).piece.square = self.getSquare(rookTo)

    def _handle_pawn_promotion(self, move):
            toSqr = move.toSqr
            old_id, old_move_cnt = toSqr.piece.id, toSqr.piece.movesCnt
            self.remove_piece(toSqr.piece)
            self.place_piece(toSqr.idx, move.newPiece, self.turn)
            move.piece = toSqr.piece
            move.piece.id, move.piece.movesCnt = old_id, old_move_cnts

    def _update_en_passant_rights(self, move):
        if move.piece.kind == PAWN and abs(move.toSqr.rowIdx - move.fromSqr.rowIdx) == 2:
            self.en_passant = move.toSqr
        else:
            self.en_passant = None

    def _update_casteling_rights(self, piece):
        if piece.kind == KING:
            if piece.color == WHITE:
                self.castle_white_king, self.castle_white_queen = False, False
            else:
                self.castle_black_king, self.castle_black_queen = False, False
        if piece.kind == ROOK:
            if piece.color == WHITE:
                if self.getSquare(0).piece is not None and self.getSquare(0).piece.kind != ROOK:
                    self.castle_white_queen = False
                if self.getSquare(7).piece is not None and self.getSquare(7).piece.kind != ROOK:
                    self.castle_white_king = False
            else:
                if self.getSquare(56).piece is not None and self.getSquare(56).piece.kind != ROOK:
                    self.castle_black_queen = False
                if self.getSquare(63).piece is not None and self.getSquare(63).piece.kind != ROOK:
                    self.castle_black_king = False

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
        pinned_pieces = []
        kingSqr = self.get_king_sqr(color)

        for piece in self.get_pieces(not color, sliding=True):
            if piece.kind == ROOK:
                if not isSameColOrRow(piece.square, kingSqr):
                    continue
            elif piece.kind == BISHOP:
                if not isSameDiag(piece.square, kingSqr):
                    continue
            else: #piece.kind == QUEEN
                if not isSameColOrRow(piece.square, kingSqr):
                    continue

            direction = self.get_direction(kingSqr, piece.square)
            firstSquare = self.find_first_piece_in_dir(kingSqr, direction)
            
            if firstSquare is None or firstSquare.piece.color != color:
                continue
            
            secondSquare = self.find_first_piece_in_dir(firstSquare, direction)
            if secondSquare.piece == piece:
                pinned_pieces.append(firstSquare.piece)
                
        return pinned_pieces
           
    def get_all_moves(self):
        color = self.turn
        pieces = self.get_pieces(color)
        pinned_pieces = self.get_pinned_pieces(color)
        
        moves = []
        
        if not self.is_in_check(color):
            for piece in pieces:
                pinned = piece.is_pinned()
                if not pinned:
                    moves += piece.get_potential_moves()
                else:
                    moves += piece.get_potential_moves_pinned(pinned)
                    
            # TODO - write this better
            if self.is_castle_possible(color, RIGHT):
                if color == WHITE:
                    moves.append(cMove(self.get_king_sqr(color).piece, self.getSquare(6)))
                else:
                    moves.append(cMove(self.get_king_sqr(color).piece, self.getSquare(62)))
                    
            if self.is_castle_possible(color, LEFT):
                if color == WHITE:
                    moves.append(cMove(self.get_king_sqr(color).piece, self.getSquare(2)))
                else:
                    moves.append(cMove(self.get_king_sqr(color).piece, self.getSquare(58)))
        
        else:
            # king is in check
            kingSqr = self.get_king_sqr(color)
            attackers = kingSqr.get_attacked_by(not color)
            
            # can always (attempt to) move the king
            moves = kingSqr.piece.get_potential_moves()
            for piece in attackers:
                if piece.is_sliding:
                    # cannot just run from sliding piece in the direction of the attack
                    direction = reverse_dir(self.get_direction(kingSqr, piece.square))
                    row, col = move_in_direction(kingSqr.rowIdx, kingSqr.colIdx, direction)
                    if self.getSquare(row, col) is not None:
                        tmpMove = cMove(kingSqr.piece, self.getSquare(row, col))
                        if tmpMove in moves:
                            moves.remove(tmpMove)
            if len(attackers) == 1:
                attacker = attackers.pop()
                attackers.add(attacker)

                # not double check - can also capture the attacker
                if attacker.is_sliding:
                    # can also block the attacker
                    direction = self.get_direction(kingSqr, attacker.square)
                    target_squares = self.find_first_piece_in_dir(kingSqr, direction, includePath=True)
                else:
                    target_squares = [attacker.square]
                    
                for piece in pieces:
                    if piece.kind != KING:
                        moves += list(filter(lambda x: x.toSqr in target_squares, piece.get_potential_moves()))
        return moves

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
            sqr = self.getSquare(rowIdx, colIdx)
            if sqr is None or not sqr.is_free():
                return path + [sqr] if includePath else sqr
            elif includePath:
                path.append(sqr)
            colIdx, rowIdx = colIdx + colDiff, rowIdx + rowDiff
            
    def get_king_sqr(self, color):
        if color == WHITE:
            return self.white_pieces[0]
        return self.black_pieces[0]

    def is_in_check(self, color):
        kingSqr = self.get_king_sqr(color)
        if not kingSqr:
            return False
        
        return kingSqr.is_attacked_by(not color)
    
    def is_castle_possible(self, color, side):
        if color == WHITE:
            if side == RIGHT:
                if not self.castle_white_king:
                    return False
                kingSqr = self.getSquare(4)
                rookSqr = self.getSquare(7)
                passingSqrs = [self.getSquare(5), self.getSquare(6)]
            else:
                if not self.castle_white_queen:
                    return False
                kingSqr = self.getSquare(4)
                rookSqr = self.getSquare(0)
                passingSqrs = [self.getSquare(2), self.getSquare(3)]
        else:
            if side == RIGHT:
                if not self.castle_black_king:
                    return False
                kingSqr = self.getSquare(60)
                rookSqr = self.getSquare(63)
                passingSqrs = [self.getSquare(61), self.getSquare(62)]
            else:
                if not self.castle_black_queen:
                    return False
                kingSqr = self.getSquare(60)
                rookSqr = self.getSquare(56)
                passingSqrs = [self.getSquare(58), self.getSquare(59)]

        if kingSqr.piece is None or kingSqr.piece.kind != KING or kingSqr.piece.color != color:
            return False

        if rookSqr.piece is None or rookSqr.piece.kind != ROOK or rookSqr.piece.color != color:
            return False

        if self.is_in_check(color):
            return False

        for sqr in passingSqrs:
            if sqr.piece is not None or sqr.is_attacked_by(not color):
                return False

        return True
