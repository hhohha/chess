from piece import cPieceNotSliding
from constants import *
from move import cMove

class cKnight (cPieceNotSliding):
    def __init__(self, color, square):
        super().__init__(KNIGHT, color, square)
        self.is_light = True

    def calc_potential_moves(self, ownPieces=False):
        for (i, j) in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + i, self.square.colIdx + j)
            if square is not None and (square.piece is None or square.piece.color != self.color or ownPieces):
                yield cMove(self, square)

    #def calculate_potentional_squares(self):
        #self.potentialSquares.clear()
        #for sqr in self.get_attacked_squares():
            #if sqr.piece is None or sqr.piece.color != self.color:
                #self.potentialSquares.append(sqr)

    def calc_potential_moves_pinned(self, direction):
        return
        yield

    def __str__(self):
        return 'N' + self.square.getCoord()

    def __repr__(self):
        return 'N' + self.square.getCoord()
