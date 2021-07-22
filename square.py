from constants import *

class cSquare:
    def __init__(self, idx, board):
        self.idx = idx
        self.rowIdx = idx // 8
        self.colIdx = idx % 8
        self.piece = None
        self.board = board
        #self.attacked_by_whites = set()
        #self.attacked_by_blacks = set()
        self.attacked_by_whites = [(0, set())]
        self.attacked_by_blacks = [(0, set())]
        
    def __str__(self):
        return self.getCoord()
        
    def is_free(self):
        return self.piece is None
        
    def getCoord(self):
        return chr(self.colIdx + 97) + str(self.rowIdx + 1)
    
    def is_attacked_by(self, color):
        return len(self.get_attacked_by(color)) > 0

    # TODO - color == None may be not efficient - test, and if so, remove
    def get_attacked_by(self, color=None):
        if color == WHITE:
            return self.attacked_by_whites[-1][1]
        if color == BLACK:
            return self.attacked_by_blacks[-1][1]
        return self.attacked_by_whites[-1][1].union(self.attacked_by_blacks[-1][1])

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
