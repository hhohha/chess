#!/usr/bin/python3

import PySimpleGUI as sg
from icons import *
from board import cBoard
from constants import *


def main():
    #board.loadFEN('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    #board.reset()
    #board.placePiece('a8', ROOK, WHITE)
    
    boardDisplay = [[sg.Button(image_data=empty_icon, button_color=(COLOR_BG_LIGHT_SELECTED, COLOR_BG_LIGHT_BASIC) if (i+j) % 2 == 0 else (COLOR_BG_DARK_SELECTED, COLOR_BG_DARK_BASIC), border_width=3, key='sqr'+str(i+(7-j)*8)) for i in range(8)] for j in range(8)]
    
    layout = boardDisplay
    layout.append([sg.Button('New game', key='new'), sg.Button('Exit', key='exit'), sg.Button('Test', key='test')])

    board = cBoard(boardDisplay)
    print(board)
    # Create the window and show it
    window = sg.Window('A Table Simulation', layout, default_element_size=(12,1), element_padding=(1,1), return_keyboard_events=True)

    selected_button = None  
    while True:
        event, values = window.read()

        if event in (None, 'exit'): 
            break
        elif event == 'test':
            #window.Element('sqr30').Update(button_color=('#000000', '#FF00FF'))
            window.Element('sqr30').Update(button_color='#FF00FF')
            window.Element('sqr30').Update(mouseover_colors='#0000FF')
            window.Element('sqr30').ButtonColor = ('#00FFFF', '#FF00FF')
            window.Refresh()
        elif event == 'new':
            board.reset()
            #board.clear()
            #board.placePiece('d3', ROOK, BLACK)
        elif event[:3] == 'sqr':
            board.unhighlightSquares()
            if selected_button == None:
                if window.Element(event).ImageData != empty_icon:
                    selected_button = event
                    potentialMoves = board.getSquare(int(selected_button[3:])).piece.getPotentialMoves()
                    
                    print(list(map(lambda x: x.getCoord(), potentialMoves)))
                    board.highlightSquares(potentialMoves)
                    
            else:
                board.move((int(selected_button[3:]), int(event[3:])))
                print (board)
                #data = window.Element(selected_button).ImageData
                #window.Element(event).ImageData = data
                #window.Element(event).Update(image_data=data)
                
                #window.Element(selected_button).ImageData = empty_icon
                #window.Element(selected_button).Update(image_data=empty_icon)
                
                selected_button = None
        
        
        
    #current_cell = window.find_element_with_focus().Key
    #r,c = current_cell
    ## Process arrow keys
    #if event.startswith('Down'):
        #r = r + 1 * (r < MAX_ROWS-1)
    #if event.startswith('Left'):
        #c = c - 1 *(c > 0)
    #if event.startswith('Right'):
        #c = c + 1 *(c < MAX_COLS-1)
    #if event.startswith('Up'):
        #r = r - 1 * (r > 0)
    ## if the current cell changed, set focus on new cell
    #if current_cell != (r,c):
      #current_cell = r,c
      #window[current_cell].set_focus()              # set the focus on the element moved to
      #window[current_cell].update(select=True)      # when setting focus, also highlight the data in the element so typing overwrites

if __name__ == '__main__':
    main()
