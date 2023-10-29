import unittest
from board import Board
from constants import FEN_INIT, FEN_A, Color, FEN_B, FEN_C, FEN_D, FEN_D_INVERTED, FEN_E, FEN_E_NO_CASTLE, FEN_F


class TestSuite_LegalMoves(unittest.TestCase):
    def test_legal_moves_position_initial(self):
        """test legal moves from initial position"""
        b = Board()
        b.load_FEN(FEN_INIT)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 20)

        b.turn = Color.BLACK
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 20)

    def test_legal_moves_position_a(self):
        """test legal moves from position a"""
        b = Board()
        b.load_FEN(FEN_A)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 3)

        b.turn = Color.BLACK
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 7)

    def test_legal_moves_position_b(self):
        """test legal moves from position b"""
        b = Board()
        b.load_FEN(FEN_B)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 44)

        b.turn = Color.BLACK
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 34)

    def test_legal_moves_position_c(self):
        """test legal moves from position c"""
        b = Board()
        b.load_FEN(FEN_C)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 14)

        b.turn = Color.BLACK
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 15)

    def test_legal_moves_position_d(self):
        """test legal moves from position d"""
        b = Board()
        b.load_FEN(FEN_D)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 6)
        # cannot test black to move, white is in check

        b.load_FEN(FEN_D_INVERTED)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 6)

    def test_legal_moves_position_e(self):
        """test legal moves from position e"""
        b = Board()
        b.load_FEN(FEN_E)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 48)

        b.turn = Color.BLACK
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 43)

    def test_legal_moves_position_e_no_castle(self):
        """test legal moves from position e with no castling"""
        b = Board()
        b.load_FEN(FEN_E_NO_CASTLE)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 46)

        b.turn = Color.BLACK
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 41)

    def test_legal_moves_position_f(self):
        """test legal moves from position f"""
        b = Board()
        b.load_FEN(FEN_F)
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 46)

        b.turn = Color.BLACK
        moves = b.calc_all_legal_moves()
        self.assertEqual(len(moves), 46)