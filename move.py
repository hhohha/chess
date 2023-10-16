from __future__ import annotations
from constants import PieceType
from typing import TYPE_CHECKING, Optional
from square import Square
from utils import pieceToLetter

if TYPE_CHECKING:
    from piece import Piece

class Move:
    # TODO - isPromotion looks redundant - if so, remove it
    __slots__ = 'piece', 'toSqr', 'fromSqr', 'newPiece', 'pieceTaken', 'isEnPassant', 'isPromotion'#, 'pastEP'

    def __init__(self, piece: Piece, toSqr: Square, newPiece: Optional[PieceType]=None, pieceTaken: Optional[Piece]=None, isEnPassant: bool=False,
                 isPromotion: bool=False):
        self.piece = piece
        self.toSqr = toSqr
        self.fromSqr: Square = piece.square
        self.newPiece = newPiece
        self.pieceTaken = pieceTaken
        self.isEnPassant = isEnPassant
        self.isPromotion = isPromotion
        #self.pastEP = None
    
    def __eq__(self, other: Move) -> bool:
        return self.piece == other.piece and self.fromSqr == other.fromSqr and self.toSqr == other.toSqr and self.newPiece == other.newPiece
    
    def __str__(self) -> str:
        return f'{str(self.piece)[0]}{self.fromSqr}-{self.toSqr}{pieceToLetter[self.newPiece] if self.newPiece else ""}'

    def __hash__(self) -> int:
        return hash((self.piece, self.fromSqr, self.toSqr, self.newPiece))

    def is_castling(self) -> bool:
        return self.piece.kind == PieceType.KING and abs(self.fromSqr.idx - self.toSqr.idx) == 2

    def __repr__(self) -> str:
        return f'Move({self.piece}, {self.toSqr}, {self.newPiece}, {self.pieceTaken}, {self.isEnPassant}, {self.isPromotion})'
