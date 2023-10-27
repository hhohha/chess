#!/usr/bin/python3
from typing import Optional

import PySimpleGUI as sg
import icons
from constants import *
from display_handler import DisplayHandler

from game import Game
from move import Move
from utils import letterToPiece


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
# - create Move object from string
#
# ENGINE IMPLEMENTATION
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
    boardLayout = [[
        sg.Button(image_data=icons.empty,
                  button_color=(COLOR_BG_LIGHT_BASIC, COLOR_BG_LIGHT_BASIC) if (i+j) % 2 == 0 else (COLOR_BG_DARK_BASIC, COLOR_BG_DARK_BASIC),
                  border_width=3,
                  key='sqr'+str(i+(7-j)*8))
                  for i in range(8)
            ] for j in range(8)]
    
    white_icons = [icons.whitePawn, icons.whiteKnight, icons.whiteBishop, icons.whiteRook, icons.whiteQueen, icons.whiteKing, icons.empty]
    white_keys = ['new_wp', 'new_wn', 'new_wb', 'new_wr', 'new_wq', 'new_wk', 'new_empty']
    black_icons = [icons.blackPawn, icons.blackKnight, icons.blackBishop, icons.blackRook, icons.blackQueen, icons.blackKing]
    black_keys = ['new_bp', 'new_bn', 'new_bb', 'new_br', 'new_bq', 'new_bk']

    layout = (boardLayout +
              [[sg.Button(image_data=icon, key=key) for key, icon in zip(white_keys, white_icons)]] +
              [[sg.Button(image_data=icon, key=key) for key, icon in zip(black_keys, black_icons)]] +
              [[sg.Button('New game', key='new_game'),
                sg.Button('Clear board', key='clear_board'),
                sg.Button('Exit', key='exit'),
                sg.Button('UNDO', key='unmove')]]
              )

    displayHandler = DisplayHandler(boardLayout)
    game = Game(displayHandler)

    window = sg.Window('Welcome to chessify', layout, default_element_size=(12,1), element_padding=(1,1), return_keyboard_events=True)
    
    newPiece: Optional[str] = None
    selectedButton = None
    potentialSquares = []
    while True:
        event, values = window.read()

        if event in (None, 'exit'): 
            break
        elif event == 'unmove':
            game.undo_move()
        elif event == 'new_game':
            game.displayHandler.unlight_squares()
            game.reset()
        elif event == 'clear_board':
            game.displayHandler.unlight_squares()
            game.clear()
        elif event[:4] == 'new_':
            newPiece = event[4:]
        elif event[:3] == 'sqr': # click on a square
            eventSqr = int(event[3:])

            # we are not moving but placing a new piece on the board
            if newPiece is not None:
                color = Color.WHITE if newPiece[0] == 'w' else Color.BLACK
                kind = letterToPiece[newPiece[1]]
                game.place_piece(eventSqr, kind, color)
                newPiece = None
            
            elif selectedButton is None:
                # selected button is None - we are selecting a piece to be moved
                if window.Element(event).ImageData != icons.empty:  # there must be a piece on the square...
                    if game.board.get_square_by_idx_opt(eventSqr).piece.color == game.board.turn:  # ...of the color whose turn it is
                        selectedButton = eventSqr

                        #now light up the possible destination squares
                        potentialMoves = game.board.get_square_by_idx_opt(selectedButton).piece.get_legal_moves()
                        potentialSquares = list(map(lambda mv: mv.toSqr, potentialMoves))
                        game.displayHandler.light_squares([game.board.get_square_by_idx_opt(selectedButton)], 2)
                        game.displayHandler.light_squares(potentialSquares, 1)

            elif selectedButton == eventSqr:
                # clicked the same button twice - just unselect the piece - unlight potential moves
                game.displayHandler.unlight_squares()
                selectedButton = None

            elif game.board.get_square_by_idx_opt(eventSqr).piece and game.board.get_square_by_idx_opt(selectedButton).piece.color == game.board.get_square_by_idx_opt(eventSqr).piece.color:
                # we clicked on a different piece of the same color - select it instead
                game.displayHandler.unlight_squares()
                selectedButton = eventSqr
                potentialMoves = game.board.get_square_by_idx_opt(selectedButton).piece.get_legal_moves()
                potentialSquares = list(map(lambda mv: mv.toSqr, potentialMoves))
                game.displayHandler.light_squares([game.board.get_square_by_idx_opt(selectedButton)], 2)
                game.displayHandler.light_squares(potentialSquares, 1)
            elif game.board.get_square_by_idx_opt(eventSqr) in potentialSquares:
                # clicked on a square where the selected piece can move - let's move the piece
                game.displayHandler.unlight_squares()
                move = Move(game.board.get_square_by_idx(selectedButton).piece, game.board.get_square_by_idx(eventSqr))
                game.perform_move(move)
                selectedButton = None
            else:
                # only other possibility - clicked on a square where the selected piece cannot move - do nothing
                pass

    window.close()

if __name__ == '__main__':
    main()
