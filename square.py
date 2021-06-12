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
        
    def getCoord(self):
        return chr(self.colIdx + 97) + str(self.rowIdx + 1)
        
    def isInCheck(self, myColor):
        return False
    
    def isFree(self):
        return self.piece is None
