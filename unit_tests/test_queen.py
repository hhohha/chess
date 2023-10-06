import unittest
from board import Board
from constants import PieceType, Color, Direction


class TestSuite_QueenMoves(unittest.TestCase):
    def test_queen_moves_1(self):
        """Queen's moves on an empty board"""
        for square in ['a1', 'c2', 'e4', 'g7']:
            b1, b2, b3 = Board(), Board(), Board()
            queen = b1.place_piece(square, PieceType.QUEEN, Color.WHITE)
            rook = b2.place_piece(square, PieceType.ROOK, Color.WHITE)
            bishop = b3.place_piece(square, PieceType.BISHOP, Color.WHITE)
            actualMoves = queen.calc_potential_moves()
            expectedMoves = rook.calc_potential_moves() + bishop.calc_potential_moves()
            self.assertEqual(set(map(lambda x: str(x)[1:], actualMoves)), set(map(lambda x: str(x)[1:], expectedMoves)))

    def test_queen_moves_2(self):
        """Queen's moves on a non-empty board"""
        b = Board()
        queen = b.place_piece('g2', PieceType.QUEEN, Color.WHITE)
        b.place_piece('h2', PieceType.KNIGHT, Color.WHITE)
        b.place_piece('f3', PieceType.PAWN, Color.WHITE)
        b.place_piece('h3', PieceType.ROOK, Color.BLACK)
        b.place_piece('g4', PieceType.PAWN, Color.BLACK)
        actualMoves = queen.calc_potential_moves()
        expectedMoves = ['Qg2-a2', 'Qg2-b2', 'Qg2-c2', 'Qg2-d2', 'Qg2-e2', 'Qg2-f2', 'Qg2-f1', 'Qg2-g1', 'Qg2-h1', 'Qg2-g3', 'Qg2-g4', 'Qg2-h3']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_queen_moves_pinned(self):
        """Queen's moves while pinned"""
        # there is a queen and a king lined up, but no pinner
        b = Board()
        queen = b.place_piece('c1', PieceType.QUEEN, Color.WHITE)
        b.place_piece('a1', PieceType.KING, Color.WHITE)

        with self.assertRaises(AssertionError):
            queen.calc_potential_moves_pinned(Direction.LEFT)
        with self.assertRaises(AssertionError):
            queen.calc_potential_moves_pinned(Direction.RIGHT)

        # there is a queen and a pinner lined up, but no king
        b = Board()
        queen = b.place_piece('c1', PieceType.QUEEN, Color.WHITE)
        b.place_piece('e1', PieceType.ROOK, Color.BLACK)
        b.place_piece('b1', PieceType.KING, Color.WHITE)
        actualMoves = queen.calc_potential_moves_pinned(Direction.LEFT)
        expectedMoves = ['Qc1-d1', 'Qc1-e1']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))