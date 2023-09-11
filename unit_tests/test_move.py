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
        b.place_piece('e4', PieceType.KNIGHT, Color.WHITE)
        knight = b.get_square('e4').piece
        move1 = Move(knight, b.get_square('f6'))
        self.assertEqual(str(move1), 'Ne4-f6')
        self.assertFalse(move1.is_castling())

        b.place_piece('e1', PieceType.KING, Color.WHITE)
        b.place_piece('a1', PieceType.KING, Color.WHITE)
        king = b.get_square('e1').piece
        move2 = Move(king, b.get_square('c1'))
        self.assertEqual(str(move2), 'Ke1-c1')
        self.assertTrue(move2.is_castling())
