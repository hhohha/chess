from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from constants import PieceType, Direction
if TYPE_CHECKING:
    from square import Square

letterToPiece = {
    'p': PieceType.PAWN,
    'n': PieceType.KNIGHT,
    'b': PieceType.BISHOP,
    'r': PieceType.ROOK,
    'q': PieceType.QUEEN,
    'k': PieceType.KING
}

pieceToLetter = {
    PieceType.PAWN: 'p',
    PieceType.KNIGHT: 'N',
    PieceType.BISHOP: 'B',
    PieceType.ROOK: 'R',
    PieceType.QUEEN: 'Q',
    PieceType.KING: 'K'
}
    
def kind_to_letter(kind: PieceType) -> str:
    return 'pNBRQK'[kind.value]

def reverse_dir(direction: Direction) -> Direction:
    return [Direction.DOWN, Direction.UP, Direction.RIGHT, Direction.LEFT, Direction.DOWN_RIGHT, Direction.DOWN_LEFT, Direction.UP_RIGHT,
            Direction.UP_LEFT][direction.value]

def is_same_col_or_row(sqr1: Square, sqr2: Square) -> bool:
    return sqr1.colIdx == sqr2.colIdx or sqr1.rowIdx == sqr2.rowIdx

def is_same_diag(sqr1: Square, sqr2: Square) -> bool:
    return abs(sqr1.colIdx - sqr2.colIdx) == abs(sqr1.rowIdx - sqr2.rowIdx)

def move_in_direction(col: int, row: int, direction: Direction) -> Tuple[int ,int]:
    # UP = 0, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT 
    return [(col, row+1), (col, row-1), (col-1, row), (col+1, row), (col-1, row+1), (col+1, row+1), (col-1, row-1), (col+1, row-1)][direction.value]

def square_idx_to_coord(idx: int) -> str:
    return chr(idx % 8 + 97) + str(idx // 8 + 1)

def coord_to_square_idx(coord: str) -> int:
    return (ord(coord[0]) - 97) + (int(coord[1]) - 1) * 8