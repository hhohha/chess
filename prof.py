#!/usr/bin/python3

from board import cBoard
from move import cMove
from constants import *
import cProfile

def main():
    board = cBoard()
    board.loadFEN('r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10')

    n = board.generate_successors(3)

    print('cnt:', n)


cProfile.run('main()')
#main()   #24sec
