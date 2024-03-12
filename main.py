#!/usr/bin/python3
from typing import Optional, List, Iterable

import PySimpleGUI as sg
import icons
from constants import *
from display_handler import DisplayHandler
from engine_protocol import EngineProtocol

from game import Game
from square import Square
from utils import letterToPiece


# C++ methods of board functions to be callable:
# - reset
# - clear
# - place_piece
# - remove_piece
# - load fen
# - move
# - undo move
# - play move
# - get possible target squares of a piece

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
                sg.Button('Undo', key='unmove'),
                sg.Button('Move', key='move')]]
              )

    game = Game(DisplayHandler(boardLayout), EngineProtocol())

    window = sg.Window('Welcome to chessify', layout, default_element_size=(12,1), element_padding=(1,1), return_keyboard_events=True)


    newPieceName: Optional[str] = None
    squareIdxWithPieceToMove: Optional[int] = None
    possibleSquares: Iterable[Square] = []
    while True:
        event, values = window.read()

        if event in (None, 'exit'): 
            break
        elif event == 'unmove':
            game.undo_move()
        elif event == 'new_game':
            game.reset()
        elif event == 'clear_board':
            game.clear()
        elif event[:4] == 'new_':
            newPieceName = event[4:]
        elif event[:3] == 'sqr': # click on a square
            boardSquareClickedIdx = int(event[3:])
            assert 0 <= boardSquareClickedIdx < 64, f"clicked invalid square with index = {boardSquareClickedIdx}"
            sqrClicked = game.squares[boardSquareClickedIdx]

            # we are not moving but placing a new piece on the board
            if newPieceName is not None:
                color = Color.WHITE if newPieceName[0] == 'w' else Color.BLACK
                kind = letterToPiece[newPieceName[1]]
                game.place_piece(boardSquareClickedIdx, kind, color)
                newPieceName = None

            # no piece is selected to be moved - we are selecting one
            elif squareIdxWithPieceToMove is None and sqrClicked.piece and sqrClicked.piece.color == game.turn:
                squareIdxWithPieceToMove = boardSquareClickedIdx

                #now light up the possible destination squares
                possibleSquares = game.get_possible_target_squares(sqrClicked)
                game.displayHandler.light_squares([sqrClicked], 2)
                game.displayHandler.light_squares(possibleSquares, 1)

            # clicked the same button twice - just unselect the piece and unlight potential moves
            elif squareIdxWithPieceToMove == boardSquareClickedIdx:
                game.displayHandler.unlight_squares()
                squareIdxWithPieceToMove = None

            # we clicked on a different piece of the same color - select it instead
            elif sqrClicked.piece and sqrClicked.piece.color == game.turn:
                game.displayHandler.unlight_squares()
                squareIdxWithPieceToMove = boardSquareClickedIdx

                possibleSquares = game.get_possible_target_squares(sqrClicked)
                game.displayHandler.light_squares([sqrClicked], 2)
                game.displayHandler.light_squares(possibleSquares, 1)

            # clicked on a square where the selected piece can move - let's move the piece
            elif sqrClicked in game.get_possible_target_squares(game.squares[squareIdxWithPieceToMove]):
                game.displayHandler.unlight_squares()
                game.perform_move(game.make_move(squareIdxWithPieceToMove, boardSquareClickedIdx))
                squareIdxWithPieceToMove = None

            # only other possibility - clicked on a square where the selected piece cannot move - do nothing
            else:
                pass

    window.close()

if __name__ == '__main__':
    main()
