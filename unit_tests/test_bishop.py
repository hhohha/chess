import unittest
from board import Board
from constants import PieceType, Color, Direction


class TestSuite_BishopMoves(unittest.TestCase):
    def test_bishop_moves_1(self):
        """bishop's moves on an empty board"""

        b = Board()
        bishop = b.place_piece('a1', PieceType.BISHOP, Color.WHITE)
        actualMoves = bishop.calc_potential_moves()
        expectedMoves = ['Ba1-h8', 'Ba1-g7', 'Ba1-f6', 'Ba1-e5', 'Ba1-d4', 'Ba1-c3', 'Ba1-b2']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        bishop = b.place_piece('b1', PieceType.BISHOP, Color.WHITE)
        actualMoves = bishop.calc_potential_moves()
        expectedMoves =  ['Bb1-a2', 'Bb1-c2', 'Bb1-d3', 'Bb1-e4', 'Bb1-f5', 'Bb1-g6', 'Bb1-h7']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        bishop = b.place_piece('f4', PieceType.BISHOP, Color.BLACK)
        actualMoves = bishop.calc_potential_moves()
        expectedMoves =  ['Bf4-e3', 'Bf4-d2', 'Bf4-c1', 'Bf4-g5', 'Bf4-h6', 'Bf4-g3', 'Bf4-h2', 'Bf4-e5', 'Bf4-d6', 'Bf4-c7', 'Bf4-b8']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_bishop_moves_2(self):
        """bishop's moves on a non-empty board"""

        b = Board()
        b.place_piece('a1', PieceType.KNIGHT, Color.WHITE)
        b.place_piece('c3', PieceType.ROOK, Color.BLACK)
        bishop = b.place_piece('b2', PieceType.BISHOP, Color.WHITE)
        actualMoves = bishop.calc_potential_moves()
        expectedMoves =  ['Bb2-c3', 'Bb2-a3', 'Bb2-c1']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        for square in ['c4', 'd4', 'e4']:
            b.place_piece(square, PieceType.PAWN, Color.BLACK)
        for square in ['c2', 'd2', 'e2']:
            b.place_piece(square, PieceType.PAWN, Color.WHITE)
        bishop = b.place_piece('d3', PieceType.BISHOP, Color.WHITE)
        actualMoves = bishop.calc_potential_moves()
        expectedMoves = ['Bd3-c4', 'Bd3-e4']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('g2', PieceType.PAWN, Color.BLACK)
        bishop = b.place_piece('h1', PieceType.BISHOP, Color.BLACK)
        actualMoves = bishop.calc_potential_moves()
        expectedMoves = []
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_bishop_moves_pinned(self):
        """bishop's moves on a board while pinned"""

        b = Board()
        bishop = b.place_piece('c3', PieceType.BISHOP, Color.BLACK)
        actualMoves = bishop.calc_potential_moves_pinned(Direction.LEFT)
        expectedMoves = []
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        actualMoves = bishop.calc_potential_moves_pinned(Direction.UP)
        expectedMoves = []
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        # if the king is actually not pinned, this test raises an assertion error
        with self.assertRaises(AssertionError):
            bishop.calc_potential_moves_pinned(Direction.DOWN_RIGHT)

        b.place_piece('a1', PieceType.KING, Color.BLACK)
        b.place_piece('e5', PieceType.QUEEN, Color.WHITE)
        actualMoves = bishop.calc_potential_moves_pinned(Direction.UP_RIGHT)
        expectedMoves = ['Bc3-b2', 'Bc3-d4', 'Bc3-e5']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))