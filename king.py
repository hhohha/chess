from piece import cPiece
from constants import *
from move import cMove

class cKing (cPiece):
    def __init__(self, color, square):
        super().__init__(KING, color, square)
        
    # potential moves don't respect checks
    def get_potential_moves(self):
        moves = []
        
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + i, self.square.colIdx + j)
            if square is None:
                continue
        
            if (not square.is_attacked_by(not self.color) and (square.piece is None or square.piece.color != self.color)):
                moves.append(cMove(self, square))

        return moves
    
    def get_potential_moves_pinned(self, direction):
        return []
    
    def getAttackedSquares(self):
        moves = []
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + j, self.square.colIdx + i)
            if square is not None:
                moves.append(square)
                
        return moves
    
    #def is_attacking_sqr(self, sqr):
        #if self.square.colIdx == sqr.colIdx and self.square.rowIdx == sqr.rowIdx:
            #return False
        #return abs(self.square.colIdx - sqr.colIdx) <= 1 and abs(self.square.rowIdx - sqr.rowIdx) <= 1
    
    def __str__(self):
        return 'K' + self.square.getCoord()

    def __repr__(self):
        return 'K' + self.square.getCoord()
