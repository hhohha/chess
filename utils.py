from typing import Tuple

from constants import *

# TODO - refactor

letterToPiece = {
    'p': PieceType.PAWN,
    'n': PieceType.KNIGHT,
    'b': PieceType.BISHOP,
    'r': PieceType.ROOK,
    'q': PieceType.QUEEN,
    'k': PieceType.KING
}
    
def kind_to_letter(kind: PieceType) -> str:
    return 'pNBRQK'[kind.value]

def reverse_dir(direction: Direction) -> Direction:
    return [Direction.DOWN, Direction.UP, Direction.RIGHT, Direction.LEFT, Direction.DOWN_RIGHT, Direction.DOWN_LEFT, Direction.UP_RIGHT,
            Direction.UP_LEFT][direction.value]

def is_same_col_or_row(sqr1, sqr2):
    return sqr1.colIdx == sqr2.colIdx or sqr1.rowIdx == sqr2.rowIdx

def is_same_diag(sqr1, sqr2):
    return abs(sqr1.colIdx - sqr2.colIdx) == abs(sqr1.rowIdx - sqr2.rowIdx)

def move_in_direction(row: int, col: int, direction: Direction) -> Tuple[int ,int]:
    # UP = 0, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT 
    return [(col, row+1), (col, row-1), (col-1, row), (col+1, row), (col-1, row+1), (col+1, row+1), (col-1, row-1), (col+1, row-1)][direction.value]

def squareIdx_to_coord(idx):
    return chr(idx % 8 + 97) + str(idx // 8 + 1)

def coord_to_squareIdx(coord) -> int:
    return (ord(coord[0]) - 97) + (int(coord[1]) - 1) * 8