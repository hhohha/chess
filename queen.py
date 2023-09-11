from typing import List
from piece import SlidingPiece
from square import Square
from constants import Color, PieceType, Direction

class Queen (SlidingPiece):
    def __init__(self, color: Color, square: Square):
        super().__init__(PieceType.QUEEN, color, square)
        self.isLight = False   # light piece is a bishop or a knight
        self.slidingDirections = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP_LEFT, Direction.UP_RIGHT,
                                  Direction.DOWN_LEFT, Direction.DOWN_RIGHT]

    def get_sliding_directions(self) -> List[Direction]:
        return self.slidingDirections

    def is_sliding(self) -> bool:
        return True

    def __str__(self):
        return 'Q' + self.square.getCoord()

    def __repr__(self):
        return f'Queen({self.color}, {self.square})'
