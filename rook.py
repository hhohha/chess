from typing import List

from constants import Color, PieceType, Direction
from piece import SlidingPiece
from square import Square

class Rook (SlidingPiece):
    def __init__(self, color: Color, square:Square):
        super().__init__(PieceType.ROOK, color, square)
        self.isLight = False    # light piece is a bishop or a knight
        self.slidingDirections: List[Direction] = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    def is_sliding(self) -> bool:
        return True

    def get_sliding_directions(self) -> List[Direction]:
        return self.slidingDirections
        
    def __str__(self):
        return f'R{self.square.name}'
    
    def __repr__(self):
        return f'Rook({self.color}, {self.square})'
