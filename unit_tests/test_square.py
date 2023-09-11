import unittest
from board import Board


class TestSuite_Square(unittest.TestCase):
    def test_coordinates(self):
        """
        square coordinates
        """
        b = Board()
        square = b.get_square_by_name('e4')
        self.assertEqual(square.rowIdx, 3)
        self.assertEqual(square.colIdx, 4)
        self.assertEqual(square.coordinates, 'e4')

        square = b.get_square_by_name('c7')
        self.assertEqual(square.rowIdx, 6)
        self.assertEqual(square.colIdx, 2)
        self.assertEqual(square.coordinates, 'c7')
