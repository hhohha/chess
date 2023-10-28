from typing import List, Set
from constants import Color, PieceType, Direction
from move import Move
from piece import Piece
from square import Square

class Knight (Piece):
    def __init__(self, color: Color, square: Square):
        super().__init__(PieceType.KNIGHT, color, square)
        self.isLight = True
        self.potentialMoves: List[Move] = []

    def calc_attacked_squares(self):
        assert False, 'calc_attacked_squares called on Knight'
    def calc_potential_moves(self):
        assert False, 'calc_potential_moves called on Knight'

    def recalculate(self) -> None:
        """recalculate potential moves and attacked squares"""
        for sqr in self.attackedSquares:
            sqr.get_attacked_by(self.color).remove(self)

        self.potentialMoves.clear()
        self.attackedSquares.clear()
        for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            square = self.square.board.get_square_by_coords_opt(self.square.colIdx + i, self.square.rowIdx + j)
            if square is not None:
                self.attackedSquares.add(square)
                if square.piece is None or square.piece.color != self.color:
                    self.potentialMoves.append(Move(self, square))

        for sqr in self.attackedSquares:
            sqr.get_attacked_by(self.color).add(self)

    # def update_potential_moves(self) -> None:
    #     """calculate a list of potential moves"""
    #     self.potentialMoves = []
    #     for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
    #         square = self.square.board.get_square_by_coords_opt(self.square.colIdx + i, self.square.rowIdx + j)
    #         if square is not None and (square.piece is None or square.piece.color != self.color):
    #             self.potentialMoves.append(Move(self, square))
    #
    # def update_attacked_squares(self) -> None:
    #     """calculates squares attacked by the piece"""
    #     self.attackedSquares: Set[Square] = set()
    #     for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
    #         square = self.square.board.get_square_by_coords_opt(self.square.colIdx + i, self.square.rowIdx + j)
    #         if square is not None:
    #             self.attackedSquares.add(square)

    def calc_potential_moves_pinned(self, direction: Direction) -> List[Move]:
        """calculate a list of potential moves when pinned - a pinned knight can never move"""
        return []

    def __str__(self):
        return f'N{self.square.name}'

    def __repr__(self):
        return f'Knight ({self.color}, {self.square})'
