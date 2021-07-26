from piece import cPieceSliding
from constants import *
from lib import *
from move import cMove

class cBishop (cPieceSliding):
    def __init__(self, color, square):
        super().__init__(BISHOP, color, square)
        self.is_light = True

    def calc_potential_moves(self, ownPieces=False):
        all_moves = []
        for func in [lambda x, y: (x + 1, y + 1), lambda x, y: (x - 1, y - 1), lambda x, y: (x - 1, y + 1), lambda x, y: (x + 1, y - 1)]:
            i, j = 0, 0
            while True:
                i, j = func(i, j)
                square = self.square.board.get_square_by_coords(self.square.rowIdx + i, self.square.colIdx + j)
                if square is None:
                    break
                
                if square.piece is None:
                    all_moves.append(cMove(self, square))
                elif square.piece.color != self.color:
                    all_moves.append(cMove(self, square))
                    break
                else:
                    if ownPieces:
                        all_moves.append(cMove(self, square))
                    break
        return all_moves
        
    def calc_potential_moves_pinned(self, direction):
        if direction <= RIGHT:
            return []

        all_moves = []

        # can move in the direction of the pinner including its capture
        for square in self.square.board.find_first_piece_in_dir(self.square, direction, includePath=True):
            all_moves.append(cMove(self, square))

        # can move towards the king but the last move would actually capture own king
        for square in self.square.board.find_first_piece_in_dir(self.square, reverse_dir(direction), includePath=True)[:-1]:
            all_moves.append(cMove(self, square))
        return all_moves
        
    def __str__(self):
        return 'B' + self.square.getCoord()

    def __repr__(self):
        return 'B' + self.square.getCoord()
