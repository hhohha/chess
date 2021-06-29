from piece import cPiece
from constants import *
from lib import *
from move import cMove

class cRook (cPiece):
    def __init__(self, color, square):
        super().__init__(ROOK, color, square)

    def is_sliding(self):
        return True

    def get_potential_moves(self, ownPieces=False):
        for func in [lambda x, y: (x + 1, y), lambda x, y: (x - 1, y), lambda x, y: (x, y + 1), lambda x, y: (x, y - 1)]:
            i, j = 0, 0
            while True:
                i, j = func(i, j)
                square = self.square.board.get_square_by_coords(self.square.rowIdx + i, self.square.colIdx + j)
                if square is None:
                    break
                
                if square.piece is None:
                    yield cMove(self, square)
                elif square.piece.color != self.color:
                    yield cMove(self, square)
                    break
                else:
                    if ownPieces:
                        yield cMove(self, square)
                    break

    def get_potential_moves_pinned(self, direction):
        if direction > RIGHT:
            return
        
        # can move in the direction of the pinner including its capture
        for square in self.square.board.find_first_piece_in_dir(self.square, direction, includePath=True):
            yield cMove(self, square)

        # can move towards the king but the last move would actually capture own king
        for square in self.square.board.find_first_piece_in_dir(self.square, reverse_dir(direction), includePath=True)[:-1]:
            yield cMove(self, square)

    #def isAttackingSqr(self, colIdx, rowIdx):
        #if self.square.colIdx == colIdx and self.square.rowIdx == rowIdx:
            #return False
        #if self.square.colIdx != colIdx and self.square.rowIdx != rowIdx:
            #return False
        
        #if colIdx == self.square.colIdx and rowIdx > self.square.rowIdx:
            #colDiff, rowDiff = 0, 1
        #elif colIdx == self.square.colIdx:
            #colDiff, rowDiff = 0, -1
        #elif colIdx > self.square.colIdx:
            #colDiff, rowDiff = 1, 0
        #else:
            #colDiff, rowDiff = -1, 0
        
        #col, row = self.square.colIdx + colDiff, self.square.rowIdx + rowDiff
        #while True:
            #if col == colIdx and row == rowIdx:
                #return True
            #if self.board.get_square_by_coords(col, row).piece is not None:
                #return False
            #col, row = col + colDiff, row + rowDiff
        
    def __str__(self):
        return 'R' + self.square.getCoord()
    
    def __repr__(self):
        return 'R' + self.square.getCoord()
