from typing import List, Tuple, Optional
from constants import PieceType, Color, Direction
from move import Move
from piece import Piece
from square import Square
from utils import move_in_direction


class King(Piece):
    def __init__(self, color: Color, square: Square):
        super().__init__(PieceType.KING, color, square)
        self.isLight = False

    def calc_potential_moves(self, inaccessibleDirs: Optional[List[Direction]]=None) -> List[Move]:
        """
        return king moves that don't walk into a check
        :param inaccessibleDirs: directions in which the king cannot move because if walks into a check even though the square is technically not
            attacked - it is in cover behind the king, e.g. black Ra1, white Kb1 - king cannot escape the check to c1
        :return: list of potential moves
        """
        if inaccessibleDirs is None:
            inaccessibleDirs = []
        potentialMoves: List[Move] = []

        for direction in Direction:
            if direction in inaccessibleDirs:
                continue
            square = self.square.board.get_square_by_coords(*move_in_direction(self.square.colIdx, self.square.rowIdx, direction))
            # the square must exist (not off the board), must not be occupied by a piece of the same color and must not be attacked by the opponent
            if square is not None and (square.piece is None or square.piece.color != self.color) and not square.is_attacked_by(self.color.invert()):
                potentialMoves.append(Move(self, square))

        return potentialMoves
    
    def calc_potential_moves_pinned(self, direction) -> List[Move]:
        assert False, "king cannot be pinned"
        return []
    
    def calc_attacked_squares(self) -> None:
        """calculates squares attacked by the piece"""
        self.attackedSquares.clear()
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.get_square_by_coords(self.square.colIdx + i, self.square.rowIdx + j)
            if square is not None:
                self.attackedSquares.add(square)


    def __str__(self):
        return f'K{self.square.name}'

    def __repr__(self):
        return f'King ({self.color}, {self.square})'
