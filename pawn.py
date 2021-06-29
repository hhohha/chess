from piece import cPiece
from move import cMove
from constants import *

class cPawn (cPiece):
    def __init__(self, color, square):
        super().__init__(PAWN, color, square)
        if self.color == WHITE:
            self.move_offset = 1
            self.base_row = 1
            self.promote_row = 7
            self.en_passant_row = 4
        else:
            self.move_offset = -1
            self.base_row = 6
            self.promote_row = 0
            self.en_passant_row = 3
        
    def get_potential_moves(self):
        moves = self.get_moves_forward()
                    
        for i in [1, -1]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + self.move_offset, self.square.colIdx + i)
            if square is not None and square.piece is not None and square.piece.color != self.color:
                moves += self.generate_pawn_move(square)
        
        en_passant = self.square.board.en_passant
        if self.can_capture_en_passant():
            moves.append(cMove(self, self.square.board.get_square_by_coords(en_passant.rowIdx + self.move_offset, en_passant.colIdx), isEnPassant=True))
        
        return moves
    
    def can_capture_en_passant(self):
        en_passant = self.square.board.en_passant
        return en_passant is not None and self.square.rowIdx == self.en_passant_row and abs(self.square.idx - en_passant.idx) == 1 and not self.is_en_passant_pin(en_passant)

    def get_moves_forward(self):
        moves = []

        # check the square in front of the pawn
        square = self.square.board.get_square_by_coords(self.square.rowIdx + self.move_offset, self.square.colIdx)
        if square.piece is None:
            moves += self.generate_pawn_move(square)
            # if on the base row, check one square further
            if self.square.rowIdx == self.base_row:
                square = self.square.board.get_square_by_coords(self.square.rowIdx + 2*self.move_offset, self.square.colIdx)
                if square.piece is None:
                    moves.append(cMove(self, square))
        return moves


    def get_potential_moves_pinned(self, direction):
        if direction == RIGHT or direction == LEFT:
            return []

        if direction == UP or direction == DOWN:
            return self.get_moves_forward()

        if direction == UP_RIGHT or direction == DOWN_LEFT:
            sqr = self.square.board.get_square_by_coords(self.square.rowIdx + self.move_offset, self.square.colIdx + self.move_offset)
            if sqr is not None and sqr.piece is not None and sqr.piece.color != self.color:
                return [cMove(self, sqr)]
            else:
                return []
        
        # direction is LEFT_UP or RIGHT_DOWN
        sqr = self.square.board.get_square_by_coords(self.square.rowIdx + self.move_offset, self.square.colIdx - self.move_offset)
        if sqr is not None and sqr.piece is not None and sqr.piece.color != self.color:
            return [cMove(self, sqr)]
        else:
            return []

    def generate_pawn_move(self, square):
        if square.rowIdx != self.promote_row:
            return [cMove(self, square)]
        else:
            return [cMove(self, square, KNIGHT, isPromotion=True), cMove(self, square, BISHOP, isPromotion=True), cMove(self, square, ROOK, isPromotion=True), cMove(self, square, QUEEN, isPromotion=True)]
    
    def getAttackedSquares(self):
        resLst = []

        for i in [1, -1]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + self.move_offset, self.square.colIdx + i)
            if square is not None:
                resLst.append(square)

        return resLst
    
    #def isAttackingSqr(self, colIdx, rowIdx):
        #return abs(colIdx - self.square.colIdx) == 1 and rowIdx == self.square.rowIdx + self.move_offset
        
    def is_en_passant_pin(self, en_passant):
        kingSqr = self.square.board.get_king_sqr(self.color)
        if kingSqr.rowIdx != en_passant.rowIdx:
            return False
        
        direction = LEFT if kingSqr.colIdx > en_passant.colIdx else RIGHT
        firstSquare = self.square.board.find_first_piece_in_dir(kingSqr, direction)
        
        if firstSquare is None or (firstSquare != en_passant and firstSquare.piece != self):
            return False
        
        secondSquare = self.square.board.get_square_by_coords(firstSquare.rowIdx, firstSquare.colIdx + (1 if direction == RIGHT else -1))
        if secondSquare is None or secondSquare.piece is None:
            return False
        
        if not (firstSquare == en_passant and secondSquare.piece == self or firstSquare.piece == self and secondSquare == en_passant):
            return False
        
        thirdSquare = self.square.board.find_first_piece_in_dir(secondSquare, direction)
        
        if thirdSquare is None or thirdSquare.piece.color == self.color or thirdSquare.piece.kind not in [QUEEN, ROOK]:
            return False
        
        return True
        
    
        
    
    def __str__(self):
        return 'p' + self.square.getCoord()

    def __repr__(self):
        return 'p' + self.square.getCoord()
