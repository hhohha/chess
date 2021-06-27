from constants import *
from lib import *

class cMove:
    __slots__ = 'piece', 'toSqr', 'fromSqr', 'newPiece', 'pieceTaken'

    def __init__(self, piece, toSqr, newPiece=None, pieceTaken=None):
        self.piece = piece
        self.toSqr = toSqr
        self.fromSqr = piece.square
        self.newPiece = newPiece
    
    def __eq__(self, other):
        return self.piece == other.piece and self.fromSqr == other.fromSqr and self.toSqr == other.toSqr and self.newPiece == other.newPiece
    
    def __str__(self):
        return str(main_board.getSquare(self.fromSqr).piece) + str(main_board.getSquare(self.toSqr))

    def is_castling(self):
        return self.piece == KING and abs(self.fromSqr - self.toSqr) == 2
    
    def is_promotion(self):
        return self.piece == PAWN and (self.toSqr < 8 or self.toSqr > 55)

    def is_en_passant(self):
        return movPiece.kind == PAWN and fromSqr.colIdx != toSqr.colIdx and toSqr.piece is None

    def __repr__(self):
        return self.__str__()
