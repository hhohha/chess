from constants import *
from icons import *
import PySimpleGUI as sg

class cDisplayer:
    def __init__(self, display):
        self.display = display
        self.lighted_squares = []
    
    def clear(self):
        for i in range(8):
            for j in range(8):
                if self.display[i][j].ImageData != empty_icon:
                    self.display[i][j].Update(image_data=empty_icon)
                    self.display[i][j].ImageData=empty_icon

    def load(self, board):
        self.clear()
        for sqr in board.squares:
            icon = self._get_icon(sqr.piece)
            self.display[7-sqr.rowIdx][sqr.colIdx].Update(image_data=icon)
            self.display[7-sqr.rowIdx][sqr.colIdx].ImageData = icon

    def draw_square(self, sqr, piece):
        icon = self._get_icon(piece)
        self.display[7-sqr.rowIdx][sqr.colIdx].Update(image_data=icon)
        self.display[7-sqr.rowIdx][sqr.colIdx].ImageData = icon
    
    def light_squares(self, squares, intensity=1):
        self.lighted_squares += squares
        for sqr in squares:
            color = self._get_color(sqr, intensity)
            self.display[7-sqr.rowIdx][sqr.colIdx].Update(button_color=color)
            
    def unlight_squares(self):
        self.light_squares(self.lighted_squares, 0)
        self.lighted_squares = []
    
    def _get_icon(self, piece):
        if piece is None:
            return empty_icon
        elif piece.color == WHITE:
            if piece.kind == PAWN:
                return white_pawn_icon
            elif piece.kind == KNIGHT:
                return white_knight_icon
            elif piece.kind == BISHOP:
                return white_bishop_icon
            elif piece.kind == ROOK:
                return white_rook_icon
            elif piece.kind == QUEEN:
                return white_queen_icon
            else:
                return white_king_icon
        else:
            if piece.kind == PAWN:
                return black_pawn_icon
            elif piece.kind == KNIGHT:
                return black_knight_icon
            elif piece.kind == BISHOP:
                return black_bishop_icon
            elif piece.kind == ROOK:
                return black_rook_icon
            elif piece.kind == QUEEN:
                return black_queen_icon
            else:
                return black_king_icon
    
    def _get_color(self, sqr, intensity):
        if (sqr.rowIdx + sqr.colIdx) % 2 == 0:
            #dark square
            if intensity == 0:
                return COLOR_BG_DARK_BASIC
            elif intensity == 1:
                return COLOR_BG_DARK_HLIGHTED_1
            elif intensity == 2:
                return COLOR_BG_DARK_HLIGHTED_2
        else:
            #light square
            if intensity == 0:
                return COLOR_BG_LIGHT_BASIC
            elif intensity == 1:
                return COLOR_BG_LIGHT_HLIGHTED_1
            elif intensity == 2:
                return COLOR_BG_LIGHT_HLIGHTED_2

    def get_promoted_piece_from_dialog(self):
        promote_window = sg.Window('what piece do you want', [[sg.Button('Queen'), sg.Button('Rook'), sg.Button('Bishop'), sg.Button('Knight')]])
        piece, _  = promote_window.read()
        promote_window.close()
        if piece == 'Queen':
            return QUEEN
        elif piece == 'Rook':
            return ROOK
        elif piece == 'Bishop':
            return BISHOP
        else:
            return KNIGHT
        
    def inform(self, msg):
        sg.popup(msg)
