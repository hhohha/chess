from board import cBoard
from constants import *
from copy import deepcopy

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
            if self.is_in_check(self.turn):
                if self.turn == WHITE:
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
        fromSqr, toSqr, movPiece = move.fromSqr, move.toSqr, move.piece
        
        if move.is_promotion():
            move.newPiece = self.displayer.get_promoted_piece_from_dialog()
            #self.displayer.draw_square(toSqr, movPiece)

        if move.is_en_passant():
            self.displayer.draw_square(self.board.en_passant, None)

        self.board.perform_move(move)
        self.displayer.draw_square(fromSqr, None)
        self.displayer.draw_square(toSqr, toSqr.piece)
        
        if move.is_castling():
            if toSqr.idx == 6:
                rookFromIdx, rookToIdx = 7, 5
            elif toSqr.idx == 2:
                rookFromIdx, rookToIdx = 0, 3
            elif toSqr.idx == 62:
                rookFromIdx, rookToIdx = 63, 61
            else:
                rookFromIdx, rookToIdx = 56, 59

            rookFromSqr = movPiece.square.board.getSquare(rookFromIdx)
            rookToSqr = movPiece.square.board.getSquare(rookToIdx)
            self.displayer.draw_square(rookFromSqr, None)
            self.displayer.draw_square(rookToSqr, rookToSqr.piece)

        self.history.append(move)
        self.legal_moves = self.board.legal_moves

    def generate_positions(self, board):

        positions = []
        for move in board.get_all_moves():
            print('moving', move)
            #b = deepcopy(board)
            b = cBoard()
            b.load_position(board)
            b.perform_move(move)
            positions.append(b)
        return positions
