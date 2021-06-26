from board import cBoard
from constants import *
from copy import deepcopy
import sys

class cGame:
    def __init__(self, display):
        self.history = []
        self.displayer = display
        self.legal_moves = []
        self.board = cBoard()
        
    def place_piece(self, sqr, kind, color):
        self.board.place_piece(sqr, kind, color)
        self.displayer.draw_square(square, square.piece)
        
    def remove_piece(self, piece, display=False):
        self.board.remove_piece(piece)
        if display:
            self.displayer.draw_square(piece.square, None)
        
    def reset(self):
        self.board.loadFEN(FEN_INIT)
        self.displayer.load(self.board)
        
    def clear(self):
        self.board.clear()
        self.displayer.load(self.board)

    def check_game_end(self):
        if len(self.legal_moves) == 0:
            if self.board.is_in_check(self.board.turn):
                if self.board.turn == WHITE:
                    self.displayer.inform(GAME_WON_BLACK)
                else:
                    self.displayer.inform(GAME_WON_WHITE)
            else:
                self.displayer.inform(GAME_DRAW_STALEMATE)

            return
        
        pieces = self.board.get_pieces()
        if len(pieces) == 2 or (len(pieces) == 3 and any(map(lambda p: p.is_light(), pieces))):
            self.displayer.inform(GAME_DRAW_MATERIAL)
            
        if self.board.half_moves == 100:
            self.displayer.inform(GAME_DRAW_50_MOVES)

    def perform_move(self, move):
        if move.is_promotion():
            move.newPiece = self.displayer.get_promoted_piece_from_dialog()
            #self.displayer.draw_square(toSqr, movPiece)

        # is en passant?
        if move.piece == PAWN and (move.fromSqr + move.toSqr) & 1 == 1 and self.board.getSquare(move.toSqr).piece is None:
            # if sum of to and from indexes is odd, the piece must be moving across columns (pawn takes)
            self.displayer.draw_square(self.board.en_passant, None)

        self.board.perform_move(move)
        self.displayer.draw_square(self.board.getSquare(move.fromSqr), None)
        self.displayer.draw_square(self.board.getSquare(move.toSqr), self.board.getSquare(move.toSqr).piece)
        
        if move.is_castling():
            if move.toSqr == 6:
                rookFromIdx, rookToIdx = 7, 5
            elif move.toSqr == 2:
                rookFromIdx, rookToIdx = 0, 3
            elif move.toSqr == 62:
                rookFromIdx, rookToIdx = 63, 61
            else:
                rookFromIdx, rookToIdx = 56, 59

            rookFromSqr = self.board.getSquare(rookFromIdx)
            rookToSqr = self.board.getSquare(rookToIdx)
            self.displayer.draw_square(rookFromSqr, None)
            self.displayer.draw_square(rookToSqr, rookToSqr.piece)

        self.history.append(move)
        self.legal_moves = self.board.legal_moves
        self.check_game_end()

