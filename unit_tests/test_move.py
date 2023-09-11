import unittest

from board import Board
from constants import PieceType, Color
from move import Move


class TestSuite_Move(unittest.TestCase):
    def test_coordinates(self):
        """
        basic move
        """
        b = Board()
        knight = b.place_piece('e4', PieceType.KNIGHT, Color.WHITE)
        move1 = Move(knight, b.get_square_by_name('f6'))
        self.assertEqual(str(move1), 'Ne4-f6')
        self.assertFalse(move1.is_castling())

        king = b.place_piece('e1', PieceType.KING, Color.WHITE)
        b.place_piece('a1', PieceType.ROOK, Color.WHITE)
        move2 = Move(king, b.get_square_by_name('c1'))
        self.assertEqual(str(move2), 'Ke1-c1')
        self.assertTrue(move2.is_castling())
