from typing import Optional, Dict, List

from constants import Color, PieceType, Direction
from piece import Piece, SlidingPiece
from pawn import Pawn
from knight import Knight
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
from square import Square
from move import Move
import re
from utils import letterToPiece, is_same_col_or_row, is_same_diag, reverse_dir, move_in_direction, coord_to_square_idx

# TODO - refactor

captures = 0
ep = 0
castles = 0
promotions = 0
checks = 0

class Board:
    def __init__(self):
        self.squares: List[Square] = [Square(idx, self) for idx in range(64)]
        self.turn: Color = Color.WHITE

        # a square of a pawn that has just moved two squares and can be captured en passant (of there is a pawn next to it)
        # careful - FEN uses the square behind the pawn, but this is the square of the pawn itself
        self.enPassantPawnSquare: Optional[Square] = None
        self.halfMoves: int = 0
        self.moves: int = 0
        self.analysisDepth: int = 0
        self.piecesRecalculated: List[Piece] = []
        self.legalMoves: List[Move] = []
        self.history: List[Move] = []

        self.whiteKing: Optional[King] = None
        self.blackKing: Optional[King] = None
        self.whiteQueens: List[Queen] = []
        self.blackQueens: List[Queen] = []
        self.whiteRooks: List[Rook] = []
        self.blackRooks: List[Rook] = []
        self.whiteBishops: List[Bishop] = []
        self.blackBishops: List[Bishop] = []
        self.whiteKnights: List[Knight] = []
        self.blackKnights: List[Knight] = []
        self.whitePawns: List[Pawn] = []
        self.blackPawns: List[Pawn] = []

    def load_FEN(self, fen: str) -> None:
        """
        load a position from a FEN string
        :param fen: string in a FEN format
        """
        self.clear()
        
        if not re.match(r'^([rnbqkpRNBQKP1-8]*/){7}[rnbqkpRNBQKP1-8]* [wb] (-|[KQkq]{1,4}) (-|[a-h][36]) [0-9]+ [0-9]+$', fen):
            # doesn't catch all invalid FENs, but it's a good sanity check
            raise ValueError('Invalid FEN position given')

        pieces, turn, castling, enPassantSqr, halves, fulls = fen.split()

        col, row = 0, 7 # for some reason, FEN starts with a8
        for c in pieces:
            if c.isnumeric():  # number of empty squares to skip
                col += int(c)
                continue

            if c == '/': # new row
                assert col == 8, 'Invalid FEN position given'
                col, row = 0, row - 1
                continue

            # place a new piece
            piece: PieceType = letterToPiece[c.lower()]
            color: Color = Color.WHITE if c.isupper() else Color.BLACK
            self.place_piece(col + 8*row, piece, color)

            col += 1

        self.turn = Color.WHITE if turn == 'w' else Color.BLACK

        # if cannot castle, mark the respective rook to have moved
        cornerPiece = self.get_square_by_name('h1').piece
        if not 'K' in castling and cornerPiece is not None and cornerPiece.color == Color.WHITE and cornerPiece.kind == PieceType.ROOK:
            cornerPiece.hasMoved = True

        cornerPiece = self.get_square_by_name('a1').piece
        if not 'Q' in castling and cornerPiece is not None and cornerPiece.color == Color.WHITE and cornerPiece.kind == PieceType.ROOK:
            cornerPiece.hasMoved = True

        cornerPiece = self.get_square_by_name('h8').piece
        if not 'k' in castling and cornerPiece is not None and cornerPiece.color == Color.BLACK and cornerPiece.kind == PieceType.ROOK:
            cornerPiece.hasMoved = True

        cornerPiece = self.get_square_by_name('a8').piece
        if not 'q' in castling and cornerPiece is not None and cornerPiece.color == Color.BLACK and cornerPiece.kind == PieceType.ROOK:
            cornerPiece.hasMoved = True

        if enPassantSqr != '-':
            # we need the square of the pawn, not the square behind it
            self.enPassantPawnSquare = self.get_square_by_idx(coord_to_square_idx(enPassantSqr) + (8 if self.turn == Color.WHITE else -8))
        
        self.halfMoves = int(halves)
        self.moves = int(fulls)
        
        #for piece in self.get_pieces():
        #    piece.update_attacked_squares()

        #self.legalMoves.append(list(self.get_all_legal_moves()))

    def clear(self):
        self.squares = [Square(idx, self) for idx in range(64)]
        self.whiteKing = None
        self.blackKing = None
        self.whiteQueens.clear()
        self.blackQueens.clear()
        self.whiteRooks.clear()
        self.blackRooks.clear()
        self.whiteBishops.clear()
        self.blackBishops.clear()
        self.whiteKnights.clear()
        self.blackKnights.clear()
        self.whitePawns.clear()
        self.blackPawns.clear()
        self.enPassantPawnSquare = None
        self.history.clear()
        self.halfMoves = 0
        self.moves = 0

    def get_pieces(self, kind: PieceType, color: Color) -> List[Piece]:
        if kind == PieceType.PAWN:
            return self.whitePawns if color == Color.WHITE else self.blackPawns
        elif kind == PieceType.KNIGHT:
            return self.whiteKnights if color == Color.WHITE else self.blackKnights
        elif kind == PieceType.BISHOP:
            return self.whiteBishops if color == Color.WHITE else self.blackBishops
        elif kind == PieceType.ROOK:
            return self.whiteRooks if color == Color.WHITE else self.blackRooks
        elif kind == PieceType.QUEEN:
            return self.whiteQueens if color == Color.WHITE else self.blackQueens

    def get_sliding_pieces(self, color: Color) -> List[Piece]:
        return self.whiteBishops + self.whiteRooks + self.whiteQueens if color == Color.WHITE else (self.blackBishops + self.blackRooks +
                                                                                                    self.blackQueens)

    def get_king(self, color: Color) -> Optional[King]:
        return self.whiteKing if color == Color.WHITE else self.blackKing

    def get_square_by_idx(self, idx: int) -> Optional[Square]:
        return self.squares[idx] if 0 <= idx < 64 else None

    def get_square_by_coords(self, col: int, row: int) -> Optional[Square]:
        return self.squares[col + row*8] if 0 <= col < 8 and 0 <= row < 8 else None

    def get_square_by_name(self, square: str) -> Optional[Square]:
        assert len(square) == 2, f'Invalid square given {square}'

        col, row = square
        assert 'a' <= col <= 'h' and '1' <=  row <= '8', f'Invalid square given {square}'

        idx = (ord(col) - 97) + (int(row) - 1)*8
        return self.squares[idx]

    def place_piece(self, sqr: int | str, kind: PieceType, color: Color) -> Piece:
        if isinstance(sqr, str):
            square = self.get_square_by_name(sqr)
        else:
            square = self.get_square_by_idx(sqr)

        if kind == PieceType.PAWN: square.piece = Pawn(color, square)
        elif kind == PieceType.KNIGHT: square.piece = Knight(color, square)
        elif kind == PieceType.BISHOP: square.piece = Bishop(color, square)
        elif kind == PieceType.ROOK: square.piece = Rook(color, square)
        elif kind == PieceType.QUEEN: square.piece = Queen(color, square)
        elif kind == PieceType.KING: square.piece = King(color, square)
        else: assert False, f'Invalid piece kind {kind}'

        square.piece.square = square

        if kind == PieceType.KING:
            #self.get_pieces(color).insert(0, square.piece)
            if color == Color.WHITE:
                self.whiteKing = square.piece
            else:
                self.blackKing = square.piece
        else:
            self.get_pieces(kind, color).append(square.piece)
            #self.get_pieces(color).append(square.piece)
            #if square.piece.is_sliding():
            #    self.get_pieces(color, sliding=True).append(square.piece)

        return square.piece

    def remove_piece(self, piece):
        self.get_pieces(piece.color).remove(piece)
        if piece.is_sliding:
            self.get_pieces(piece.color, sliding=True).remove(piece)
        piece.is_active = False

    def perform_move(self, move, analysis=True):
        # TODO - rook and king has moved indicators
        fromSqr, toSqr, movPiece = move.fromSqr, move.toSqr, move.piece

        #if toSqr.piece is not None or movPiece.kind == PAWN:
            #self.half_moves = 0
        #else:
            #self.half_moves += 1
        if self.enPassantPawnSquare:
            move.pastEP = self.enPassantPawnSquare
        if self.turn == Color.BLACK:
            self.moves += 1

        if toSqr.piece is not None:
            move.pieceTaken = toSqr.piece
            self.remove_piece(toSqr.piece)

        if move.isEnPassant:
            move.pieceTaken = self.enPassantPawnSquare.piece
            self.remove_piece(self.enPassantPawnSquare.piece)
            self.enPassantPawnSquare.piece = None

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
        self.legalMoves.append(self.get_all_legal_moves())

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

        self.piecesRecalculated.append(recalc_pieces)

        for piece in recalc_pieces:
            if analysis:
                piece.add_new_calculation()
            piece.update_attacked_squares()

    def undo_move(self, move, analysis=True):
        # TODO - rook and king has moved indicators
        fromSqr, toSqr, movPiece = move.fromSqr, move.toSqr, move.piece

        # TODO - move counters
        if move.pastEP:
            self.enPassantPawnSquare = move.pastEP

        if move.pieceTaken is not None:
            move.pieceTaken.is_active = True
            if move.isEnPassant:
                # restore the taken piece
                self.enPassantPawnSquare.piece = move.pieceTaken
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
            self.change_piece_kind(movPiece, PieceType.PAWN)

        if move.is_castling():
            # rookTo and rookFrom are just switched here
            rookTo, rookFrom = self._get_castle_rook_squares(move)
            self.get_square_by_idx(rookTo).piece = self.get_square_by_idx(rookFrom).piece
            self.get_square_by_idx(rookFrom).piece = None
            self.get_square_by_idx(rookTo).piece.square = self.get_square_by_idx(rookTo)

        for piece in self.piecesRecalculated[-1]:
            if analysis:
                piece.remove_last_calculation()
            else:
                piece.update_attacked_squares()
        self.piecesRecalculated.pop()

        self.turn = not self.turn
        self.legalMoves.pop()

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
        if piece.is_sliding and newKind in [PieceType.PAWN, PieceType.KNIGHT]:
            self.get_pieces(piece.color, sliding=True).remove(piece)
        elif not piece.isSliding and newKind in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]:
            self.get_pieces(piece.color, sliding=True).append(piece)
        piece.kind = newKind
        piece.__class__ = [Pawn, Knight, Bishop, Rook, Queen, King][newKind]
        #piece.__init__(piece.color, piece.square)

# TODO - FIX THIS !!!
#        if PieceWithPotenialSquares in piece.__class__.__bases__:
#            piece.has_PT = True
#            piece.potential_squares = [[]]
#        else:
#            piece.has_PT = False

        piece.is_sliding = newKind in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]
        piece.is_light = newKind in [PieceType.KNIGHT, PieceType.BISHOP]

    def _update_en_passant_rights(self, move):
        if move.piece.kind == PieceType.PAWN and abs(move.toSqr.idx - move.fromSqr.idx) == 16:
            self.enPassantPawnSquare = move.toSqr
        else:
            self.enPassantPawnSquare = None

    def get_direction(self, sqr1, sqr2):
        if sqr1 == sqr2:
            return None

        if sqr1.colIdx == sqr2.colIdx:
            if sqr1.rowIdx < sqr2.rowIdx:
                return Direction.UP
            else:
                return Direction.DOWN
            
        if sqr1.rowIdx == sqr2.rowIdx:
            if sqr1.colIdx < sqr2.colIdx:
                return Direction.RIGHT
            else:
                return Direction.LEFT
            
        if sqr1.colIdx - sqr2.colIdx == sqr1.rowIdx - sqr2.rowIdx:
            if sqr1.colIdx > sqr2.colIdx:
                return Direction.DOWN_LEFT
            else:
                return Direction.UP_RIGHT
            
        if sqr1.colIdx - sqr2.colIdx == sqr2.rowIdx - sqr1.rowIdx:
            if sqr1.colIdx > sqr2.colIdx:
                return Direction.UP_LEFT
            else:
                return Direction.DOWN_RIGHT

        return None
        
    def get_pinned_pieces(self, color: Color) -> Dict[Piece, Direction]:
        """
        get all pinned pieces of the given color, a pinned piece is the only piece that is between the own king and a sliding piece that would
        otherwise attack the king
        :param color: which color
        :return: a dictionary of pinned pieces and the direction of the pin FROM KING TOWARDS PINNER!!!
        """
        pinnedPieces: Dict[Piece, Direction] = {}
        kingSqr = self.get_king_sqr(color)

        # look at all opponent's sliding pieces (rooks, bishops, queens)
        for piece in self.get_sliding_pieces(color.invert()):
            # if the piece is not on the same row, column (rook, queen) or diagonal (bishop, queen) as the king, it cannot pin
            if piece.kind == PieceType.ROOK:
                if not is_same_col_or_row(piece.square, kingSqr):
                    continue
            elif piece.kind == PieceType.BISHOP:
                if not is_same_diag(piece.square, kingSqr):
                    continue
            else: #piece.kind == QUEEN
                if not is_same_col_or_row(piece.square, kingSqr) and not is_same_diag(piece.square, kingSqr):
                    continue

            # go from own king towards the potential pinner, the first piece must be a piece of the same color
            direction = self.get_direction(kingSqr, piece.square)
            firstSquare = self.find_first_piece_in_dir(kingSqr, direction)
            if firstSquare is None or firstSquare.piece.color != color:
                continue

            # the second piece must be the potential pinner - then all conditions are met, the first piece is pinned
            secondSquare = self.find_first_piece_in_dir(firstSquare, direction)
            if secondSquare.piece == piece:
                pinnedPieces[firstSquare.piece] = direction
                
        return pinnedPieces

    def get_all_legal_moves(self) -> List[Move]:
        color = self.turn
        pieces: List[Piece] = self.get_pieces(color)
        pinnedPieces: Dict[Piece, Direction] = self.get_pinned_pieces(color)
        legalMoves: List[Move] = []
        
        if not self.is_in_check(color):
            for piece in pieces:
                if piece in pinnedPieces:
                    legalMoves += piece.calc_potential_moves_pinned(pinnedPieces[piece])
                else:
                    #if piece.has_PT:
                    #    legalMoves += list(map(lambda sqr: cMove(piece, sqr), piece.get_potential_squares()))
                    #else:
                    legalMoves += piece.calc_potential_moves()

                    
            # TODO - write this better
            if self.is_castle_possible(color, Direction.RIGHT):
                legalMoves.append(Move(self.get_king_sqr(color).piece, self.get_square_by_idx(6 if color == Color.WHITE else 62)))
                    
            if self.is_castle_possible(color, Direction.LEFT):
                legalMoves.append(Move(self.get_king_sqr(color).piece, self.get_square_by_idx(2 if color == Color.WHITE else 58)))
        
        else:
            # king is in check
            kingSqr = self.get_king_sqr(color)
            attackers = kingSqr.get_attacked_by(color.invert())
            
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
                    legalMoves.append(mv)

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
                    if piece.kind != PieceType.KING and piece not in pinnedPieces:
                        for mv in piece.calc_potential_moves():
                            if mv.toSqr in target_squares:
                                legalMoves.append(mv)

                    if self.enPassantPawnSquare is not None and attacker.square == self.enPassantPawnSquare and piece.kind == PieceType.PAWN and piece.square.rowIdx == self.enPassantPawnSquare.rowIdx and abs(piece.square.idx - self.enPassantPawnSquare.idx) == 1 and (piece not in pinnedPieces or pinnedPieces[piece] not in [Direction.UP, Direction.DOWN]):
                        legalMoves.append(Move(piece, self.get_square_by_coords(self.enPassantPawnSquare.rowIdx + (1 if piece.color == Color.WHITE else -1), self.enPassantPawnSquare.colIdx), isEnPassant=True))
        return legalMoves

    def find_path_in_dir(self, square: Square, direction: Direction) -> List[Square]:
        # TODO - should include the piece itself???
        path: List[Square] = []
        while True:
            colIdx, rowIdx = move_in_direction(square.colIdx, square.rowIdx, direction)
            sqr = self.get_square_by_coords(rowIdx, colIdx)
            if sqr is not None:
                path.append(sqr)
            if sqr is None or not sqr.is_free():
                return path

    def find_first_piece_in_dir(self, square: Square, direction) -> Optional[Square]:
        colIdx, rowIdx = move_in_direction(square.colIdx, square.rowIdx, direction)
        while True:
            sqr = self.get_square_by_coords(colIdx, rowIdx)
            if sqr is None or not sqr.is_free():
                return sqr
            colIdx, rowIdx = move_in_direction(colIdx, rowIdx, direction)

    def is_in_check(self, color: Color) -> bool:
        king = self.get_king(color)
        return king is not None and king.square.is_attacked_by(color.invert())
    
    def is_castle_possible(self, color: Color, side: Direction) -> bool:
        assert side == Direction.LEFT or side == Direction.RIGHT, f"castling must be to the LEFT or RIGHT, not {side}"
        rookPassSqr: Optional[Square] = None

        if color == Color.WHITE:
            kingSqr = self.get_square_by_idx(4)
            if side == Direction.RIGHT:
                rookSqr = self.get_square_by_idx(7)
                passingSqrs = [self.get_square_by_idx(5), self.get_square_by_idx(6)]
            else:
                rookSqr = self.get_square_by_idx(0)
                passingSqrs = [self.get_square_by_idx(2), self.get_square_by_idx(3)]
                rookPassSqr = self.get_square_by_idx(1)
        else:
            kingSqr = self.get_square_by_idx(60)
            if side == Direction.RIGHT:
                rookSqr = self.get_square_by_idx(63)
                passingSqrs = [self.get_square_by_idx(61), self.get_square_by_idx(62)]
            else:
                rookSqr = self.get_square_by_idx(56)
                passingSqrs = [self.get_square_by_idx(58), self.get_square_by_idx(59)]
                rookPassSqr = self.get_square_by_idx(57)

        assert isinstance(kingSqr.piece, King), f"error in castle handling"
        if kingSqr.piece is None or kingSqr.piece.kind != PieceType.KING or kingSqr.piece.color != color or kingSqr.piece.hasMoved:
            return False

        assert isinstance(rookSqr.piece, Rook), f"error in castle handling"
        if rookSqr.piece is None or rookSqr.piece.kind != PieceType.ROOK or rookSqr.piece.color != color or rookSqr.piece.hasMoved:
            return False

        if self.is_in_check(color):
            return False

        if side == Direction.LEFT and rookPassSqr is not None and rookPassSqr.piece is not None:
            return False

        for sqr in passingSqrs:
            if sqr.piece is not None or sqr.is_attacked_by(color.invert()):
                return False

        return True

    def generate_successors(self, depth):
        if depth == 0:
            return 1

        total = 0
        for move in self.legalMoves[-1]:
            self.analysisDepth += 1
            self.perform_move(move)
            total += self.generate_successors(depth - 1)
            self.analysisDepth -= 1
            self.undo_move(move)

        return total

