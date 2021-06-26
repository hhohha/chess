#!/usr/bin/python3

from board import cBoard
from constants import *
import cProfile

def main():
    board = cBoard()
    board.loadFEN(FEN_INIT)

    print(board.generate_successors(2))


cProfile.run('main()')

main()
