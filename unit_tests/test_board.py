import unittest

from board import Board
from constants import FEN_INIT, PieceType, Color, Direction, FEN_A, FEN_B, FEN_C, FEN_D
from move import Move


class TestSuite_Board(unittest.TestCase):
    def test_square_coords(self):
        b = Board()

        sqr = b.get_square_by_idx(-1)
        self.assertIsNone(sqr)

        sqr = b.get_square_by_idx(64)
        self.assertIsNone(sqr)

        sqr = b.get_square_by_idx(0)
        self.assertEqual(sqr.name, 'a1')

        sqr = b.get_square_by_coords(1, 8)
        self.assertIsNone(sqr)

        sqr = b.get_square_by_coords(0, 7)
        self.assertEqual(sqr.name, 'a8')

        sqr = b.get_square_by_coords(7, 7)
        self.assertEqual(sqr.name, 'h8')

    def test_is_castle_possible(self):
        b = Board()
        b.place_piece('e1', PieceType.KING, Color.WHITE)
        b.place_piece('h1', PieceType.ROOK, Color.WHITE)
        self.assertTrue(b.is_castle_possible(Color.WHITE, Direction.RIGHT))
        self.assertFalse(b.is_castle_possible(Color.WHITE, Direction.LEFT))

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
        self.assertIsNone(b.enPassantPawnSquare[-1])
        self.assertEqual(b.halfMoves, [0])
        self.assertEqual(b.moves, 1)

        b.load_FEN(FEN_A)
        self.assertIsNone(b.get_square_by_name('a1').piece)
        self.assertEqual(b.get_square_by_name('h1').piece.kind, PieceType.KING)
        self.assertEqual(b.get_square_by_name('h1').piece.color, Color.WHITE)
        self.assertEqual(b.get_square_by_name('a8').piece.kind, PieceType.KING)
        self.assertEqual(b.get_square_by_name('a8').piece.color, Color.BLACK)

        self.assertEqual(b.whiteKing, b.get_square_by_name('h1').piece)
        self.assertEqual(b.blackKing, b.get_square_by_name('a8').piece)
        self.assertEqual(set(b.whiteRooks), set())
        self.assertEqual(set(b.blackRooks), set())
        self.assertEqual(set(b.whitePawns), set())
        self.assertEqual(set(b.blackPawns), {b.get_square_by_name('d2').piece})
        self.assertEqual(b.turn, Color.WHITE)
        self.assertIsNone(b.enPassantPawnSquare[-1])
        self.assertEqual(b.halfMoves, [98])
        self.assertEqual(b.moves, 0)

    def test_find_first_piece_in_dir(self):
        b = Board()
        b.load_FEN(FEN_INIT)
        self.assertEqual(b.find_first_piece_in_dir(b.get_square_by_name('e4'), Direction.UP), b.get_square_by_name('e7'))
        self.assertEqual(b.find_first_piece_in_dir(b.get_square_by_name('e4'), Direction.UP_LEFT), b.get_square_by_name('b7'))
        self.assertIsNone(b.find_first_piece_in_dir(b.get_square_by_name('e4'), Direction.RIGHT))
        self.assertIsNone(b.find_first_piece_in_dir(b.get_square_by_name('e4'), Direction.LEFT))
        self.assertEqual(b.find_first_piece_in_dir(b.get_square_by_name('e1'), Direction.UP), b.get_square_by_name('e2'))
        self.assertEqual(b.find_first_piece_in_dir(b.get_square_by_name('e1'), Direction.RIGHT), b.get_square_by_name('f1'))
        self.assertEqual(b.find_first_piece_in_dir(b.get_square_by_name('e1'), Direction.UP_RIGHT), b.get_square_by_name('f2'))


    def test_get_pinned_pieces(self):
        b = Board()
        b.load_FEN(FEN_INIT)
        self.assertEqual(b.calc_pinned_pieces(Color.WHITE), {})
        self.assertEqual(b.calc_pinned_pieces(Color.BLACK), {})

        b = Board()
        b.load_FEN(FEN_C)

        pinnedWhite = b.calc_pinned_pieces(Color.WHITE)
        self.assertEqual(len(pinnedWhite), 1)
        self.assertEqual(list(pinnedWhite.keys())[0], b.get_square_by_name('b5').piece)
        self.assertEqual(list(pinnedWhite.values())[0], Direction.RIGHT)

        pinnedBlack = b.calc_pinned_pieces(Color.BLACK)
        self.assertEqual(len(pinnedBlack), 1)
        self.assertEqual(list(pinnedBlack.keys())[0], b.get_square_by_name('f4').piece)
        self.assertEqual(list(pinnedBlack.values())[0], Direction.LEFT)

        # king surrounded by own pawns, all pinned by queens
        fen1 = 'k7/8/2q1q1q1/3PPP2/2qPKPq1/3PPP2/2q1q1q1/8 w - - 0 0'
        b.load_FEN(fen1)

        pinnedWhite = b.calc_pinned_pieces(Color.WHITE)
        self.assertEqual(len(pinnedWhite), 8)
        self.assertEqual(set(pinnedWhite.keys()), set(b.whitePawns))
        self.assertEqual(set(pinnedWhite.values()), {Direction.UP, Direction.UP_LEFT, Direction.UP_RIGHT, Direction.LEFT, Direction.RIGHT,
                                                     Direction.DOWN_LEFT, Direction.DOWN_RIGHT, Direction.DOWN})

        # substitute queens for rooks, only 4 pawns are pinned
        fen1 = 'k7/8/2r1r1r1/3PPP2/2rPKPr1/3PPP2/2r1r1r1/8 w - - 0 0'
        b.load_FEN(fen1)
        pinnedWhite = b.calc_pinned_pieces(Color.WHITE)
        self.assertEqual(len(pinnedWhite), 4)
        self.assertEqual(set(pinnedWhite.keys()), {b.get_square_by_name('d4').piece, b.get_square_by_name('f4').piece,
                                                   b.get_square_by_name('e3').piece, b.get_square_by_name('e5').piece})
        self.assertEqual(set(pinnedWhite.values()), {Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN})

    def test_my(self):
        b = Board()
        b.load_FEN(FEN_D)
        m = Move(b.get_square_by_name('b4').piece, b.get_square_by_name('c5'))
        b.perform_move(m)

        m = Move(b.get_square_by_name('a3').piece, b.get_square_by_name('c5'))
        b.perform_move(m)

        moves = b.get_all_legal_moves()
        for move in moves:
            print(move)
        print(f'moves cnt: {len(moves)}')

    def xtest_recalculation(self):
        pass

    def xtest_place_piece(self):
        pass

    def xtest_is_check(self):
        pass
