from typing import List
from constants import Color, PieceType, Direction
from piece import SlidingPiece
from square import Square

class Bishop (SlidingPiece):
    def __init__(self, color: Color, square: Square):
        super().__init__(PieceType.BISHOP, color, square)
        self.isLight = True     # light piece is a bishop or a knight
        self.slidingDirections: List[Direction] = [Direction.DOWN_LEFT, Direction.DOWN_RIGHT, Direction.UP_LEFT, Direction.UP_RIGHT]

    def get_sliding_directions(self) -> List[Direction]:
        return self.slidingDirections
        
    def __str__(self):
        return f'B{self.square.getCoord()}'

    def __repr__(self):
        return f'Bishop({self.color}, {self.square})'
