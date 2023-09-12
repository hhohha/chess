import unittest

from board import Board
from constants import FEN_INIT, PieceType, Color, Direction


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

    def test_load_FEN(self):
        b = Board()
        b.load_FEN(FEN_INIT)
        self.assertEqual(b.get_square_by_name('a1').piece.kind, PieceType.ROOK)
        self.assertEqual(b.get_square_by_name('a1').piece.color, Color.WHITE)
        self.assertEqual(b.get_square_by_name('e1').piece.kind, PieceType.KING)
        self.assertEqual(b.get_square_by_name('e1').piece.color, Color.WHITE)
        self.assertEqual(b.get_square_by_name('c8').piece.kind, PieceType.BISHOP)
        self.assertEqual(b.get_square_by_name('c8').piece.color, Color.BLACK)

        self.assertEqual(b.whiteKing, b.get_square_by_name('e1').piece)
        self.assertEqual(b.blackKing, b.get_square_by_name('e8').piece)
        self.assertEqual(set(b.whiteRooks), {b.get_square_by_name('a1').piece, b.get_square_by_name('h1').piece})
        self.assertEqual(set(b.blackRooks), {b.get_square_by_name('a8').piece, b.get_square_by_name('h8').piece})
        self.assertEqual(set(b.whitePawns), {b.get_square_by_name('a2').piece, b.get_square_by_name('b2').piece, b.get_square_by_name('c2').piece,
                                             b.get_square_by_name('d2').piece, b.get_square_by_name('e2').piece, b.get_square_by_name('f2').piece,
                                             b.get_square_by_name('g2').piece, b.get_square_by_name('h2').piece})

        self.assertEqual(b.turn, Color.WHITE)
        self.assertTrue(b.is_castle_possible(Color.WHITE, Direction.RIGHT))
        self.assertTrue(b.is_castle_possible(Color.WHITE, Direction.LEFT))
        self.assertTrue(b.is_castle_possible(Color.BLACK, Direction.RIGHT))
        self.assertTrue(b.is_castle_possible(Color.BLACK, Direction.LEFT))

        self.assertIsNone(b.enPassantPawnSquare)

        self.assertEqual(b.halfMoves, 0)
        self.assertEqual(b.moves, 1)


    def xtest_recalculation(self):
        pass

    def xtest_place_piece(self):
        pass

    def xtest_is_check(self):
        pass

    def xtest_is_castle_possible(self):
        pass

    def xtest_get_pinned_pieces(self):
        pass