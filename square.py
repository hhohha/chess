from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING, Set
from constants import Color

if TYPE_CHECKING:
    from board import Board
    from piece import Piece


class Square:
    def __init__(self, idx: int, board: Board):
        self.idx = idx
        self.rowIdx = idx // 8
        self.colIdx = idx % 8
        self.piece: Optional[Piece] = None
        self.board = board
        self.attackedByWhites: Set[Piece] = set()
        self.attackedByBlacks: Set[Piece] = set()
        self.name: str = chr(self.colIdx + 97) + str(self.rowIdx + 1)
        #self.attackedByWhites = [[]]
        #self.attackedByBlacks = [[]]
        
    def __str__(self) -> str:
        return self.name

    def is_free(self) -> bool:
        return self.piece is None
    
    def is_attacked_by(self, color: Color) -> bool:
        return len(self.get_attacked_by(color)) > 0

    def get_attacked_by(self, color: Optional[Color]=None) -> Set[Piece]:
        if color is None:
            return self.attackedByWhites | self.attackedByBlacks
        return self.attackedByWhites if color == Color.WHITE else self.attackedByBlacks

    # TODO - color == None may be not efficient - unit_tests, and if so, remove
    # def get_attacked_by(self, color=None):
    #     if color == Color.WHITE:
    #         return self.attackedByWhites[-1]
    #     if color == Color.BLACK:
    #         return self.attackedByBlacks[-1]
    #     return self.attackedByWhites[-1] + self.attackedByBlacks[-1]

    def __eq__(self, other: Square) -> bool:
        return self.idx == other.idx
    
    def __hash__(self) -> int:
        return hash(self.idx)
        
    def __repr__(self) -> str:
        return f'Square({self.idx}, {self.board})'

    def clear(self) -> None:
        self.piece = None
        self.attackedByBlacks.clear()
        self.attackedByWhites.clear()
