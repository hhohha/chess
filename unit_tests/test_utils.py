import unittest

from constants import Direction
from utils import move_in_direction


class TestSuite_Utils(unittest.TestCase):
    def test_move_in_direction(self):
        col, row = move_in_direction(1, 1, Direction.UP)
        self.assertEqual((col, row), (2, 1))

        col, row = move_in_direction(1, 1, Direction.DOWN)
        self.assertEqual((col, row), (0, 1))

        col, row = move_in_direction(1, 1, Direction.LEFT)
        self.assertEqual((col, row), (1, 0))

        col, row = move_in_direction(1, 1, Direction.RIGHT)
        self.assertEqual((col, row), (1, 2))

        col, row = move_in_direction(1, 1, Direction.UP_RIGHT)
        self.assertEqual((col, row), (2, 2))

        col, row = move_in_direction(1, 1, Direction.UP_LEFT)
        self.assertEqual((col, row), (2, 0))

        col, row = move_in_direction(1, 1, Direction.DOWN_RIGHT)
        self.assertEqual((col, row), (0, 2))
