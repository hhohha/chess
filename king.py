from piece import cPiece
from constants import *

class cKing (cPiece):
    def __init__(self, color):
        super().__init__(KING, color)
        
    # potential moves don't respect checks
    def getPotentialMoves(self):
        resLst = []
        
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.getSquare(self.square.rowIdx + i, self.square.colIdx + j)
            if square is None:
                continue
        
            if (square.piece == None or square.piece.color != self.color):
                resLst.append(square)
                
        if self.square.board.isShortCastlePossible(self.color):
            resLst.append(self.square.board.getSquare('g1'))
            
        if self.square.board.isLongCastlePossible(self.color):
            resLst.append(self.square.board.getSquare('c1'))
                
        return resLst
    
    def getAttackedSquares(self):
        resLst = []
        
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.getSquare(self.square.colIdx + i, self.square.rowIdx + j)
            if square is not None:
                resLst.append(square)
                
        return resLst
    
    def isAttackingSqr(self, colIdx, rowIdx):
        if self.square.colIdx == colIdx and self.square.rowIdx == rowIdx:
            return False
        return abs(self.square.colIdx - colIdx) <= 1 and abs(self.square.rowIdx - rowIdx) <= 1
    
    def __str__(self):
        return ' K' if self.color == WHITE else '*K' 
