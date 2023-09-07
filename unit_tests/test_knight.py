import unittest
from board import Board
from constants import PieceType, Color, Direction


class TestSuite_KnightMoves(unittest.TestCase):
    def test_knight_moves_1(self):
        """
        knight's moves on an empty board
        """
        b = Board()
        b.place_piece('a1', PieceType.KNIGHT, Color.WHITE)
        knight = b.get_square('a1').piece
        actualMoves = knight.calc_potential_moves()
        expectedMoves = ['Na1-c2', 'Na1-b3']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('e4', PieceType.KNIGHT, Color.WHITE)
        knight = b.get_square('e4').piece
        actualMoves = knight.calc_potential_moves()
        expectedMoves = ['Ne4-d6', 'Ne4-d2', 'Ne4-c3', 'Ne4-c5', 'Ne4-f2', 'Ne4-f6', 'Ne4-g3', 'Ne4-g5', ]
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_knight_moves_2(self):
        """
        knight's moves on a non-empty board
        """
        b = Board()
        b.place_piece('c1', PieceType.KNIGHT, Color.WHITE)
        b.place_piece('d3', PieceType.PAWN, Color.WHITE)
        b.place_piece('b3', PieceType.PAWN, Color.BLACK)
        knight = b.get_square('c1').piece
        actualMoves = knight.calc_potential_moves()
        expectedMoves = ['Nc1-a2', 'Nc1-e2', 'Nc1-b3']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_knight_moves_pinned(self):
        """
        knight's moves while pinned
        """
        b = Board()
        b.place_piece('c1', PieceType.KNIGHT, Color.WHITE)
        knight = b.get_square('c1').piece
        actualMoves = knight.calc_potential_moves_pinned(Direction.UP)
        expectedMoves = []
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        actualMoves = knight.calc_potential_moves_pinned(Direction.LEFT)
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        actualMoves = knight.calc_potential_moves_pinned(Direction.DOWN_RIGHT)
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))