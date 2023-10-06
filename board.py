from typing import Optional, Dict, List

from constants import Color, PieceType, Direction
from piece import Piece
from pawn import Pawn
from knight import Knight
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
from square import Square
from move import Move
import re
from utils import letterToPiece, is_same_col_or_row, is_same_diag, reverse_dir, move_in_direction, coord_to_square_idx, get_direction

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

        # a square of a pawn that has just moved two squares and can be captured en passant (if there is a pawn next to it)
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

        # pieces: Dict[Tuple[Optional[PieceType], Optional[Color]], List[Piece]] = {
        #     (PieceType.PAWN, Color.WHITE): self.whitePawns,
        #     (PieceType.PAWN, Color.BLACK): self.blackPawns,
        #     (PieceType.KNIGHT, Color.WHITE): self.whiteKnights,
        #     (PieceType.KNIGHT, Color.BLACK): self.blackKnights,
        #     (PieceType.BISHOP, Color.WHITE): self.whiteBishops,
        #     (PieceType.BISHOP, Color.BLACK): self.blackBishops,
        #     (PieceType.ROOK, Color.WHITE): self.whiteRooks,
        #     (PieceType.ROOK, Color.BLACK): self.blackRooks,
        #     (PieceType.QUEEN, Color.WHITE): self.whiteQueens,
        #     (PieceType.QUEEN, Color.BLACK): self.blackQueens,
        #     (PieceType.KING, Color.WHITE): [self.whiteKing],
        #     (PieceType.KING, Color.BLACK): [self.blackKing],
        #     (None, Color.WHITE): self.whitePawns + self.whiteKnights + self.whiteBishops + self.whiteRooks + self.whiteQueens + [self.whiteKing],
        #     (None, Color.BLACK): self.blackPawns + self.blackKnights + self.blackBishops + self.blackRooks + self.blackQueens + [self.blackKing],
        #     (PieceType.PAWN, None): [],
        #     (PieceType.KNIGHT, None): [],
        #     (PieceType.BISHOP, None): [],
        #     (PieceType.ROOK, None): [],
        #     (PieceType.QUEEN, None): [],
        #     (PieceType.KING, None): [],
        #     (None, None): []
        # }

    # TODO - this is probably quite ineffective, needs to be optimized if it should be used heavily in the engine
    def get_all_pieces(self, color: Optional[Color]=None) -> List[Piece]:
        if color == Color.WHITE:
            return (self.whitePawns + self.whiteKnights + self.whiteBishops + self.whiteRooks + self.whiteQueens +
                    ([self.whiteKing] if self.whiteKing else []))
        elif color == Color.BLACK:
            return (self.blackPawns + self.blackKnights + self.blackBishops + self.blackRooks + self.blackQueens +
                    ([self.blackKing] if self.blackKing else []))
        else:
            return (self.whitePawns + self.whiteKnights + self.whiteBishops + self.whiteRooks + self.whiteQueens +
            ([self.whiteKing] if self.whiteKing else []) +
            self.blackPawns + self.blackKnights + self.blackBishops + self.blackRooks + self.blackQueens +
            ([self.blackKing] if self.blackKing else []))

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
        
        for p in self.get_all_pieces():
            p.update_attacked_squares()

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
        """
        Get a square by its index, e.g. 0 is a1
        :param idx: square index (0-63)
        :return: the Square object
        """
        return self.squares[idx] if 0 <= idx < 64 else None

    def get_square_by_coords(self, col: int, row: int) -> Optional[Square]:
        """
        Get a square by its coordinates, e.g. (0, 0) is a1

        :param col: column coordinate (0-7)
        :param row: row coordinate (0-7)
        :return: the Square object
        """
        return self.squares[col + row*8] if 0 <= col < 8 and 0 <= row < 8 else None

    def get_square_by_name(self, square: str) -> Optional[Square]:
        """
        Get a square by its name, e.g. 'a1'

        :param square: square name
        :return: the Square object
        """
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

        
    def calc_pinned_pieces(self, color: Color) -> Dict[Piece, Direction]:
        """
        get all pinned pieces of the given color, a pinned piece is the only piece that is between the own king and a sliding piece that would
        otherwise attack the king
        :param color: which color
        :return: a dictionary of pinned pieces and the direction of the pin FROM KING TOWARDS PINNER!!!
        """
        king = self.get_king(color)
        if king is None:
            return {}

        pinnedPieces: Dict[Piece, Direction] = {}
        kingSqr = king.square

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
            direction = get_direction(kingSqr, piece.square)
            firstSquare = self.find_first_piece_in_dir(kingSqr, direction)
            if firstSquare is None or firstSquare.piece.color != color:
                continue

            # the second piece must be the potential pinner - then all conditions are met, the first piece is pinned
            secondSquare = self.find_first_piece_in_dir(firstSquare, direction)
            if secondSquare.piece == piece:
                pinnedPieces[firstSquare.piece] = direction
                
        return pinnedPieces

    def get_all_legal_moves(self) -> List[Move]:
        """
        :return: list of legal moves
        """
        return self.get_all_legal_moves_no_check() if not self.is_in_check(self.turn) else self.get_all_legal_moves_check()

    def get_all_legal_moves_no_check(self) -> List[Move]:
        """
        Get all legal moves of the current player provided that the king is not in check
        :return: list of legal king moves
        """
        color = self.turn
        legalMoves: List[Move] = []
        pinnedPieces = self.calc_pinned_pieces(color)

        for piece in self.get_all_pieces(color):
            if piece in pinnedPieces:
                legalMoves += piece.calc_potential_moves_pinned(pinnedPieces[piece])
            else:
                # if piece.has_PT:
                #    legalMoves += list(map(lambda sqr: cMove(piece, sqr), piece.get_potential_squares()))
                # else:
                legalMoves += piece.calc_potential_moves()

        # castling
        king = self.get_king(color)
        if king:
            if self.is_castle_possible(color, Direction.RIGHT):
                legalMoves.append(Move(king, self.get_square_by_idx(6 if color == Color.WHITE else 62)))

            if self.is_castle_possible(color, Direction.LEFT):
                legalMoves.append(Move(king, self.get_square_by_idx(2 if color == Color.WHITE else 58)))
        return legalMoves

    def get_all_legal_moves_check(self) -> List[Move]:
        """
        Get all legal moves of the current player provided that the king is in check
        :return: list of legal moves
        """
        color = self.turn
        pinnedPieces = self.calc_pinned_pieces(color)
        legalMoves = self.get_legal_moves_check_move_king()
        attackers = self.get_king(color).square.get_attacked_by(color.invert())

        if len(attackers) == 1:
            # not double-check - can also capture the attacker or block it if it's a sliding piece
            attacker = attackers.pop()  # there is no convenient way of getting the only element from a set without removing it
            attackers.add(attacker)
            legalMoves += self.get_legal_moves_check_captures(attacker, pinnedPieces)

            # if the attacker is a sliding piece, we might be able to block it
            if attacker.is_sliding():
                legalMoves += self.get_legal_moves_check_blocks(attacker, pinnedPieces)

        return legalMoves

    def get_legal_moves_check_move_king(self) -> List[Move]:
        """
        Get all legal king moves of the current player provided that the king is in check
        :return: list of legal moves
        """
        color = self.turn
        king = self.get_king(color)
        assert king is not None, 'King is in check, but no king found'
        attackers = king.square.get_attacked_by(color.invert())

        # if the king is in check by a sliding piece(s), it cannot move away from that piece, even though that square
        # is technically not currently attacked
        inaccessibleDirs = []
        for piece in attackers:
            if piece.is_sliding():
                inaccessibleDirs.append(get_direction(piece.square, king.square))

        return king.calc_potential_moves(inaccessibleDirs)

    def get_legal_moves_check_captures(self, attacker: Piece, pinnedPieces: Dict[Piece, Direction]) -> List[Move]:
        """
        Get all legal capture moves of the current player provided that the king is in check (captures of the attacker)
        :return: list of legal moves
        """
        color = self.turn
        legalMoves: List[Move] = []

        for piece in attacker.square.get_attacked_by(color):
            # a pinned piece cannot capture the attacker
            if piece in pinnedPieces:
                continue
            if isinstance(piece, Pawn):
                # if the attacker is captured by a pawn, this can result in a promotion (4 different moves)
                legalMoves += piece.generate_pawn_move(attacker.square)
            elif not isinstance(piece, King):
                # king can also capture the attacker, but that's a king move which is already covered
                legalMoves.append(Move(piece, attacker.square))

        # the attacker can also be captured en passant
        if attacker.square == self.enPassantPawnSquare:
            assert isinstance(attacker, Pawn), 'En passant capture by a non-pawn piece'
            for offset in [1, -1]:
                # look to both sides if there is an own pawn that can capture en passant
                potentialPawnSqr = self.get_square_by_coords(attacker.square.colIdx + offset, attacker.square.rowIdx)
                if potentialPawnSqr and isinstance(potentialPawnSqr.piece, Pawn) and potentialPawnSqr.piece.color == color:
                    legalMoves.append(Move(potentialPawnSqr.piece, self.get_square_by_coords(attacker.square.colIdx, attacker.square.rowIdx + (
                        1 if color == Color.WHITE else -1))))

        return legalMoves

    def get_legal_moves_check_blocks(self, attacker: Piece, pinnedPieces: Dict[Piece, Direction]) -> List[Move]:
        """
        Get all legal blocking moves of the current player provided that the king is in check
        :return: list of legal moves
        """
        color = self.turn
        legalMoves: List[Move] = []
        king = self.get_king(color)

        direction = get_direction(king.square, attacker.square)
        # look at all the squares between the king and the attacker - what pieces can access them?
        for blockingSquare in self.get_squares_in_dir(king.square, direction):
            for piece in blockingSquare.get_attacked_by(color):
                # king cannot block, pawn cannot block to a square that it is attacking
                if not isinstance(piece, (Pawn, King)) and piece not in pinnedPieces:
                    legalMoves.append(Move(piece, blockingSquare))

            # look one square in the direction of attackers pawns, if there is a defending pawn, it can block the attack
            # consider potential promotion as well
            potentialPawnSqr = self.get_square_by_coords(blockingSquare.colIdx, blockingSquare.rowIdx + (-1 if color == Color.WHITE else 1))
            if potentialPawnSqr is not None and isinstance(potentialPawnSqr.piece, Pawn) and potentialPawnSqr.piece.color == color:
                legalMoves += potentialPawnSqr.piece.generate_pawn_move(blockingSquare)

            # on row 3 (4 for black) look two squares in the direction of attackers pawns, if there is a defending pawn, it can block the attack
            if (blockingSquare.rowIdx == 3 and color == Color.WHITE) or (blockingSquare.rowIdx == 4 and color == Color.BLACK):
                potentialPawnSqr = self.get_square_by_coords(blockingSquare.colIdx, blockingSquare.rowIdx + (-2 if color == Color.WHITE else 2))
                if potentialPawnSqr is not None and isinstance(potentialPawnSqr.piece, Pawn) and potentialPawnSqr.piece.color == color:
                    legalMoves.append(Move(potentialPawnSqr.piece, blockingSquare))
            # pawn taking en passant can never block

        return legalMoves

    def get_squares_in_dir(self, square: Square, direction: Direction) -> List[Square]:
        """
        Get all empty squares in the given direction from the given square

        :param square: square to start from
        :param direction: direction to look in
        :return: list of squares
        """
        squares: List[Square] = []
        colIdx, rowIdx = move_in_direction(square.colIdx, square.rowIdx, direction)
        while True:
            sqr = self.get_square_by_coords(rowIdx, colIdx)
            if sqr is None or not sqr.is_free():
                return squares
            squares.append(sqr)
            colIdx, rowIdx = move_in_direction(colIdx, rowIdx, direction)

    def find_first_piece_in_dir(self, square: Square, direction) -> Optional[Square]:
        """
        Find the square with first piece in the given direction from the given square

        :param square: square to start from
        :param direction: direction to look in
        :return: the square with the first piece in the given direction, or None if there is no piece in that direction
        """
        colIdx, rowIdx = move_in_direction(square.colIdx, square.rowIdx, direction)
        while True:
            sqr = self.get_square_by_coords(colIdx, rowIdx)
            if sqr is None or not sqr.is_free():
                return sqr
            colIdx, rowIdx = move_in_direction(colIdx, rowIdx, direction)

    def is_in_check(self, color: Color) -> bool:
        """
        Is the king of the given color currently in check? Pre-supposes that the attacked squares of all pieces are up-to-date

        :param color: color of the king
        :return: True if the king is in check, False otherwise
        """
        king = self.get_king(color)
        return king is not None and king.square.is_attacked_by(color.invert())
    
    def is_castle_possible(self, color: Color, side: Direction) -> bool:
        """
        Checks the preconditions for castling:
            1. king and the rook haven't moved
            2. king is not in check
            3. no pieces between the king and the rook
            4. no square between the king and the rook is attacked by the opponent

        :param color: color of the side to castle
        :param side: which side to castle are we checking
        :return: True if castling is possible, False otherwise
        """
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

        if kingSqr.piece is None or not isinstance(kingSqr.piece, King) or kingSqr.piece.color != color or kingSqr.piece.hasMoved:
            return False

        if rookSqr.piece is None or not isinstance(rookSqr.piece, Rook) or rookSqr.piece.color != color or rookSqr.piece.hasMoved:
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

