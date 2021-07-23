from piece import cPieceNotSliding
from constants import *
from move import cMove

class cKing (cPieceNotSliding):
    def __init__(self, color, square):
        super().__init__(KING, color, square)
        self.is_light = False
        
    # potential moves don't respect checks
    def calc_potential_moves(self):
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + i, self.square.colIdx + j)
            if square is None:
                continue
        
            if (not square.is_attacked_by(not self.color) and (square.piece is None or square.piece.color != self.color)):
                yield cMove(self, square)
    
    def calc_potential_moves_pinned(self, direction):
        return
        yield
    
    def calc_attacked_squares(self):
        for i, j in [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + j, self.square.colIdx + i)
            if square is not None:
                yield square
                

    def __str__(self):
        return 'K' + self.square.getCoord()

    def __repr__(self):
        return 'K' + self.square.getCoord()
