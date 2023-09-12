from typing import List
from constants import Color, PieceType, Direction
from move import Move
from piece import Piece
from square import Square

class Knight (Piece):
    def __init__(self, color: Color, square: Square):
        super().__init__(PieceType.KNIGHT, color, square)
        self.isLight = True

    def calc_potential_moves(self) -> List[Move]:
        """
        :return: list of knight's potential moves
        """
        potentialMoves = []
        for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            square = self.square.board.get_square_by_coords(self.square.colIdx + i, self.square.rowIdx + j)
            if square is not None and (square.piece is None or square.piece.color != self.color):
                potentialMoves.append(Move(self, square))

        return potentialMoves

    def get_attacked_squares(self) -> List[Square]:
        """
        :return: list of squares attacked by the piece
        """
        attackedSquares: List[Square] = []
        for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            square = self.square.board.get_square_by_coords(self.square.colIdx + i, self.square.rowIdx + j)
            if square is not None:
                attackedSquares.append(square)

        return attackedSquares

    def calc_potential_moves_pinned(self, direction: Direction) -> List[Move]:
        return []

    def __str__(self):
        return 'N' + self.square.getCoord()

    def __repr__(self):
        return 'N' + self.square.getCoord()
