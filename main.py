#!/usr/bin/python3

import PySimpleGUI as sg
from icons import *
from board import cBoard
from constants import *
from move import cMove
from game import cGame
from displayer import cDisplayer
from lib import *

# TO FIX
# - new game/clear board after selecting a piece
# - place empty square
#
# - en passant can stop check

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

# TODO - sliding pieces as first indexes in pieces list (after king)
def main():

    boardDisplay = [[sg.Button(image_data=empty_icon, button_color=(COLOR_BG_LIGHT_BASIC, COLOR_BG_LIGHT_BASIC) if (i+j) % 2 == 0 else (COLOR_BG_DARK_BASIC, COLOR_BG_DARK_BASIC), border_width=3, key='sqr'+str(i+(7-j)*8)) for i in range(8)] for j in range(8)]
    
    layout = boardDisplay
    
    white_icons = [white_pawn_icon, white_knight_icon, white_bishop_icon, white_rook_icon, white_queen_icon, white_king_icon, empty_icon]
    white_keys = ['new_wp', 'new_wn', 'new_wb', 'new_wr', 'new_wq', 'new_wk', 'new_empty']
    black_icons = [black_pawn_icon, black_knight_icon, black_bishop_icon, black_rook_icon, black_queen_icon, black_king_icon]
    black_keys = ['new_bp', 'new_bn', 'new_bb', 'new_br', 'new_bq', 'new_bk']
    
    layout += [[sg.Button(image_data=icon, key=key) for key, icon in zip(white_keys, white_icons)]]
    layout += [[sg.Button(image_data=icon, key=key) for key, icon in zip(black_keys, black_icons)]]
    
    layout.append([sg.Button('New game', key='new_game'),  sg.Button('Clear board', key='clear_board'), sg.Button('Exit', key='exit'), sg.Button('Generate', key='generate'), sg.Button('UNDO', key='unmove')])

    displayer = cDisplayer(boardDisplay)
    game = cGame(displayer)

    window = sg.Window('Welcome to chessify', layout, default_element_size=(12,1), element_padding=(1,1), return_keyboard_events=True)
    
    new_piece, selected_button = None, None
    potential_squares = []
    while True:
        event, values = window.read()

        if event in (None, 'exit'): 
            break
        elif event == 'unmove':
            game.undo_move()
        elif event == 'generate':
            game.generate_positions()
        elif event == 'new_game':
            game.displayer.unlight_squares()
            game.reset()
        elif event == 'clear_board':
            game.displayer.unlight_squares()
            game.clear()
        elif event[:4] == 'new_':
            new_piece = event[4:]
        elif event[:3] == 'sqr':
            event_sqr = int(event[3:])
            
            if new_piece is not None:
                color = WHITE if new_piece[0] == 'w' else BLACK
                kind = letter_to_piece(new_piece[1])
                game.place_piece(event_sqr, kind, color)
                new_piece = None
                continue
            
            if selected_button is None:
                if window.Element(event).ImageData != empty_icon:
                    if game.board.get_square_by_idx(event_sqr).piece.color == game.board.turn:
                        selected_button = event_sqr
                        potential_moves = game.board.get_square_by_idx(selected_button).piece.get_legal_moves()
                        potential_squares = list(map(lambda mv: mv.toSqr, potential_moves))
                        game.displayer.light_squares([game.board.get_square_by_idx(selected_button)], 2)
                        game.displayer.light_squares(potential_squares, 1)

            elif selected_button == event_sqr:
                game.displayer.unlight_squares()
                selected_button = None
            elif game.board.get_square_by_idx(event_sqr).piece and game.board.get_square_by_idx(selected_button).piece.color == game.board.get_square_by_idx(event_sqr).piece.color:
                game.displayer.unlight_squares()
                selected_button = event_sqr
                potential_moves = game.board.get_square_by_idx(selected_button).piece.get_legal_moves()
                potential_squares = list(map(lambda mv: mv.toSqr, potential_moves))
                game.displayer.light_squares([game.board.get_square_by_idx(selected_button)], 2)
                game.displayer.light_squares(potential_squares, 1)
            else:
                if not game.board.get_square_by_idx(event_sqr) in potential_squares:
                    continue
                   
                game.displayer.unlight_squares()
                #move = cMove(game.board.get_square_by_idx(selected_button).piece, game.board.get_square_by_idx(event_sqr)
                moves = list(filter(lambda x: x.piece == game.board.get_square_by_idx(selected_button).piece and x.toSqr == game.board.get_square_by_idx(event_sqr), potential_moves))
                if len(moves) > 0:
                    game.perform_move(moves[0])
                    selected_button = None

if __name__ == '__main__':
    main()
