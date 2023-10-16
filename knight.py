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

    def calc_attacked_squares(self) -> None:
        """calculates squares attacked by the piece"""
        self.attackedSquares.clear()
        for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            square = self.square.board.get_square_by_coords(self.square.colIdx + i, self.square.rowIdx + j)
            if square is not None:
                self.attackedSquares.add(square)

    def calc_potential_moves_pinned(self, direction: Direction) -> List[Move]:
        return []

    def __str__(self):
        return f'N{self.square.name}'

    def __repr__(self):
        return f'Knight ({self.color}, {self.square})'
