import unittest
from board import Board
from constants import PieceType, Color, Direction


class TestSuite_KingMoves(unittest.TestCase):
    def test_king_moves(self):
        """
        king's moves on an empty board
        """
        b = Board()
        b.place_piece('a1', PieceType.KING, Color.WHITE)
        king = b.get_square('a1').piece
        actualMoves = king.calc_potential_moves()
        expectedMoves = ['Ka1-b1', 'Ka1-b2', 'Ka1-a2']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('e4', PieceType.KING, Color.WHITE)
        b.place_piece('e5', PieceType.PAWN, Color.BLACK)
        b.place_piece('e3', PieceType.PAWN, Color.WHITE)
        king = b.get_square('e4').piece
        actualMoves = king.calc_potential_moves()
        expectedMoves = ['Ke4-d3', 'Ke4-f3', 'Ke4-d4', 'Ke4-f4', 'Ke4-d5', 'Ke4-e5', 'Ke4-f5']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))
