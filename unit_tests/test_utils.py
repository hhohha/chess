import unittest
from board import Board
from constants import Direction
from utils import move_in_direction, reverse_dir, is_same_col_or_row, is_same_diag, square_idx_to_coord, coord_to_square_idx, get_direction


class TestSuite_Utils(unittest.TestCase):
    def test_move_in_direction(self):
        col, row = move_in_direction(1, 1, Direction.UP)
        self.assertEqual((col, row), (1, 2))

        col, row = move_in_direction(1, 1, Direction.DOWN)
        self.assertEqual((col, row), (1, 0))

        col, row = move_in_direction(1, 1, Direction.LEFT)
        self.assertEqual((col, row), (0, 1))

        col, row = move_in_direction(1, 1, Direction.RIGHT)
        self.assertEqual((col, row), (2, 1))

        col, row = move_in_direction(1, 1, Direction.UP_RIGHT)
        self.assertEqual((col, row), (2, 2))

        col, row = move_in_direction(1, 1, Direction.UP_LEFT)
        self.assertEqual((col, row), (0, 2))

        col, row = move_in_direction(1, 1, Direction.DOWN_RIGHT)
        self.assertEqual((col, row), (2, 0))

        col, row = move_in_direction(1, 1, Direction.DOWN_LEFT)
        self.assertEqual((col, row), (0, 0))

    def test_reverse_dir(self):
        self.assertEqual(reverse_dir(Direction.UP), Direction.DOWN)
        self.assertEqual(reverse_dir(Direction.DOWN), Direction.UP)
        self.assertEqual(reverse_dir(Direction.LEFT), Direction.RIGHT)
        self.assertEqual(reverse_dir(Direction.RIGHT), Direction.LEFT)
        self.assertEqual(reverse_dir(Direction.UP_RIGHT), Direction.DOWN_LEFT)
        self.assertEqual(reverse_dir(Direction.UP_LEFT), Direction.DOWN_RIGHT)
        self.assertEqual(reverse_dir(Direction.DOWN_RIGHT), Direction.UP_LEFT)
        self.assertEqual(reverse_dir(Direction.DOWN_LEFT), Direction.UP_RIGHT)

    def test_is_same_col_row_diag(self):
        b = Board()
        self.assertTrue(is_same_col_or_row(b.get_square_by_name('a1'), b.get_square_by_name('a2')))
        self.assertTrue(is_same_col_or_row(b.get_square_by_name('a1'), b.get_square_by_name('a7')))
        self.assertTrue(is_same_col_or_row(b.get_square_by_name('a1'), b.get_square_by_name('b1')))
        self.assertTrue(is_same_col_or_row(b.get_square_by_name('a1'), b.get_square_by_name('f1')))
        self.assertFalse(is_same_col_or_row(b.get_square_by_name('a1'), b.get_square_by_name('b2')))
        self.assertFalse(is_same_col_or_row(b.get_square_by_name('a1'), b.get_square_by_name('f3')))

        self.assertTrue(is_same_diag(b.get_square_by_name('a1'), b.get_square_by_name('b2')))
        self.assertTrue(is_same_diag(b.get_square_by_name('a1'), b.get_square_by_name('h8')))
        self.assertTrue(is_same_diag(b.get_square_by_name('a2'), b.get_square_by_name('b1')))
        self.assertFalse(is_same_diag(b.get_square_by_name('a2'), b.get_square_by_name('h8')))
        self.assertFalse(is_same_diag(b.get_square_by_name('e1'), b.get_square_by_name('b3')))

    def test_square_coord_idx(self):
        self.assertEqual(square_idx_to_coord(0), 'a1')
        self.assertEqual(coord_to_square_idx('a1'), 0)

        self.assertEqual(square_idx_to_coord(7), 'h1')
        self.assertEqual(coord_to_square_idx('h1'), 7)

        self.assertEqual(square_idx_to_coord(56), 'a8')
        self.assertEqual(coord_to_square_idx('a8'), 56)

        self.assertEqual(square_idx_to_coord(63), 'h8')
        self.assertEqual(coord_to_square_idx('h8'), 63)

        self.assertEqual(square_idx_to_coord(28), 'e4')
        self.assertEqual(coord_to_square_idx('e4'), 28)

    def test_get_direction(self):
        b = Board()
        self.assertEqual(get_direction(b.get_square_by_name('a1'), b.get_square_by_name('a2')), Direction.UP)
        self.assertEqual(get_direction(b.get_square_by_name('b7'), b.get_square_by_name('b3')), Direction.DOWN)

        #TODO - throws an exeption
        #self.assertIsNone(get_direction(b.get_square_by_name('d3'), b.get_square_by_name('d3')))

        self.assertEqual(get_direction(b.get_square_by_name('d3'), b.get_square_by_name('f5')), Direction.UP_RIGHT)
        self.assertEqual(get_direction(b.get_square_by_name('f5'), b.get_square_by_name('d3')), Direction.DOWN_LEFT)
        self.assertEqual(get_direction(b.get_square_by_name('d3'), b.get_square_by_name('b5')), Direction.UP_LEFT)
        self.assertEqual(get_direction(b.get_square_by_name('b5'), b.get_square_by_name('d3')), Direction.DOWN_RIGHT)
        # TODO - throws an exeption
        #self.assertIsNone(get_direction(b.get_square_by_name('d3'), b.get_square_by_name('f4')))


