import unittest
from board import Board
from constants import PieceType, Color, Direction


class TestSuite_RookMoves(unittest.TestCase):
    def test_rook_moves_1(self):
        """
        rooks's moves on an empty board
        """
        b = Board()
        b.place_piece('b3', PieceType.ROOK, Color.WHITE)
        rook = b.get_square('b3').piece
        actualMoves = rook.calc_potential_moves()
        expectedMoves = [f'Rb3-{col}3' for col in 'acdefgh'] + [f'Rb3-b{row}' for row in [1, 2, 4, 5, 6, 7, 8]]
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_rook_moves_2(self):
        """
        rooks's moves on a non-empty board
        """
        b = Board()
        b.place_piece('e4', PieceType.ROOK, Color.WHITE)
        b.place_piece('e5', PieceType.ROOK, Color.WHITE)
        b.place_piece('e2', PieceType.QUEEN, Color.BLACK)
        b.place_piece('b4', PieceType.PAWN, Color.WHITE)
        b.place_piece('h4', PieceType.PAWN, Color.BLACK)
        rook = b.get_square('e4').piece
        actualMoves = rook.calc_potential_moves()
        expectedMoves = ['Re4-e3', 'Re4-e2', 'Re4-d4', 'Re4-c4', 'Re4-f4', 'Re4-g4', 'Re4-h4']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_rook_moves_pinned(self):
        """
        rooks's moves while pinned
        """
        b = Board()
        b.place_piece('e4', PieceType.ROOK, Color.WHITE)
        rook = b.get_square('e4').piece
        actualMoves = rook.calc_potential_moves_pinned(Direction.UP_LEFT)
        expectedMoves = []
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        # there is a rook and a king lined up, but no pinner
        b = Board()
        b.place_piece('c1', PieceType.ROOK, Color.WHITE)
        b.place_piece('a1', PieceType.KING, Color.WHITE)
        rook = b.get_square('c1').piece

        with self.assertRaises(AssertionError):
            rook.calc_potential_moves_pinned(Direction.LEFT)
        with self.assertRaises(AssertionError):
            rook.calc_potential_moves_pinned(Direction.RIGHT)

        # there is a rook and a pinner lined up, but no king
        b = Board()
        b.place_piece('c1', PieceType.ROOK, Color.WHITE)
        b.place_piece('d1', PieceType.ROOK, Color.BLACK)
        rook = b.get_square('c1').piece

        with self.assertRaises(AssertionError):
            rook.calc_potential_moves_pinned(Direction.LEFT)
        with self.assertRaises(AssertionError):
            rook.calc_potential_moves_pinned(Direction.RIGHT)

        # there is a rook and a king lined up, but the pinner is invalid (knight)
        b = Board()
        b.place_piece('a1', PieceType.KING, Color.WHITE)
        b.place_piece('c1', PieceType.ROOK, Color.WHITE)
        b.place_piece('e1', PieceType.KNIGHT, Color.BLACK)
        rook = b.get_square('c1').piece

        with self.assertRaises(AssertionError):
            rook.calc_potential_moves_pinned(Direction.LEFT)
        with self.assertRaises(AssertionError):
            rook.calc_potential_moves_pinned(Direction.RIGHT)

    def test_rook_moves_pinned_2(self):
        """
        rooks's moves while pinned
        """

        # correct pin, bad direction
        b = Board()
        b.place_piece('a1', PieceType.KING, Color.WHITE)
        b.place_piece('c1', PieceType.ROOK, Color.WHITE)
        b.place_piece('e1', PieceType.QUEEN, Color.BLACK)
        rook = b.get_square('c1').piece

#        with self.assertRaises(AssertionError):
#            rook.calc_potential_moves_pinned(Direction.RIGHT)

        # correct pin and direction
        actualMoves = rook.calc_potential_moves_pinned(Direction.LEFT)
        expectedMoves = ['Rc1-b1', 'Rc1-d1', 'Rc1-e1']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))
