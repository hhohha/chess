#!/usr/bin/python3

import PySimpleGUI as sg
from icons import *
from board import cBoard
from constants import *


def main():
    #board.loadFEN('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    #board.reset()
    #board.placePiece('a8', ROOK, WHITE)
    
    boardDisplay = [[sg.Button(image_data=empty_icon, button_color=('#FFBAB0', '#EDEAE0') if (i+j) % 2 == 0 else ('#FF9779', '#8F9779'), border_width=3, key='sqr'+str(i+(7-j)*8)) for i in range(8)] for j in range(8)]
    
    layout = boardDisplay
    layout.append([sg.Button('New game', key='new'), sg.Button('Exit', key='exit')])

    board = cBoard(boardDisplay)
    print(board)
    # Create the window and show it
    window = sg.Window('A Table Simulation', layout, default_element_size=(12,1), element_padding=(1,1), return_keyboard_events=True)

    selected_button = None  
    while True:
        event, values = window.read()

        if event in (None, 'exit'): 
            break
        elif event == 'new':
            board.reset()
        elif event[:3] == 'sqr':
            if selected_button == None:
                if window.Element(event).ImageData != empty_icon:
                    selected_button = event
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
