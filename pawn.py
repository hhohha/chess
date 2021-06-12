from piece import cPiece
from constants import *

class cPawn (cPiece):
    def __init__(self, color):
        super().__init__(PAWN, color)
        if self.color == WHITE:
            self.d = 1
            self.base_row = 1
        else:
            self.d = -1
            self.base_row = 6
        
    def getPotentialMoves(self):
        resLst = []
        
        square = self.square.board.getSquare(self.square.rowIdx + self.d, self.square.colIdx)
        if square.piece is None:
            resLst.append(square)
            if self.square.rowIdx == self.base_row:
                square = self.square.board.getSquare(self.square.rowIdx + 2*self.d, self.square.colIdx)
                if square.piece is None:
                    resLst.append(square)
                    
        for i in [1, -1]:
            square = self.square.board.getSquare(self.square.rowIdx + self.d, self.square.colIdx + i)
            if square is not None and square.piece is not None and square.piece.color != self.color:
                resLst.append(square)
        
        return resLst
    
    def getAttackedSquares(self):
        resLst = []

        for i in [1, -1]:
            square = self.square.board.getSquare(self.square.rowIdx + self.d, self.square.colIdx + i)
            if square is not None:
                resLst.append(square)

        return resLst
    
    def isAttackingSqr(self, colIdx, rowIdx):
        return abs(colIdx - self.square.colIdx) == 1 and rowIdx == self.square.rowIdx + self.d
        
    def __str__(self):
        return ' p' if self.color == WHITE else '*p'
