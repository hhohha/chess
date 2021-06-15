from piece import cPiece
from constants import *
from move import cMove

class cKing (cPiece):
    def __init__(self, color):
        super().__init__(KING, color)
        self.is_sliding = False
        
    # potential moves don't respect checks
    def get_potential_moves(self):
        moves = []
        
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.getSquare(self.square.rowIdx + i, self.square.colIdx + j)
            if square is None:
                continue
        
            if (not square.is_attacked_by(not self.color) and (square.piece == None or square.piece.color != self.color)):
                moves.append(cMove(self, square))

        return moves
    
    def get_potential_moves_pinned(self, direction):
        return []
    
    def getAttackedSquares(self):
        moves = []
        
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.getSquare(self.square.rowIdx + j, self.square.colIdx + i)
            if square is not None:
                moves.append(square)
                
        return moves
    
    def isAttackingSqr(self, colIdx, rowIdx):
        if self.square.colIdx == colIdx and self.square.rowIdx == rowIdx:
            return False
        return abs(self.square.colIdx - colIdx) <= 1 and abs(self.square.rowIdx - rowIdx) <= 1
    
    def __str__(self):
        return ' K' if self.color == WHITE else '*K' 

    def __repr__(self):
        return 'K' + self.square.getCoord()
