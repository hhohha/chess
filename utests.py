#!/usr/bin/python3

from constants import *
from board import cBoard
from square import cSquare
import unittest

class dummyDisplayer:
    def __init__(self):
        pass
    def clear(self):
        pass
    def draw_square(self, s, p):
        pass
    def light_squares(self, s, i=1):
        pass
    def unlight_squares(self):
        pass
    def get_promoted_piece_from_diag(self):
        return QUEEN

class TestStringMethods(unittest.TestCase):
    def test_start_position(self):
        board = cBoard(dummyDisplayer())
        board.loadFEN(FEN_INIT)
        self.assertEqual(len(board.white_pieces), 16)
        self.assertEqual(len(board.black_pieces), 16)


if __name__ == '__main__':
    unittest.main()
