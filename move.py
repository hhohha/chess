class cMove:
    __slots__ = 'piece', 'toSqr', 'fromSqr', 'newPiece'

    def __init__(self, piece, toSqr, newPiece=None):
        self.piece = piece
        self.toSqr = toSqr
        #self.fromSqr = piece.square
        self.newPiece = newPiece
        
    def __str__(self):
        return self.piece[-1] + self.fromSqr.getCoord() + '-' + self.toSqr.getCoord()
    
    def __eq__(self, other):
        return self.piece == other.piece and self.toSqr == other.toSqr and self.newPiece == other.newPiece
    
    def __str__(self):
        return str(self.piece.__repr__()) + '-' + str(self.toSqr.__repr__())
