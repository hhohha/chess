from piece import cPiece
from constants import *

class cBishop (cPiece):
    def __init__(self, color):
        super().__init__(BISHOP, color)
        self.is_sliding = True
        
    def getPotentialMoves(self, ownPieces=False):
        resLst = []
        
        for func in [lambda x, y: (x + 1, y + 1), lambda x, y: (x - 1, y - 1), lambda x, y: (x - 1, y + 1), lambda x, y: (x + 1, y - 1)]:
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
    
    def get_potential_moves_pinned(self, direction):
        if direction <= RIGHT:
            return []
        moves = self.square.board.find_first_piece_in_dir(self.square, direction, includePath=True)
        moves += self.square.board.find_first_piece_in_dir(self.square, reverse_dir(direction), includePath=True)
        moves.pop() # the previous line acually would include the square with own king
        
        return moves

    def isAttackingSqr(self, colIdx, rowIdx):
        if self.square.colIdx == colIdx and self.square.rowIdx == rowIdx:
            return False
        if abs(colIdx - self.square.colIdx) != abs(rowIdx - self.square.rowIdx):
            return False
        
        colDiff = 1 if self.square.colIdx < colIdx else -1
        rowDiff = 1 if self.square.rowIdx < rowIdx else -1
        col, row = self.square.colIdx + colDiff, self.square.rowIdx + rowDiff
        
        while True:
            if col == colIdx and row == rowIdx:
                return True
            if self.square.board.getSquare(col, row).piece is not None:
                return False
            col, row = col + colDiff, row + rowDiff
        
    def __str__(self):
        return ' B' if self.color == WHITE else '*B'
