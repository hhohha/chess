import unittest
from board import Board
from constants import PieceType, Color
from unit_tests.testing_utils import compare_moves

class TestSuite_BishopMoves(unittest.TestCase):
    def test_bishop(self):
        b = Board()
        b.place_piece('a1', PieceType.BISHOP, Color.WHITE)
        bishop = b.get_square('a1').piece
        moves = bishop.calc_potential_moves()

        expectedMoves = ['Ba1-h8', 'Ba1-g7', 'Ba1-f6', 'Ba1-e5', 'Ba1-d4', 'Ba1-c3', 'Ba1-b2']

        self.assertEqual(set(map(str, moves)), set(expectedMoves))
        #assert compare_moves(moves, ['Ba1-h8', 'Ba1-g7', 'Ba1-f6', 'Ba1-e5', 'Ba1-d4', 'Ba1-c3', 'Ba1-b2 '])

    def test_bishop2(self):
        b = Board()
        b.place_piece('b1', PieceType.BISHOP, Color.WHITE)
        bishop = b.get_square('b1').piece
        moves = bishop.calc_potential_moves()

        assert compare_moves(moves, ['Bb1-a2', 'Bb1-c2', 'Bb1-d3', 'Bb1-e4', 'Bb1-f5', 'Bb1-g6', 'Bb1-h7'])