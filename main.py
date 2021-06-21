#!/usr/bin/python3

import PySimpleGUI as sg
from icons import *
from board import cBoard
from constants import *
from move import cMove
from displayer import cDisplayer
from lib import *

# TO FIX
# - new game/clear board after selecting a piece
# - place empty square

# RULES TO IMPLEMENT
# - draw by repetition
#
# UI FEATURES TO IMPLEMENT
# - display history
# - go back/forward in history
# - clock (less prio)
# - display coordinates
#
# OTHER IMPLEMENTATIONS
# - replace lists with other structures (sets) where appropriate
# - unit tests
# - consider some automatic tests
# - in color_pieces - first is always the king (instead of special variable)
#
# ENGINE IMPLAMENTATION
# - probably break cBoard to cGame and cPosition??
# - search (iterative deepening)
# - evaluate function
# - move ordering
# - alpha-beta pruning
# - reordering of search
# - search all captures
# - opening database
# - position maps
# - ...


def main():
    boardDisplay = [[sg.Button(image_data=empty_icon, button_color=(COLOR_BG_LIGHT_BASIC, COLOR_BG_LIGHT_BASIC) if (i+j) % 2 == 0 else (COLOR_BG_DARK_BASIC, COLOR_BG_DARK_BASIC), border_width=3, key='sqr'+str(i+(7-j)*8)) for i in range(8)] for j in range(8)]
    
    layout = boardDisplay
    layout.append([sg.Button('New game', key='new_game'),  sg.Button('Clear board', key='clear_board'), sg.Button('Exit', key='exit')])
    
    white_icons = [white_pawn_icon, white_knight_icon, white_bishop_icon, white_rook_icon, white_queen_icon, white_king_icon, empty_icon]
    white_keys = ['new_wp', 'new_wn', 'new_wb', 'new_wr', 'new_wq', 'new_wk', 'new_empty']
    black_icons = [black_pawn_icon, black_knight_icon, black_bishop_icon, black_rook_icon, black_queen_icon, black_king_icon]
    black_keys = ['new_bp', 'new_bn', 'new_bb', 'new_br', 'new_bq', 'new_bk']
    
    layout += [[sg.Button(image_data=icon, key=key) for key, icon in zip(white_keys, white_icons)]]
    layout += [[sg.Button(image_data=icon, key=key) for key, icon in zip(black_keys, black_icons)]]
    
    displayer = cDisplayer(boardDisplay)
    board = cBoard(displayer)

    window = sg.Window('Welcome to chessify', layout, default_element_size=(12,1), element_padding=(1,1), return_keyboard_events=True)
    
    new_piece, selected_button = None, None
    showing_attacking_pieces = False
    
    potential_squares = []
    while True:
        event, values = window.read()

        if event in (None, 'exit'): 
            break
        elif event == 'new_game':
            board.reset()
        elif event == 'clear_board':
            board.clear()
        elif event[:4] == 'new_':
            new_piece = event[4:]
        elif event[:3] == 'sqr':
            event_sqr = int(event[3:])
            
            if new_piece is not None:
                color = WHITE if new_piece[0] == 'w' else BLACK
                kind = letter_to_piece(new_piece[1])
                board.placePiece(event_sqr, kind, color)
                new_piece = None
                continue
            
            if selected_button is None:
                if window.Element(event).ImageData != empty_icon:
                    if board.getSquare(event_sqr).piece.color == board.turn:
                        selected_button = event_sqr
                        potential_moves = board.getSquare(selected_button).piece.get_legal_moves()
                        potential_squares = list(map(lambda mv: mv.toSqr, potential_moves))
                        board.displayer.light_squares([board.getSquare(selected_button)], 2)
                        board.displayer.light_squares(potential_squares, 1)

            elif selected_button == event_sqr:
                board.displayer.unlight_squares()
                selected_button = None
            elif board.getSquare(event_sqr).piece and board.getSquare(selected_button).piece.color == board.getSquare(event_sqr).piece.color:
                board.displayer.unlight_squares()
                selected_button = event_sqr
                potential_moves = board.getSquare(selected_button).piece.get_legal_moves()
                potential_squares = list(map(lambda mv: mv.toSqr, potential_moves))
                board.displayer.light_squares([board.getSquare(selected_button)], 2)
                board.displayer.light_squares(potential_squares, 1)
            else:
                if not board.getSquare(event_sqr) in potential_squares:
                    continue
                   
                board.displayer.unlight_squares()
                move = cMove(board.getSquare(selected_button).piece, board.getSquare(event_sqr))
                board.perform_move(move)
                selected_button = None

if __name__ == '__main__':
    main()
