from piece import cPiece
from constants import *

class cPawn (cPiece):
    def __init__(self, color):
        super().__init__(PAWN, color)
        self.d = 1 if self.color == WHITE else -1
        
    def getPotentialMoves(self):
        resLst = []
        
        square = self.square.board.getSquare(self.square.colIdx, self.square.rowIdx + self.d)
        if square.piece is None:
            resLst.append(square)
            if self.movesCnt == 0:
                square = self.square.board.getSquare(self.square.colIdx, self.square.rowIdx + 2*self.d)
                if square.piece is None:
                    resLst.append(square)
                    
        square = self.square.board.getSquare(self.square.colIdx + 1, self.square.rowIdx + self.d)
        if square is not None and square.piece is not None and square.piece.color != self.color:
            resLst.append(square)
            
        square = self.square.board.getSquare(self.square.colIdx - 1, self.square.rowIdx + self.d)
        if square is not None and square.piece is not None and square.piece.color != self.color:
            resLst.append(square)
        
        return resLst
    
    def getAttackedSquares(self):
        resLst = []
        
        square = self.square.board.getSquare(self.square.colIdx + 1, self.square.rowIdx + self.d)
        if square is not None:
            resLst.append(square)
        square = self.square.board.getSquare(self.square.colIdx - 1, self.square.rowIdx + self.d)
        if square is not None:
            resLst.append(square)
        
        return resLst
    
    def isAttackingSqr(self, colIdx, rowIdx):
        return abs(colIdx - self.square.colIdx) == 1 and rowIdx == self.square.rowIdx + self.d
        
    def __str__(self):
        return ' p' if self.color == WHITE else '*p'
