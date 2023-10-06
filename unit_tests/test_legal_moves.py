import unittest
from board import Board
from constants import FEN_INIT, FEN_A, Color, FEN_B


class TestSuite_LegalMoves(unittest.TestCase):
    def test_legal_moves(self):
        """test legal moves from various positions"""
        # b = Board()
        # b.load_FEN(FEN_INIT)
        # moves = b.get_all_legal_moves()
        # self.assertEqual(len(moves), 20)
        #
        # b.load_FEN(FEN_A)
        # moves = b.get_all_legal_moves()
        # self.assertEqual(len(moves), 3)
        #
        # b.turn = Color.BLACK
        # moves = b.get_all_legal_moves()
        # self.assertEqual(len(moves), 7)

        b = Board()
        b.load_FEN(FEN_B)
        for square in b.squares:
            print(f'{square}: W: {square.get_attacked_by(Color.WHITE)}   B: {square.get_attacked_by(Color.BLACK)}')
        #moves = b.get_all_legal_moves()
        #for move in moves:
        #    print(move)
        #self.assertEqual(len(moves), 44)

        #pawns    13
        #knights   8
        #bishops  12
        #rooks     2
        #queen     5
        #king      4
        #13 + 8 + 12 + 2 + 5 + 4