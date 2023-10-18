from typing import List
from constants import Color, PieceType, Direction
from piece import SlidingPiece
from square import Square

class Bishop (SlidingPiece):
    def __init__(self, color: Color, square: Square):
        super().__init__(PieceType.BISHOP, color, square)
        self.isLight = True
        self.slidingDirections: List[Direction] = [Direction.DOWN_LEFT, Direction.DOWN_RIGHT, Direction.UP_LEFT, Direction.UP_RIGHT]

    def get_sliding_directions(self) -> List[Direction]:
        return self.slidingDirections
        
    def __str__(self) -> str:
        return f'B{self.square.name}'

    def __repr__(self) -> str:
        return f'Bishop({self.color}, {self.square})'
