from piece import cPiece
from constants import *

class cKnight (cPiece):
    def __init__(self, color):
        super().__init__(KNIGHT, color)
        self.is_sliding = False
        
    def getPotentialMoves(self, ownPieces=False):
        resLst = []
        
        for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            square = self.square.board.getSquare(self.square.rowIdx + i, self.square.colIdx + j)
            if square is not None and (square.piece is None or square.piece.color != self.color or ownPieces):
                resLst.append(square)

        return resLst

    def get_potential_moves_pinned(self, direction):
        return []

    def isAttackingSqr(self, colIdx, rowIdx):
        return abs(colIdx - self.square.colIdx) == 1 and abs(rowIdx - self.square.rowIdx) == 2 or \
            abs(colIdx - self.square.colIdx) == 2 and abs(rowIdx - self.square.rowIdx) == 1
        
    def __str__(self):
        return ' N' if self.color == WHITE else '*N'
