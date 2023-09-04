from constants import PieceType
from typing import TYPE_CHECKING
from square import Square
if TYPE_CHECKING:
    from piece import Piece


# TODO - refactor

class Move:
    __slots__ = 'piece', 'toSqr', 'fromSqr', 'newPiece', 'pieceTaken', 'isEnPassant', 'isPromotion', 'pastEP'

    def __init__(self, piece, toSqr, newPiece=None, pieceTaken=None, isEnPassant=False, isPromotion=False):
        self.piece: Piece = piece
        self.toSqr: Square = toSqr
        self.fromSqr: Square = piece.square
        self.newPiece = newPiece
        self.pieceTaken = pieceTaken
        self.isEnPassant = isEnPassant
        self.isPromotion = isPromotion
        self.pastEP = None
    
    def __eq__(self, other):
        return self.piece == other.piece and self.fromSqr == other.fromSqr and self.toSqr == other.toSqr and self.newPiece == other.newPiece
    
    def __str__(self):
        return str(self.piece)[0] + str(self.fromSqr) + '-' + str(self.toSqr)

    def __hash__(self):
        return hash((self.piece, self.fromSqr, self.toSqr, self.newPiece))

    def is_castling(self):
        return self.piece.kind == PieceType.KING and abs(self.fromSqr.idx - self.toSqr.idx) == 2

    def __repr__(self):
        return self.__str__()
