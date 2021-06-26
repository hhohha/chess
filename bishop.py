from piece import cPiece
from constants import *
from lib import *
from move import cMove

class cBishop (cPiece):
    def __init__(self, color, square):
        super().__init__(BISHOP, color, square)

    def is_sliding(self):
        return True

    def is_light(self):
        return True

    def get_potential_moves(self, ownPieces=False):
        moves = []
        
        for func in [lambda x, y: (x + 1, y + 1), lambda x, y: (x - 1, y - 1), lambda x, y: (x - 1, y + 1), lambda x, y: (x + 1, y - 1)]:
            i, j = 0, 0
            while True:
                i, j = func(i, j)
                square = self.square.board.getSquareGen(self.square.rowIdx + i, self.square.colIdx + j)
                if square is None:
                    break
                
                if square.piece is None:
                    moves.append(cMove(self, square))
                elif square.piece.color != self.color:
                    moves.append(cMove(self, square))
                    break
                else:
                    if ownPieces:
                        moves.append(cMove(self, square))
                    break

        return moves
        
    def get_potential_moves_pinned(self, direction):
        if direction <= RIGHT:
            return []
        moves = self.square.board.find_first_piece_in_dir(self.square, direction, includePath=True)
        moves += self.square.board.find_first_piece_in_dir(self.square, reverse_dir(direction), includePath=True)
        moves.pop() # the previous line acually would include the square with own king
        
        return list(map(lambda sqr: cMove(self, sqr), moves))

    #def isAttackingSqr(self, colIdx, rowIdx):
        #if self.square.colIdx == colIdx and self.square.rowIdx == rowIdx:
            #return False
        #if abs(colIdx - self.square.colIdx) != abs(rowIdx - self.square.rowIdx):
            #return False
        
        #colDiff = 1 if self.square.colIdx < colIdx else -1
        #rowDiff = 1 if self.square.rowIdx < rowIdx else -1
        #col, row = self.square.colIdx + colDiff, self.square.rowIdx + rowDiff
        
        #while True:
            #if col == colIdx and row == rowIdx:
                #return True
            #if self.square.board.getSquareGen(col, row).piece is not None:
                #return False
            #col, row = col + colDiff, row + rowDiff
        
    def __str__(self):
        return 'B' + self.square.getCoord()

    def __repr__(self):
        return 'B' + self.square.getCoord()
