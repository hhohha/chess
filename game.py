from board import Board
from constants import *
from copy import deepcopy
import sys

# TODO - refactor

class Game:
    def __init__(self, display):
        self.history = []
        self.displayHandler = display
        self.legal_moves = []
        self.board = Board()
        
    def place_piece(self, sqr, kind, color):
        self.board.place_piece(sqr, kind, color)
        self.displayer.draw_square(sqr, sqr.piece)
        
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
        if len(pieces) == 2 or (len(pieces) == 3 and any(map(lambda p: p.is_light, pieces))):
            self.displayer.inform(GAME_DRAW_MATERIAL)
            
        if self.board.half_moves == 100:
            self.displayer.inform(GAME_DRAW_50_MOVES)

    def undo_move(self):
        if len(self.history) == 0:
            return
        move = self.history.pop()

        self.board.undo_move(move)
        self.displayer.load(self.board)
        self.legal_moves = self.board.legal_moves[-1]

    def perform_move(self, move):
        if move.isPromotion:
            move.newPiece = self.displayer.get_promoted_piece_from_dialog()

        self.board.perform_move(move)
        self.displayer.load(self.board)
        self.history.append(move)
        self.legal_moves = self.board.legal_moves[-1]
        self.check_game_end()

