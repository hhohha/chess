from constants import *

class cMove:
    __slots__ = 'piece', 'toSqr', 'fromSqr', 'newPiece'

    def __init__(self, piece, toSqr, newPiece=None):
        self.piece = piece
        self.toSqr = toSqr
        self.fromSqr = piece.square
        self.newPiece = newPiece
    
    def __eq__(self, other):
        return self.piece == other.piece and self.toSqr == other.toSqr and self.newPiece == other.newPiece
    
    def __str__(self):
        return str(self.piece.__repr__()) + '-' + str(self.toSqr.__repr__())

    def is_castling(self):
        return self.piece.kind == KING and abs(self.fromSqr.idx - self.toSqr.idx) == 2
    
    def is_promotion(self):
        return self.piece.kind == PAWN and self.piece.promote_row == self.toSqr.rowIdx
    
    def is_en_passant(self):
        return self.piece.kind == PAWN and self.fromSqr.colIdx != self.toSqr.colIdx and self.toSqr.piece is None

    def __repr__(self):
        return self.__str__()
