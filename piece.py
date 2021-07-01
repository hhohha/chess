from lib import *

class cPiece:
    def __init__(self, kind, color, square):
        global counter
        self.id = square.idx
        self.kind = kind
        self.color = color
        self.movesCnt = 0
        self.attackingSquares = []
        self.potentialSquares = []
        self.square = square
        
    def is_sliding(self):
        return False

    def is_light(self):
        return False
        
    def calculate_attacking_squares(self):
        self.potentialSquares.clear()

        for sqr in self.attackingSquares:
            sqr.get_attacked_by(self.color).remove(self)
            
        self.attackingSquares.clear()
        for sqr in self.getAttackedSquares():
            self.attackingSquares.append(sqr)
            if sqr.piece is None or sqr.piece.color != self.color:
                self.potentialSquares.append(sqr)
        
        for sqr in self.attackingSquares:
            sqr.get_attacked_by(self.color).add(self)
            
    def getAttackedSquares(self):
        for move in self.get_potential_moves(ownPieces=True):
            yield move.toSqr

    def get_legal_moves(self):
        if self.square.board.turn != self.color:
            return []
        return list(filter(lambda move: move.fromSqr == self.square, self.square.board.legal_moves))

    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
