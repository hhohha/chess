from constants import *

class cSquare:
    def __init__(self, idx, board):
        self.idx = idx
        self.rowIdx = idx // 8
        self.colIdx = idx % 8
        self.piece = None
        self.board = board
        self.attacked_by_whites = set()
        self.attacked_by_blacks = set()
        
    def __str__(self):
        return self.getCoord()
        
    def is_free(self):
        return self.piece is None
        
    def getCoord(self):
        return chr(self.colIdx + 97) + str(self.rowIdx + 1)
    
    def is_attacked_by(self, color):
        return len(self.get_attacked_by(color)) > 0

    def get_attacked_by(self, color=None):
        if color == WHITE:
            return self.attacked_by_whites
        if color == BLACK:
            return self.attacked_by_blacks
        return self.attacked_by_whites.union(self.attacked_by_blacks)

    def __eq__(self, other):
        return self.idx == other.idx
    
    def __hash__(self):
        return hash(self.idx)
        
    def __repr__(self):
        return self.getCoord()

    def clear(self):
        self.piece = None
        self.attacked_by_blacks.clear()
        self.attacked_by_whites.clear()
