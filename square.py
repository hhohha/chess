from constants import *

class cSquare:
    def __init__(self, idx, board):
        self.idx = idx
        self.rowIdx = idx // 8
        self.colIdx = idx % 8
        self.piece = None
        self.board = board
        self.attacked_by_whites = []
        self.attacked_by_blacks = []
        
    def __str__(self):
        if self.piece == None:
            return " ."
        else:
            return str(self.piece)
        
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
        return self.attacked_by_whites + self.attacked_by_blacks
            
