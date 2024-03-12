from __future__ import annotations
from typing import Optional
from piece import Piece

class Square:
    def __init__(self, idx: int):
        self.idx = idx
        self.rowIdx = idx // 8
        self.colIdx = idx % 8
        self.piece: Optional[Piece] = None
        self.name: str = chr(self.colIdx + 97) + str(self.rowIdx + 1)
        
    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Square):
            return NotImplemented
        return self.idx == other.idx
    
    def __hash__(self) -> int:
        return hash(self.idx)
        
    def __repr__(self) -> str:
        return f'Square({self.idx})'
