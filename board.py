from typing import Optional, Dict, List, Tuple
from itertools import chain

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

captures = 0
ep = 0
castles = 0
promotions = 0
checks = 0

class Board:
    def __init__(self):
        self.squares: List[Square] = [Square(idx, self) for idx in range(64)]
        self.turn: Color = Color.WHITE

        # a list of squares of a pawn that has just moved two squares and can be captured en passant (if there is a pawn next to it)
        # the list stores the history of en passant options for the purpose of undoing moves
        # careful - FEN uses the square behind the pawn, but this is the square of the pawn itself
        #
        self.enPassantPawnSquare: List[Optional[Square]] = [None]

        # half moves since last capture or pawn move for each position in history
        # when undoing a pawn or a capture move, we wouldn't know what this number should be, the move would have to store it
        # now we simply remove the last number
        self.halfMoves: List[int] = [0]

        self.moves: int = 1 # move counter starts at 1 according to FEN
        self.analysisDepth: int = 0
        self.piecesRecalculated: List[Piece] = []

        # list of legal moves in every position in history, useful because when we are undoing a move, we just pop the last element
        self.legalMoves: List[List[Move]] = []
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

    def get_current_legal_moves(self) -> List[Move]:
        """Get the current list of legal moves"""
        assert len(self.legalMoves) > 0, 'No legal moves found'
        return self.legalMoves[-1]

    def get_all_pieces(self, color: Optional[Color]=None) -> chain[Piece]:
        """Get a list of all pieces of a given color, if no color is given, return all pieces"""
        if color == Color.WHITE:
            return chain(self.whitePawns, self.whiteKnights, self.whiteBishops, self.whiteRooks, self.whiteQueens,
                         [self.whiteKing] if self.whiteKing else [])
        elif color == Color.BLACK:
            return chain(self.blackPawns, self.blackKnights, self.blackBishops, self.blackRooks, self.blackQueens,
                         [self.blackKing] if self.blackKing else [])
        else:
            return chain(self.whitePawns, self.whiteKnights, self.whiteBishops, self.whiteRooks, self.whiteQueens,
                         [self.whiteKing] if self.whiteKing else [],
                         self.blackPawns, self.blackKnights, self.blackBishops, self.blackRooks, self.blackQueens,
                         [self.blackKing] if self.blackKing else [])

    def load_FEN(self, fen: str) -> None:
        """load a position from a FEN string"""
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
            cornerPiece.movesCnt = 1

        cornerPiece = self.get_square_by_name('a1').piece
        if not 'Q' in castling and cornerPiece is not None and cornerPiece.color == Color.WHITE and cornerPiece.kind == PieceType.ROOK:
            cornerPiece.movesCnt = 1

        cornerPiece = self.get_square_by_name('h8').piece
        if not 'k' in castling and cornerPiece is not None and cornerPiece.color == Color.BLACK and cornerPiece.kind == PieceType.ROOK:
            cornerPiece.movesCnt = 1

        cornerPiece = self.get_square_by_name('a8').piece
        if not 'q' in castling and cornerPiece is not None and cornerPiece.color == Color.BLACK and cornerPiece.kind == PieceType.ROOK:
            cornerPiece.movesCnt = 1

        if enPassantSqr != '-':
            # we need the square of the pawn, not the square behind it
            self.enPassantPawnSquare[-1] = self.get_square_by_idx_opt(coord_to_square_idx(enPassantSqr) + (8 if self.turn == Color.BLACK else -8))
        
        self.halfMoves = [int(halves)]
        self.moves = int(fulls)
        
        for p in self.get_all_pieces():
            p.update_attacked_squares()

        self.legalMoves = [self.get_all_legal_moves()]

    def clear(self):
        """clear the board"""
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
        self.enPassantPawnSquare = [None]
        self.history.clear()
        self.halfMoves = [0]
        self.moves = 0

    def add_piece_to_list(self, piece: Piece) -> None:
        """Add a piece to the correct list of pieces of the given kind and color (not for kings)"""
        if piece.color == Color.WHITE:
            if isinstance(piece, Pawn): self.whitePawns.append(piece)
            elif isinstance(piece, Knight): self.whiteKnights.append(piece)
            elif isinstance(piece, Bishop): self.whiteBishops.append(piece)
            elif isinstance(piece, Rook): self.whiteRooks.append(piece)
            elif isinstance(piece, Queen): self.whiteQueens.append(piece)
            else: assert False, f'There is no list of type {type(piece)}'
        else:
            if isinstance(piece, Pawn): self.blackPawns.append(piece)
            elif isinstance(piece, Knight): self.blackKnights.append(piece)
            elif isinstance(piece, Bishop): self.blackBishops.append(piece)
            elif isinstance(piece, Rook): self.blackRooks.append(piece)
            elif isinstance(piece, Queen): self.blackQueens.append(piece)
            else: assert False, f'There is no list of type {type(piece)}'

    def remove_piece_from_list(self, piece: Piece) -> None:
        """Remove a piece from the correct list of pieces of the given kind and color (not for kings)"""
        if piece.color == Color.WHITE:
            if isinstance(piece, Pawn): self.whitePawns.remove(piece)
            elif isinstance(piece, Knight): self.whiteKnights.remove(piece)
            elif isinstance(piece, Bishop): self.whiteBishops.remove(piece)
            elif isinstance(piece, Rook): self.whiteRooks.remove(piece)
            elif isinstance(piece, Queen): self.whiteQueens.remove(piece)
            else: assert False, f'There is no list of type {type(piece)}'
        else:
            if isinstance(piece, Pawn): self.blackPawns.remove(piece)
            elif isinstance(piece, Knight): self.blackKnights.remove(piece)
            elif isinstance(piece, Bishop): self.blackBishops.remove(piece)
            elif isinstance(piece, Rook): self.blackRooks.remove(piece)
            elif isinstance(piece, Queen): self.blackQueens.remove(piece)
            else: assert False, f'There is no list of type {type(piece)}'

    #TODO - to be removed
    def get_pieces(self, kind: PieceType, color: Color) -> List[Piece]:
        """Get a list of pieces of a given kind and color, cannot be used for a king"""

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
        assert False, f'Invalid piece kind {kind}'

    def get_sliding_pieces(self, color: Color) -> chain[Piece]:
        """Get a list of sliding pieces of a given color"""
        return chain(self.whiteBishops, self.whiteRooks, self.whiteQueens) if color == Color.WHITE else chain(self.blackBishops,
                                                                                                              self.blackRooks, self.blackQueens)

    def get_king(self, color: Color) -> Optional[King]:
        """Get the king of a given color"""
        return self.whiteKing if color == Color.WHITE else self.blackKing

    def get_square_by_idx_opt(self, idx: int) -> Optional[Square]:
        """Get a square by its index, e.g. 0 is a1"""
        return self.squares[idx] if 0 <= idx < 64 else None

    def get_square_by_idx(self, idx: int) -> Square:
        """Analogous to get_square_by_idx_opt, but assumes the index is valid"""
        assert 0 <= idx < 64, f'Invalid square index {idx}'
        return self.squares[idx]

    def get_square_by_coords_opt(self, col: int, row: int) -> Optional[Square]:
        """Get a square by its coordinates, e.g. (0, 0) is a1"""
        return self.squares[col + row*8] if 0 <= col < 8 and 0 <= row < 8 else None

    def get_square_by_coords(self, col: int, row: int) -> Square:
        """Analogous to get_square_by_coords_opt, but assumes the coordinates are valid"""
        assert 0 <= col < 8 and 0 <= row < 8, f'Invalid square coordinates ({col}, {row})'
        return self.squares[col + row*8]

    def get_square_by_name(self, square: str) -> Square:
        """Get a square by its name, e.g. 'a1'"""

        assert len(square) == 2, f'Invalid square given {square}'
        col, row = square
        assert 'a' <= col <= 'h' and '1' <=  row <= '8', f'Invalid square given {square}'

        idx = (ord(col) - 97) + (int(row) - 1)*8
        return self.squares[idx]

    def place_piece(self, sqr: int | str | Square, kind: PieceType, color: Color) -> Piece:
        """
        Create a piece of a given kind and color and place it on a given square - not performance critical, not used in the engine
        returns pointer to the created piece
        """
        if isinstance(sqr, str):
            square = self.get_square_by_name(sqr)
        elif isinstance(sqr, Square):
            square = sqr
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
            assert isinstance(square.piece, King)
            if color == Color.WHITE:
                self.whiteKing = square.piece
            else:
                self.blackKing = square.piece
        else:
            self.add_piece_to_list(square.piece)

        return square.piece

    def remove_piece(self, piece: Piece) -> None:
        """
        removes a piece from the board, usually during a piece capture
        the removed piece is no longer pointed to by any square or the list of pieces of the board,
        it is however pointed to by the move that it was taken in, thus the move can be undone
        """
        assert piece in self.get_pieces(piece.kind, piece.color), f'Cannot remove piece {piece}, not found'
        for sqr in piece.attackedSquares:
            sqr.get_attacked_by(piece.color).remove(piece)
        piece.attackedSquares.clear()
        self.remove_piece_from_list(piece)
        piece.isActive = False

    def perform_move(self, move: Move, analysis: bool=True) -> None:
        """performs a move on the board"""

        fromSqr, toSqr, movingPiece = move.fromSqr, move.toSqr, move.piece

        if self.turn == Color.BLACK:
            self.moves += 1   # move counter - incremented with black's move

        if toSqr.piece is not None:  # if taking a piece, store the ref in the move and remove it...
            move.pieceTaken = toSqr.piece
            self.remove_piece(toSqr.piece)

        if move.isEnPassant:         # ... and the same for taking en passant
            assert len(self.enPassantPawnSquare) > 0 and self.enPassantPawnSquare[-1] is not None
            assert self.enPassantPawnSquare[-1].piece is not None
            move.pieceTaken = self.enPassantPawnSquare[-1].piece
            self.remove_piece(self.enPassantPawnSquare[-1].piece)
            move.pieceTaken.square.piece = None

        if move.pieceTaken or movingPiece.kind == PieceType.PAWN:  # half-moves counter since the last pawn move or capture
            self.halfMoves.append(0)
        else:
            assert len(self.halfMoves) > 0
            self.halfMoves.append(self.halfMoves[-1] + 1)

        toSqr.piece, fromSqr.piece, movingPiece.square = movingPiece, None, toSqr   # update pointers
        movingPiece.movesCnt += 1  # each piece has its own move counter, might not be needed

        if move.is_castling():
            rookFrom, rookTo = self._get_castle_rook_squares(move)
            rook = self.get_square_by_idx(rookFrom).piece
            assert rook is not None

            self.get_square_by_idx(rookTo).piece = rook
            self.get_square_by_idx(rookFrom).piece = None
            rook.square = self.get_square_by_idx(rookTo)

        self._update_en_passant_rights(move)  # if a pawn was moved 2 squares forward, maybe it can be taken e.p.

        if move.is_promotion():
            assert move.newPiece is not None, f'Invalid promotion move {move}'
            self.change_piece_kind(movingPiece, move.newPiece)

        self.turn = self.turn.invert()

        self.recalculation(move, analysis)   # TODO - redo this
        self.legalMoves.append(self.get_all_legal_moves())

    def recalculation(self, move: Move, analysis: bool) -> None:
        """
        recalculates which squares are attacked by which pieces after a move
        not all pieces must be recalculated, only those that are affected by the move
            1. the moving piece
            2. the piece being taken
            3. the pieces that were previously blocked by the moving piece
            4. the pieces that are now blocked by the moving piece
            5. if the move is castling, the rook and the pieces now blocked by the rook (before the rook couldn't block anyone, it was in the corner)
            6. if the move is en passant, the pieces previously blocked by the captured pawn
        :param move: the move being made
        :param analysis: is this an actual move or just a move for analysis?
        """
        piecesToRecalc = {move.piece} | {piece for piece in move.fromSqr.get_attacked_by() if piece.is_sliding()} | {piece for piece in move.toSqr.get_attacked_by() if piece.is_sliding()}

        if move.pieceTaken is not None and move.pieceTaken.isActive:
            piecesToRecalc.add(move.pieceTaken)
        if move.is_castling():
            _, rookTo = self._get_castle_rook_squares(move)
            piecesToRecalc.update(piece for piece in self.get_square_by_idx(rookTo).get_attacked_by() if piece.is_sliding())

        if move.isEnPassant:
            assert move.pieceTaken is not None, f'Invalid en passant move {move}'
            piecesToRecalc.update(piece for piece in move.pieceTaken.square.get_attacked_by() if piece.is_sliding)

        #self.piecesRecalculated.append(piecesToRecalc)

        for piece in piecesToRecalc:
            #if analysis:
            #    piece.add_new_calculation()
            piece.update_attacked_squares()

    def undo_move(self, move, analysis=True):
        """
        undoes a move on the board
        :param move: the move being undone
        :param analysis: is this an actual move or just a move for analysis?
        """
        fromSqr, toSqr, movingPiece = move.fromSqr, move.toSqr, move.piece

        if move.pieceTaken is not None:
            if move.isEnPassant:
                # restore the piece taken en passant
                # it's column is the same as the takers destination square, it's row as the taker's starting square
                self.enPassantPawnSquare[-1] = self.get_square_by_coords_opt(toSqr.colIdx, fromSqr.rowIdx)
                self.enPassantPawnSquare[-1].piece = move.pieceTaken

                # remove the piece from toSqr
                toSqr.piece = None

                # place piece to fromSqr
                movingPiece.square = fromSqr
                fromSqr.piece = movingPiece
            else:
                # standard capture - just restore the taken piece to toSqr
                toSqr.piece = move.pieceTaken

            move.pieceTaken.isActive = True
            #self.get_pieces(move.pieceTaken.kind, movingPiece.color.invert()).append(move.pieceTaken)
            self.add_piece_to_list(move.pieceTaken)

        else:
            toSqr.piece = None

        fromSqr.piece, movingPiece.square = movingPiece, fromSqr   # restore the moving piece to fromSqr
        movingPiece.movesCnt -= 1

        if move.is_promotion():            # undo promotion, also moves the piece to the right list
            self.change_piece_kind(movingPiece, PieceType.PAWN)

        if move.is_castling():   # undo the rook move
            rookTo, rookFrom = self._get_castle_rook_squares(move)   # rookTo and rookFrom are just switched here
            self.get_square_by_idx_opt(rookTo).piece = self.get_square_by_idx_opt(rookFrom).piece
            self.get_square_by_idx_opt(rookFrom).piece = None
            self.get_square_by_idx_opt(rookTo).piece.square = self.get_square_by_idx_opt(rookTo)

        if movingPiece.color == Color.BLACK:   # update move counter only when black moves
            self.moves -= 1
        self.halfMoves.pop()          # we remember the previous position's half moves counter

        self.enPassantPawnSquare.pop()

        #for piece in self.piecesRecalculated[-1]:
        #    if analysis:
        #        piece.remove_last_calculation()
        #    else:
        #        piece.update_attacked_squares()
        #self.piecesRecalculated.pop()

        self.recalculation(move, analysis)  # TODO - redo this to remember calculations of previous positions

        self.turn = self.turn.invert()
        self.legalMoves.pop()       # we remember the previous position's legal moves

    def _get_castle_rook_squares(self, move: Move) -> Tuple[int, int]:
        """get the from and to squares of the rook that is castling"""
        assert move.toSqr.idx in [6, 2, 62, 58], f'Invalid castling move {move}'
        if move.toSqr.idx == 6:
            return 7, 5
        elif move.toSqr.idx == 2:
            return 0, 3
        elif move.toSqr.idx == 62:
            return 63, 61
        else:
            return 56, 59

    def change_piece_kind(self, piece: Piece, newKind: PieceType) -> None:
        """
        changes a piece to a different kind of piece, it is meant for pawn promotion, but there may be other funny uses
        does not currently work with king
        """

        self.remove_piece_from_list(piece)

        piece.kind = newKind
        piece.__class__ = [Pawn, Knight, Bishop, Rook, Queen][newKind.value] # type: ignore
        piece.__init__(piece.color, piece.square) # type: ignore

        self.add_piece_to_list(piece)

        # if PieceWithPotenialSquares in piece.__class__.__bases__:
        #     piece.has_PT = True
        #     piece.potential_squares = [[]]
        # else:
        #     piece.has_PT = False

    def _update_en_passant_rights(self, move: Move) -> None:
        """If the current move is a 2 square pawn move, remember that it can be taken e.p."""
        self.enPassantPawnSquare.append(move.toSqr if move.piece.kind == PieceType.PAWN and abs(move.toSqr.idx - move.fromSqr.idx) == 16 else None)
        
    def calc_pinned_pieces(self, color: Color) -> Dict[Piece, Direction]:
        """
        get all pinned pieces of the given color, a pinned piece is the only piece that is between the own king and a sliding piece that would
        otherwise attack the king, the direction is the direction from the king towards the pinner!!!
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
            firstSquare = self.find_first_occupied_square_in_dir(kingSqr, direction)

            if firstSquare is None:
                continue

            assert firstSquare.piece is not None
            if firstSquare.piece.color != color:
                continue

            # the second piece must be the potential pinner - then all conditions are met, the first piece is pinned
            secondSquare = self.find_first_occupied_square_in_dir(firstSquare, direction)

            assert secondSquare is not None and secondSquare.piece is not None
            if secondSquare.piece == piece:
                pinnedPieces[firstSquare.piece] = direction
                
        return pinnedPieces

    def get_all_legal_moves(self) -> List[Move]:
        """
        :return: list of legal moves
        """
        return self._get_all_legal_moves_no_check() if not self.is_in_check(self.turn) else self._get_all_legal_moves_check()

    def _get_all_legal_moves_no_check(self) -> List[Move]:
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

    def _get_all_legal_moves_check(self) -> List[Move]:
        """
        Get all legal moves of the current player provided that the king is in check
        :return: list of legal moves
        """
        color = self.turn
        pinnedPieces = self.calc_pinned_pieces(color)
        legalMoves = self._get_legal_moves_check_move_king()

        king = self.get_king(color)
        assert king is not None, 'King is in check, but no king found'

        attackers = king.square.get_attacked_by(color.invert())

        if len(attackers) == 1:
            # not double-check - can also capture the attacker or block it if it's a sliding piece
            attacker = attackers.pop()  # there is no convenient way of getting the only element from a set without removing it
            attackers.add(attacker)
            legalMoves += self._get_legal_moves_check_captures(attacker, pinnedPieces)

            # if the attacker is a sliding piece, we might be able to block it
            if attacker.is_sliding():
                legalMoves += self._get_legal_moves_check_blocks(attacker, pinnedPieces)

        return legalMoves

    def _get_legal_moves_check_move_king(self) -> List[Move]:
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

    def _get_legal_moves_check_captures(self, attacker: Piece, pinnedPieces: Dict[Piece, Direction]) -> List[Move]:
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
        if self.enPassantPawnSquare[-1] and attacker.square == self.enPassantPawnSquare[-1]:
            assert isinstance(attacker, Pawn), 'En passant capture by a non-pawn piece'
            for offset in [1, -1]:
                # look to both sides if there is an own pawn that can capture en passant
                potentialPawnSqr = self.get_square_by_coords_opt(attacker.square.colIdx + offset, attacker.square.rowIdx)
                if potentialPawnSqr and isinstance(potentialPawnSqr.piece, Pawn) and potentialPawnSqr.piece.color == color:
                    legalMoves.append(Move(potentialPawnSqr.piece, self.get_square_by_coords(attacker.square.colIdx, attacker.square.rowIdx + (
                        1 if color == Color.WHITE else -1))))

        return legalMoves

    def _get_legal_moves_check_blocks(self, attacker: Piece, pinnedPieces: Dict[Piece, Direction]) -> List[Move]:
        """
        Get all legal blocking moves of the current player provided that the king is in check
        :return: list of legal moves
        """
        color = self.turn
        legalMoves: List[Move] = []
        king = self.get_king(color)
        assert king is not None, 'King is in check, but no king found'

        direction = get_direction(king.square, attacker.square)
        # look at all the squares between the king and the attacker - what pieces can access them?
        for blockingSquare in self.get_squares_in_dir(king.square, direction):
            for piece in blockingSquare.get_attacked_by(color):
                # king cannot block, pawn cannot block to a square that it is attacking
                if not isinstance(piece, (Pawn, King)) and piece not in pinnedPieces:
                    legalMoves.append(Move(piece, blockingSquare))

            # look one square in the direction of attackers pawns, if there is a defending pawn, it can block the attack
            # consider potential promotion as well
            potentialPawnSqr = self.get_square_by_coords_opt(blockingSquare.colIdx, blockingSquare.rowIdx + (-1 if color == Color.WHITE else 1))
            if potentialPawnSqr is not None and isinstance(potentialPawnSqr.piece, Pawn) and potentialPawnSqr.piece.color == color:
                legalMoves += potentialPawnSqr.piece.generate_pawn_move(blockingSquare)

            # on row 3 (4 for black) look two squares in the direction of attackers pawns, if there is a defending pawn, it can block the attack
            if potentialPawnSqr is not None and potentialPawnSqr.piece is None and (blockingSquare.rowIdx == 3 and color == Color.WHITE) or (blockingSquare.rowIdx == 4 and color == Color.BLACK):
                potentialPawnSqr = self.get_square_by_coords_opt(blockingSquare.colIdx, blockingSquare.rowIdx + (-2 if color == Color.WHITE else 2))
                if potentialPawnSqr is not None and isinstance(potentialPawnSqr.piece, Pawn) and potentialPawnSqr.piece.color == color:
                    legalMoves.append(Move(potentialPawnSqr.piece, blockingSquare))
            # pawn taking en passant can never block

        return legalMoves

    def get_squares_in_dir(self, square: Square, direction: Direction) -> List[Square]:
        """Get all empty squares in the given direction from the given square"""
        squares: List[Square] = []
        colIdx, rowIdx = move_in_direction(square.colIdx, square.rowIdx, direction)
        while True:
            sqr = self.get_square_by_coords_opt(colIdx, rowIdx)
            if sqr is None or not sqr.is_free():
                return squares
            squares.append(sqr)
            colIdx, rowIdx = move_in_direction(colIdx, rowIdx, direction)

    def find_first_occupied_square_in_dir(self, square: Square, direction: Direction) -> Optional[Square]:
        """Find the square with first piece in the given direction from the given square"""

        colIdx, rowIdx = move_in_direction(square.colIdx, square.rowIdx, direction)
        while True:
            sqr = self.get_square_by_coords_opt(colIdx, rowIdx)
            if sqr is None or not sqr.is_free():
                return sqr
            colIdx, rowIdx = move_in_direction(colIdx, rowIdx, direction)

    def is_in_check(self, color: Color) -> bool:
        """Is the king of the given color currently in check? Pre-supposes that the attacked squares of all pieces are up-to-date"""
        king = self.get_king(color)
        return king is not None and king.square.is_attacked_by(color.invert())
    
    def is_castle_possible(self, color: Color, side: Direction) -> bool:
        """
        Checks the preconditions for castling:
            1. king and the rook haven't moved
            2. king is not in check
            3. no pieces between the king and the rook
            4. no square between the king and the rook is attacked by the opponent
        """
        assert side == Direction.LEFT or side == Direction.RIGHT, f"castling must be to the LEFT or RIGHT, not {side}"
        rookPassSqr: Optional[Square] = None

        # based on color and side, get the king and the rook squares, also the king passing squares and the rook passing square
        # the king passing squares need to be empty and not attacked by the opponent
        # the rook passing square needs (just b1 or b8) to be empty
        if color == Color.WHITE:
            kingSqr = self.get_square_by_idx(4) # e1
            if side == Direction.RIGHT:
                rookSqr = self.get_square_by_idx(7) # h1
                passingSqrs = [self.get_square_by_idx(5), self.get_square_by_idx(6)]  # f1, g1
            else:
                rookSqr = self.get_square_by_idx(0) # a1
                passingSqrs = [self.get_square_by_idx(2), self.get_square_by_idx(3)] # c1, d1
                rookPassSqr = self.get_square_by_idx(1) # b1
        else:
            kingSqr = self.get_square_by_idx(60) # e8
            if side == Direction.RIGHT:
                rookSqr = self.get_square_by_idx(63) # h8
                passingSqrs = [self.get_square_by_idx(61), self.get_square_by_idx(62)] # f8, g8
            else:
                rookSqr = self.get_square_by_idx(56) # a8
                passingSqrs = [self.get_square_by_idx(58), self.get_square_by_idx(59)] # c8, d8
                rookPassSqr = self.get_square_by_idx(57) # b8

        # the king must be on its place and not moved
        if kingSqr.piece is None or not isinstance(kingSqr.piece, King) or kingSqr.piece.color != color or kingSqr.piece.movesCnt > 0:
            return False
        # the rook must be on its place and not moved
        if rookSqr.piece is None or not isinstance(rookSqr.piece, Rook) or rookSqr.piece.color != color or rookSqr.piece.movesCnt > 0:
            return False
        # the king cannot be in check
        if self.is_in_check(color):
            return False
        # if castling queenside, the rook passing square must be empty
        if side == Direction.LEFT and rookPassSqr is not None and rookPassSqr.piece is not None:
            return False
        # the king passing squares must be empty and not attacked by the opponent
        for sqr in passingSqrs:
            if sqr.piece is not None or sqr.is_attacked_by(color.invert()):
                return False

        return True

    def generate_successors(self, depth: int) -> int:
        if depth == 0:
            return 1

        total = 0
        for move in self.legalMoves[-1]:
            self.analysisDepth += 1
            #if depth == 2:
            #    print(f'{">>>"*self.analysisDepth} MOVE: {move}    ', end='')
            self.perform_move(move)
            n = self.generate_successors(depth - 1)
            total += n
            #if depth == 2:
            #    print('cnt: ', n)

            self.analysisDepth -= 1
            self.undo_move(move)


        return total

