import unittest
from board import Board
from constants import PieceType, Color, Direction
from move import Move


class TestSuite_KnightMoves(unittest.TestCase):
    def test_knight_moves_1(self):
        """knight's moves on an empty board"""

        b = Board()
        knight = b.place_piece('a1', PieceType.KNIGHT, Color.WHITE)
        actualMoves = knight.calc_potential_moves()
        expectedMoves = ['Na1-c2', 'Na1-b3']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        knight = b.place_piece('e4', PieceType.KNIGHT, Color.WHITE)
        actualMoves = knight.calc_potential_moves()
        expectedMoves = ['Ne4-d6', 'Ne4-d2', 'Ne4-c3', 'Ne4-c5', 'Ne4-f2', 'Ne4-f6', 'Ne4-g3', 'Ne4-g5', ]
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_knight_moves_2(self):
        """knight's moves on a non-empty board"""

        b = Board()
        knight = b.place_piece('c1', PieceType.KNIGHT, Color.WHITE)
        b.place_piece('d3', PieceType.PAWN, Color.WHITE)
        b.place_piece('b3', PieceType.PAWN, Color.BLACK)
        actualMoves = knight.calc_potential_moves()
        expectedMoves = ['Nc1-a2', 'Nc1-e2', 'Nc1-b3']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_knight_moves_pinned(self):
        """knight's moves while pinned"""

        b = Board()
        knight = b.place_piece('c1', PieceType.KNIGHT, Color.WHITE)
        actualMoves = knight.calc_potential_moves_pinned(Direction.UP)
        expectedMoves = []
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        actualMoves = knight.calc_potential_moves_pinned(Direction.LEFT)
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        actualMoves = knight.calc_potential_moves_pinned(Direction.DOWN_RIGHT)
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_my(self):
        b = Board()
        wk = b.place_piece('h1', PieceType.KING, Color.WHITE)
        wk.update_attacked_squares()

        bk = b.place_piece('h3', PieceType.KING, Color.BLACK)
        bk.update_attacked_squares()

        wn = b.place_piece('f1', PieceType.KNIGHT, Color.WHITE)
        wn.recalculate()

        moves = b.get_all_legal_moves()
        m = Move(wn, b.get_square_by_name('g3'))
        b.perform_move(m)

        print('done')