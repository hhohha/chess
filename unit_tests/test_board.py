import unittest

from board import Board


class TestSuite_Board(unittest.TestCase):
    def test_square_coords(self):
        b = Board()

        sqr = b.get_square_by_idx(-1)
        self.assertIsNone(sqr)

        sqr = b.get_square_by_idx(64)
        self.assertIsNone(sqr)

        sqr = b.get_square_by_idx(0)
        self.assertEqual(sqr.coordinates, 'a1')

        sqr = b.get_square_by_coords(1, 8)
        self.assertIsNone(sqr)

        sqr = b.get_square_by_coords(0, 7)
        self.assertEqual(sqr.coordinates, 'a8')

        sqr = b.get_square_by_coords(7, 7)
        self.assertEqual(sqr.coordinates, 'h8')


