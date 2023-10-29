#!/usr/bin/pypy3

from board import Board
from constants import *
import sys
from time import time

# TODO - refactor


class Position:
    def __init__(self, id, position, ref):
        self.id = id
        self.position = position
        self.ref = ref

positions = []

positions.append(Position(1, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0', [1, 20, 400, 8902, 197281, 4865609, 119060324]))# FEN_INIT
positions.append(Position(2, 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0', [1, 48, 2039, 97862, 4085603, 193690690, 8031647685]))# FEN_E
positions.append(Position(3, '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0', [1, 14, 191, 2812, 43238, 674624, 11030083]))# FEN_C
positions.append(Position(4, 'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1', [1, 6, 264, 9467, 422333, 15833292, 706045033]))# FEN_D
positions.append(Position(5, 'r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1', [1, 6, 264, 9467, 422333, 15833292, 706045033]))# inverted FEN_D
positions.append(Position(6, 'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8', [1, 44, 1486, 62379, 2103487, 89941194, 0]))# FEN_B
positions.append(Position(7, 'r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10', [1, 46, 2079, 89890, 3894594, 164075551, 6923051137]))# FEN_F

def test_position(position: Position, depth: int) -> None:
    for dpt in range(2, depth + 1):
        board = Board()
        board.load_FEN(position.position)
        print ('TESTING position ' + str(position.id) + ' to depth ' + str(dpt), ':    ', end='')

        start_time = time()
        result = board.generate_successors(dpt)
        end_time = time()

        if result == position.ref[dpt]:
            print(COLOR_GREEN + 'OK' + COLOR_WHITE, '                         time: ', round(end_time - start_time, 4), 'sec')
        else:
            print(COLOR_RED + 'FAILED' + COLOR_WHITE + '  expected number: ' + str(position.ref[dpt]), '  but got: ' + str(result), '                         time: ', round(end_time - start_time, 4), 'sec')
            break

def main():
    depthArg = 3
    #depthArg = int(sys.argv[1])

    total_start = time()
    for p in positions:
        if p.id == 2:
            test_position(p, depthArg)

    total_end = time()
    print('total time needed:  ', round(total_end - total_start, 4), 'sec')

if __name__ == '__main__':
    main()

