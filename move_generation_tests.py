#!/usr/bin/python3

from board import cBoard
from move import cMove
from constants import *
import sys


class cPosition:
    def __init__(self, id, position, ref):
        self.id = id
        self.position = position
        self.reference = ref

positions = []
positions.append(cPosition(1, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0', [1, 20, 400, 8902, 197281, 4865609, 119060324]))
positions.append(cPosition(2, 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0', [1, 48, 2039, 97862, 4085603, 193690690, 8031647685]))
positions.append(cPosition(3, '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0', [1, 14, 191, 2812, 43238, 674624, 11030083]))
positions.append(cPosition(4, 'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1', [1, 6, 264, 9467, 422333, 15833292, 706045033]))
positions.append(cPosition(5, 'r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1', [1, 6, 264, 9467, 422333, 15833292, 706045033]))
positions.append(cPosition(6, 'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8', [1, 44, 1486, 62379, 2103487, 89941194, 0]))
positions.append(cPosition(7, 'r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10', [1, 46, 2079, 89890, 3894594, 164075551, 6923051137]))

def test_position(position, depth):

    for dpt in range(1, depth + 1):
        board = cBoard()
        board.loadFEN(position.position)
        result = board.generate_successors(dpt)
        print ('TESTING position ' + str(position.id) + ' to depth ' + str(dpt), ':    ', end='')
        if result == position.reference[dpt]:
            print(COLOR_GREEN + 'OK' + COLOR_WHITE)
        else:
            print(COLOR_RED + 'FAILED' + COLOR_WHITE)


depth = int(sys.argv[1])
for p in positions:
    test_position(p, depth)



