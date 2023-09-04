from typing import List

from constants import PieceType, Color
from move import Move
from piece import Piece
from square import Square


class King(Piece):
    def __init__(self, color: Color, square: Square):
        super().__init__(PieceType.KING, color, square)
        self.isLight = False

    def calc_potential_moves(self) -> List[Move]:
        """
        TODO - do we need the ownPieces parameter?
        TODO - why cannot king's potential move lead to a check (it's not the same as legal move)?
        potential moves don't respect checks
        :return: list of potential moves
        """
        potentialMoves: List[Move] = []
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + i, self.square.colIdx + j)
            if square is None:
                continue
        
            if not square.is_attacked_by(not self.color) and (square.piece is None or square.piece.color != self.color):
                potentialMoves.append(Move(self, square))

        return potentialMoves
    
    def calc_potential_moves_pinned(self, direction):
        return []
    
    def calc_attacked_squares(self) -> List[Square]:
        attackedSquares: List[Square] = []
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + j, self.square.colIdx + i)
            if square is not None:
                attackedSquares.append(square)
        return attackedSquares
                

    def __str__(self):
        return 'K' + self.square.getCoord()

    def __repr__(self):
        return f'King ({self.color}, {self.square})'
