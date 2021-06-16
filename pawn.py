from piece import cPiece
from move import cMove
from constants import *

class cPawn (cPiece):
    def __init__(self, color):
        super().__init__(PAWN, color)
        self.is_sliding = False
        if self.color == WHITE:
            self.move_offset = 1
            self.base_row = 1
        else:
            self.move_offset = -1
            self.base_row = 6
        
    def get_potential_moves(self):
        moves = []
        
        square = self.square.board.getSquare(self.square.rowIdx + self.move_offset, self.square.colIdx)
        if square.piece is None:
            moves.append(cMove(self, square))
            if self.square.rowIdx == self.base_row:
                square = self.square.board.getSquare(self.square.rowIdx + 2*self.move_offset, self.square.colIdx)
                if square.piece is None:
                    moves.append(cMove(self, square))
                    
        for i in [1, -1]:
            square = self.square.board.getSquare(self.square.rowIdx + self.move_offset, self.square.colIdx + i)
            if square is not None and square.piece is not None and square.piece.color != self.color:
                moves.append(cMove(self, square))
        
        return moves
    
    def get_potential_moves_pinned(self, direction):
        if direction == RIGHT or direction == LEFT:
            return []

        if direction == UP or direction == DOWN:
            sqrFront = self.square.board.getSquare(self.square.rowIdx + self.move_offset, self.square.colIdx)
            if sqrFront.piece is None:
                if self.square.rowIdx == self.base_row:
                    return [cMove(self, sqrFront)]
                
                sqrFront2 = self.square.board.getSquare(self.square.rowIdx + 2*self.move_offset, self.square.colIdx)
                if sqrFront2.piece is None:
                    return [cMove(self, sqrFront), cMove(self, sqrFront2)]
                else:
                    return [cMove(self, sqrFront)]
            else:
                return []

        if direction == UP_RIGHT or direction == DOWN_LEFT:
            sqr = self.square.board.getSquare(self.square.rowIdx + self.move_offset, self.square.colIdx + self.move_offset)
            if sqr is not None and sqr.piece is not None and sqr.piece.color != self.color:
                return [cMove(self, sqr)]
            else:
                return []
        
        # direction is LEFT_UP or RIGHT_DOWN
        sqr = self.square.board.getSquare(self.square.rowIdx + self.move_offset, self.square.colIdx - self.move_offset)
        if sqr is not None and sqr.piece is not None and sqr.piece.color != self.color:
            return [cMove(self, sqr)]
        else:
            return []
    
    def getAttackedSquares(self):
        resLst = []

        for i in [1, -1]:
            square = self.square.board.getSquare(self.square.rowIdx + self.move_offset, self.square.colIdx + i)
            if square is not None:
                resLst.append(square)

        return resLst
    
    def isAttackingSqr(self, colIdx, rowIdx):
        return abs(colIdx - self.square.colIdx) == 1 and rowIdx == self.square.rowIdx + self.move_offset
        
    def __str__(self):
        return ' p' if self.color == WHITE else '*p'

    def __repr__(self):
        return 'p' + self.square.getCoord()
