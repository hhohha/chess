from piece import cPiece
from constants import *
from move import cMove

class cKnight (cPiece):
    def __init__(self, color, square):
        super().__init__(KNIGHT, color, square)

    def is_light(self):
        return True

    def get_potential_moves(self, ownPieces=False):
        
        for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + i, self.square.colIdx + j)
            if square is not None and (square.piece is None or square.piece.color != self.color or ownPieces):
                yield cMove(self, square)

    def get_potential_moves_pinned(self, direction):
        return
        yield

    #def isAttackingSqr(self, colIdx, rowIdx):
        #return abs(colIdx - self.square.colIdx) == 1 and abs(rowIdx - self.square.rowIdx) == 2 or \
            #abs(colIdx - self.square.colIdx) == 2 and abs(rowIdx - self.square.rowIdx) == 1
        
    def __str__(self):
        return 'N' + self.square.getCoord()

    def __repr__(self):
        return 'N' + self.square.getCoord()
