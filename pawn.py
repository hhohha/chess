from piece import cPieceNotSliding
from move import cMove
from constants import *

class cPawn (cPieceNotSliding):
    def __init__(self, color, square):
        super().__init__(PAWN, color, square)
        self.is_light = False
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

    def update_attacked_squares(self):
        for sqr in self.get_attacked_squares():
            sqr.get_attacked_by(self.color).remove(self)

        self.set_attacked_squares(list(self.calc_attacked_squares()))

        for sqr in self.get_attacked_squares():
            sqr.get_attacked_by(self.color).add(self)

    def calc_potential_moves(self):
        yield from self.get_forward_moves()
        yield from self.get_capture_move(1)
        yield from self.get_capture_move(-1)
        
        en_passant = self.square.board.en_passant
        if en_passant is not None and self.square.rowIdx == self.en_passant_row and abs(self.square.idx - en_passant.idx) == 1 and not self.is_en_passant_pin(en_passant):
            yield cMove(self, self.square.board.get_square_by_coords(en_passant.rowIdx + self.move_offset, en_passant.colIdx), isEnPassant=True)
    
    def calc_potential_moves_pinned(self, direction):
        if direction == RIGHT or direction == LEFT:
            return
        elif direction == UP or direction == DOWN:
            yield from self.get_forward_moves()
        elif direction == UP_RIGHT or direction == DOWN_LEFT:
            yield from self.get_capture_move(self.move_offset)

            en_passant = self.square.board.en_passant
            if en_passant is not None and self.square.rowIdx == self.en_passant_row and en_passant.idx - self.square.idx == self.move_offset and not self.is_en_passant_pin(en_passant):
                yield cMove(self, self.square.board.get_square_by_coords(en_passant.rowIdx + self.move_offset, en_passant.colIdx), isEnPassant=True)
        else: # direction is LEFT_UP or RIGHT_DOWN
            yield from self.get_capture_move(-self.move_offset)
            en_passant = self.square.board.en_passant
            if en_passant is not None and self.square.rowIdx == self.en_passant_row and self.square.idx - en_passant.idx == self.move_offset and not self.is_en_passant_pin(en_passant):
                yield cMove(self, self.square.board.get_square_by_coords(en_passant.rowIdx + self.move_offset, en_passant.colIdx), isEnPassant=True)

    def get_forward_moves(self):
        # check the square in front of the pawn
        square = self.square.board.get_square_by_coords(self.square.rowIdx + self.move_offset, self.square.colIdx)
        if square.piece is None:
            yield from self.generate_pawn_move(square)

            # if on the base row, check one square further
            if self.square.rowIdx == self.base_row:
                square = self.square.board.get_square_by_coords(self.square.rowIdx + 2*self.move_offset, self.square.colIdx)
                if square.piece is None:
                    yield cMove(self, square)

    def get_capture_move(self, column_offest):
        square = self.square.board.get_square_by_coords(self.square.rowIdx + self.move_offset, self.square.colIdx + column_offest)
        if square is not None and square.piece is not None and square.piece.color != self.color:
            yield from self.generate_pawn_move(square)

    def generate_pawn_move(self, square):
        if square.rowIdx != self.promote_row:
            yield cMove(self, square)
        else:
            for newPiece in [KNIGHT, BISHOP, ROOK, QUEEN]:
                yield cMove(self, square, newPiece, isPromotion=True)
    
    def calc_attacked_squares(self):
        for i in [1, -1]:
            square = self.square.board.get_square_by_coords(self.square.rowIdx + self.move_offset, self.square.colIdx + i)
            if square is not None:
                yield square
        
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
