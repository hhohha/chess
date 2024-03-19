from __future__ import annotations
from constants import PieceType
from typing import TYPE_CHECKING, Optional
from square import Square
from utils import pieceToLetter

if TYPE_CHECKING:
    from piece import Piece

class Move:
    def __init__(self, fromSqr: Square, toSqr: Square, newPiece: Optional[PieceType] = None, capturedPiece: Optional[Piece] = None):
        assert fromSqr.piece is not None, f"Invalid Move: there is no piece on the source square {fromSqr}"
        self.piece: Piece = fromSqr.piece
        self.fromSqr = fromSqr
        self.toSqr = toSqr
        self.newPiece = newPiece
        self.isPromotion = self.piece.kind == PieceType.PAWN and (self.toSqr.rowIdx == 0 or self.toSqr.rowIdx == 7)
        self.isCastling = self.piece.kind == PieceType.KING and abs(self.fromSqr.colIdx - self.toSqr.colIdx) > 1
        self.isEnPassant = self.piece.kind == PieceType.PAWN and self.toSqr.piece is None and self.fromSqr.colIdx != self.toSqr.colIdx
        if not self.isEnPassant:
            self.capturedPiece = self.toSqr.piece
        else:
            self.capturedPiece = capturedPiece

    def __str__(self) -> str:
        return f'{str(self.piece)}{self.fromSqr}-{self.toSqr}{pieceToLetter[self.newPiece].upper() if self.newPiece else ""}'

    def __repr__(self) -> str:
        return f'Move({self.fromSqr}, {self.toSqr}, {self.newPiece}, {self.capturedPiece})'
