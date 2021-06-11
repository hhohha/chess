class cMove:
    def __init__(self, piece, toSqr, color, newPiece=None):
        self.piece = piece
        self.toSqr = toSqr
        self.fromSqr = piece.square
        self.newPiece = newPiece
        self.color = color
        
    def __str__(self):
        return self.piece[-1] + self.fromSqr.getCoord() + '-' + self.toSqr.getCoord()
