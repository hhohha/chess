from constants import *
from lib import *

class cMove:
    __slots__ = 'piece', 'toSqr', 'fromSqr', 'newPiece', 'pieceTaken', 'isEnPassant', 'isPromotion'

    def __init__(self, piece, toSqr, newPiece=None, pieceTaken=None, isEnPassant=False, isPromotion=False):
        self.piece = piece
        self.toSqr = toSqr
        self.fromSqr = piece.square
        self.newPiece = newPiece
        self.pieceTaken = pieceTaken
        self.isEnPassant = isEnPassant
        self.isPromotion = isPromotion
    
    def __eq__(self, other):
        return self.piece == other.piece and self.fromSqr == other.fromSqr and self.toSqr == other.toSqr and self.newPiece == other.newPiece
    
    def __str__(self):
        return str(self.piece) + '-' + str(self.toSqr)

    def is_castling(self):
        return self.piece.kind == KING and abs(self.fromSqr.idx - self.toSqr.idx) == 2

    def __repr__(self):
        return self.__str__()
