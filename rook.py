from piece import cPiece
from constants import *

class cRook (cPiece):
    def __init__(self, color):
        super().__init__(ROOK, color)
        
    def getPotentialMoves(self, ownPieces=False):
        resLst = []
        
        for func in [lambda x, y: (x + 1, y), lambda x, y: (x - 1, y), lambda x, y: (x, y + 1), lambda x, y: (x, y - 1)]:
            i, j = 0, 0
            while True:
                i, j = func(i, j)
                square = self.square.board.getSquare(self.square.rowIdx + i, self.square.colIdx + j)
                if square is None:
                    break
                
                if square.piece is None:
                    resLst.append(square)
                elif square.piece.color != self.color:
                    resLst.append(square)
                    break
                else:
                    if ownPieces:
                        resLst.append(square)
                    break

        return resLst
    
    def isAttackingSqr(self, colIdx, rowIdx):
        if self.square.colIdx == colIdx and self.square.rowIdx == rowIdx:
            return False
        if self.square.colIdx != colIdx and self.square.rowIdx != rowIdx:
            return False
        
        if colIdx == self.square.colIdx and rowIdx > self.square.rowIdx:
            colDiff, rowDiff = 0, 1
        elif colIdx == self.square.colIdx:
            colDiff, rowDiff = 0, -1
        elif colIdx > self.square.colIdx:
            colDiff, rowDiff = 1, 0
        else:
            colDiff, rowDiff = -1, 0
        
        col, row = self.square.colIdx + colDiff, self.square.rowIdx + rowDiff
        while True:
            if col == colIdx and row == rowIdx:
                return True
            if self.board.getSquare(col, row).piece is not None:
                return False
            col, row = col + colDiff, row + rowDiff
        
    def __str__(self):
        return ' R' if self.color == WHITE else '*R'
