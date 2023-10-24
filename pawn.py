from typing import List, Set
from constants import PieceType, Color, Direction
from move import Move
from piece import Piece
from square import Square

class Pawn (Piece):
    def __init__(self, color: Color, square: Square):
        super().__init__(PieceType.PAWN, color, square)
        self.isLight = False

        # TODO - these numbers are the same for all pawns of the same player, they should be moved somewhere
        if self.color == Color.WHITE:
            self.MOVE_OFFSET = 1  # white pawns move up the board (+1 row), black opposite
            self.BASE_ROW = 1  # white pawns start on row 1, black on row 6
            self.PROMOTION_ROW = 7  # white pawns promote on row 7, black on row 0
            self.EN_PASSANT_ROW = 4  # white pawns can take en passant on row 4, black on row 3
        else:
            self.MOVE_OFFSET = -1
            self.BASE_ROW = 6
            self.PROMOTION_ROW = 0
            self.EN_PASSANT_ROW = 3

    def calc_potential_moves(self) -> List[Move]:
        """
        potential moves of a piece are not necessarily legal moves, checks and pins are not considered
        the potential moves consists of possible (1) moves forward, (2) captures left, (3) captures right and (4) en passant
        """
        return self.get_forward_moves() + self.get_capture_moves(1) + self.get_capture_moves(-1) + self.get_en_passant_moves()

    def get_en_passant_moves(self) -> List[Move]:
        """check the possibility of taking en passant"""

        potentialMoves: List[Move] = []
        enPassantSqr = self.square.board.enPassantPawnSquare[-1] # if en passant is possible, the enPassantSqr is the square behind the pawn

        # if en passant is possible and the pawn to take is next to this pawn, add the en passant move
        if (enPassantSqr is not None and self.square.rowIdx == self.EN_PASSANT_ROW and abs(self.square.idx - enPassantSqr.idx) == 1 and
                # en passant pin is a bit problematic, because the pawn is not technically pinned so this case cannot be handled in
                # "calc_potential_moves_pinned" and there is no suitable place to handle it
                # the en passant move should technically be among potential moves even if the pawn is pinned in this way, but if it's not,
                # it shouldn't break anything
                not self.is_en_passant_pin(enPassantSqr)):

            toSqr = self.square.board.get_square_by_coords(enPassantSqr.colIdx, enPassantSqr.rowIdx + self.MOVE_OFFSET)
            return [Move(self, toSqr, isEnPassant=True)]

        return []

    def get_forward_moves(self) -> List[Move]:
        """check the possibility of moving one step forward or two steps forward if on the base row"""

        potentialMoves: List[Move] = []
        # check the square in front of the pawn
        square = self.square.board.get_square_by_coords(self.square.colIdx, self.square.rowIdx + self.MOVE_OFFSET)
        if square.piece is None:
            potentialMoves += self.generate_pawn_move(square) # might be a promotion - that would be 4 possible moves

            # if on the base row, check one square further
            if self.square.rowIdx == self.BASE_ROW:
                square = self.square.board.get_square_by_coords(self.square.colIdx, self.square.rowIdx + 2 * self.MOVE_OFFSET)
                if square.piece is None:
                    potentialMoves.append(Move(self, square))
        return potentialMoves

    def get_capture_moves(self, columnOffset: int) -> List[Move]:
        """check the possibility of capturing a piece on the given column offset: left(-1) or right(1)"""

        square = self.square.board.get_square_by_coords_opt(self.square.colIdx + columnOffset, self.square.rowIdx + self.MOVE_OFFSET)
        if square is not None and square.piece is not None and square.piece.color != self.color:
            return self.generate_pawn_move(square)
        return []

    def calc_potential_moves_pinned(self, direction: Direction) -> List[Move]:
        """the piece is pinned in the given direction, it can potentially still move in the pin and the opposite direction"""

        potentialMoves: List[Move] = []
        if direction == Direction.RIGHT or direction == Direction.LEFT:
            # a pawn pinned from side can never move
            return potentialMoves

        elif direction == Direction.UP or direction == Direction.DOWN:
            # a pawn pinned from front or back can only move forward
            potentialMoves += self.get_forward_moves()

        elif direction == Direction.UP_RIGHT or direction == Direction.DOWN_LEFT:
            # pawn pinned diagonally can possibly capture in the pin direction
            potentialMoves += self.get_capture_moves(self.MOVE_OFFSET)

            # a diagonally pinned pawn can even capture en passant, en passant pin special pin is impossible in this case (the pawn is already pinned)
            enPassant = self.square.board.enPassantPawnSquare[-1]
            if enPassant is not None and self.square.rowIdx == self.EN_PASSANT_ROW and enPassant.idx - self.square.idx == self.MOVE_OFFSET:
                potentialMoves.append(Move(self, self.square.board.get_square_by_coords(enPassant.colIdx, enPassant.rowIdx + self.MOVE_OFFSET),
                                           isEnPassant=True))

        else: # direction is LEFT_UP or RIGHT_DOWN
            # capture in the other direction is analogous to the previous case
            potentialMoves += self.get_capture_moves(-self.MOVE_OFFSET)
            enPassant = self.square.board.enPassantPawnSquare[-1]
            if enPassant is not None and self.square.rowIdx == self.EN_PASSANT_ROW and self.square.idx - enPassant.idx == self.MOVE_OFFSET:
                potentialMoves.append(Move(self, self.square.board.get_square_by_coords(enPassant.colIdx, enPassant.rowIdx + self.MOVE_OFFSET),
                                           isEnPassant=True))

        return potentialMoves

    def generate_pawn_move(self, targetSquare: Square) -> List[Move]:
        """normally the pawn has one possible move to the given square, but if it's a promotion, there are 4 possible moves"""

        if targetSquare.rowIdx != self.PROMOTION_ROW:
            return [Move(self, targetSquare)]
        else:
            return [Move(self, targetSquare, newPiece=piece) for piece in [PieceType.KNIGHT, PieceType.BISHOP, PieceType.ROOK,
                                                                                             PieceType.QUEEN]]
    
    def calc_attacked_squares(self) -> Set[Square]:
        """calculates squares attacked by the piece"""

        if self.square.colIdx == 0:
            return {self.square.board.get_square_by_coords(self.square.colIdx + 1, self.square.rowIdx + self.MOVE_OFFSET)}
        elif self.square.colIdx == 7:
            return {self.square.board.get_square_by_coords(self.square.colIdx - 1, self.square.rowIdx + self.MOVE_OFFSET)}
        else:
            return {
                self.square.board.get_square_by_coords(self.square.colIdx + 1, self.square.rowIdx + self.MOVE_OFFSET),
                self.square.board.get_square_by_coords(self.square.colIdx - 1, self.square.rowIdx + self.MOVE_OFFSET)
            }
        
    def is_en_passant_pin(self, enPassantSquare: Square) -> bool:
        """
        checks very specific situation when the pawn is not technically pinned - there is another pawn in the path, but taking en passant would
        still expose the king to check (like white: Kh5, pf5, black Qe5, pg5, white to move, taking en passant would expose the king to check,
        even though the f5 pawn is technically not pinned)
        """
        assert enPassantSquare is not None and enPassantSquare.piece is not None and enPassantSquare.piece.kind == PieceType.PAWN and\
            enPassantSquare.piece.color != self.color, f"no opponent's pawn to take en passant"
        king = self.square.board.get_king(self.color)
        if not king: # this cannot occur in a regular game
            return False

        # the special pin can only occur on the en passant row
        if  king.square.rowIdx != enPassantSquare.rowIdx:
            return False

        # what is the direction of the potential pin (from king to pinner)
        direction = Direction.LEFT if king.square.colIdx > enPassantSquare.colIdx else Direction.RIGHT

        # on the way from own king towards the pinner, the first piece must be the own pawn (that wants to take en passant) or the opponent's pawn
        firstSquare = self.square.board.find_first_occupied_square_in_dir(king.square, direction)
        if firstSquare is None or (firstSquare != enPassantSquare and firstSquare.piece != self):
            return False

        # second piece must be the other relevant pawn (taker or being taken) and must be right next to the first piece
        secondSquare = self.square.board.get_square_by_coords_opt(firstSquare.colIdx + (1 if direction == Direction.RIGHT else -1), firstSquare.rowIdx)
        if secondSquare is None or secondSquare.piece is None:
            return False

        # now check that those two pawns have been found
        if not (firstSquare == enPassantSquare and secondSquare.piece == self or firstSquare.piece == self and secondSquare == enPassantSquare):
            return False

        # the third piece must be the opponent's queen or rook
        thirdSquare = self.square.board.find_first_occupied_square_in_dir(secondSquare, direction)
        if thirdSquare is None:
            return False
        assert thirdSquare.piece is not None, f"find_first_occupied_square_in_dir returned an empty square"
        if thirdSquare.piece.color == self.color or thirdSquare.piece.kind not in [PieceType.QUEEN, PieceType.ROOK]:
            return False

        # all conditions are met, the pawn is pinned
        return True

    def __str__(self):
        return f'p{self.square.name}'

    def __repr__(self):
        return f'Pawn({self.color}, {self.square})'
