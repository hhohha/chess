#!/usr/bin/python3

import PySimpleGUI as sg
from icons import *
from board import cBoard
from constants import *
from lib import *

import inspect

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
    
    #debug buttons
    layout += [[
        sg.Button('Is white in check', key='is_white_checked'),
        sg.Button('Is black in check', key='is_black_checked'),
        sg.Button('Show white pinned', key='show_white_pinned'),
        sg.Button('Show black pinned', key='show_black_pinned'),
        sg.Button('Show attacking pieces', key='show_attacking_pieces')
    ]]
               
    board = cBoard(boardDisplay)

    # Create the window and show it
    window = sg.Window('Welcome to chessify', layout, default_element_size=(12,1), element_padding=(1,1), return_keyboard_events=True)

    new_piece, selected_button = None, None
    showing_attacking_pieces = False
    
    potential_squares = []
    while True:
        event, values = window.read()

        if event in (None, 'exit'): 
            break
        elif event == 'show_attacking_pieces':
            showing_attacking_pieces = not showing_attacking_pieces
        elif event == 'is_white_checked':
            print(board.is_in_check(WHITE))
        elif event == 'is_black_checked':
            print(board.is_in_check(BLACK))
        elif event == 'new_game':
            board.reset()
        elif event == 'clear_board':
            board.clear()
        elif event[:4] == 'new_':
            new_piece = event[4:]
        elif event[:3] == 'sqr':
            if showing_attacking_pieces:
                lst = board.getSquare(int(event[3:])).attacked_by_whites
                print('whites:', list(map(lambda x: x.pprint(), lst)))
                lst = board.getSquare(int(event[3:])).attacked_by_blacks
                print('blacks:', list(map(lambda x: x.pprint(), lst)))
                continue
            
            if new_piece != None:
                color = WHITE if new_piece[0] == 'w' else BLACK
                kind = letter_to_piece(new_piece[1])
                board.placePiece(int(event[3:]), kind, color)
                new_piece = None
                continue
            
            if selected_button == None:
                if window.Element(event).ImageData != empty_icon:
                    if board.getSquare(int(event[3:])).piece.color == board.turn:
                        selected_button = event
                        potential_moves = board.getSquare(int(selected_button[3:])).piece.get_legal_moves()
                        potential_squares = list(map(lambda mv: mv.toSqr, potential_moves))
                        board.displayer.light_squares([board.getSquare(int(selected_button[3:]))], 2)
                        board.displayer.light_squares(potential_squares, 1)

            elif selected_button == event:
                board.displayer.unlight_squares()
                selected_button = None
            else:
                if not board.getSquare(int(event[3:])) in potential_squares:
                    continue
                   
                board.displayer.unlight_squares()
                board.move((int(selected_button[3:]), int(event[3:])))
                selected_button = None

if __name__ == '__main__':
    main()
