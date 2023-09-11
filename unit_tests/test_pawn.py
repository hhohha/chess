import unittest
from board import Board
from constants import PieceType, Color, Direction


class TestSuite_PawnMoves(unittest.TestCase):
    def test_generate_pawn_moves(self):
        """
        generates all promotion moves if the pawn reaches the last rank
        """
        b = Board()
        b.place_piece('b6', PieceType.PAWN, Color.WHITE)
        pawn = b.get_square('b6').piece
        targetSquare = b.get_square('b7')
        actualMoves = pawn.generate_pawn_move(targetSquare)
        expectedMoves = ['pb6-b7']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('e2', PieceType.PAWN, Color.BLACK)
        pawn = b.get_square('e2').piece
        targetSquare = b.get_square('e1')
        actualMoves = pawn.generate_pawn_move(targetSquare)
        expectedMoves = ['pe2-e1Q', 'pe2-e1R', 'pe2-e1B', 'pe2-e1N']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

    def test_pawn_moves_forward(self):
        """
        pawn's moves on an empty board
        """
        b = Board()
        b.place_piece('a2', PieceType.PAWN, Color.WHITE)
        pawn = b.get_square('a2').piece
        actualMoves = pawn.calc_potential_moves()
        expectedMoves = ['pa2-a3', 'pa2-a4']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        forwardMoves = pawn.get_forward_moves()
        self.assertEqual(set(map(str, forwardMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('a6', PieceType.PAWN, Color.BLACK)
        pawn = b.get_square('a6').piece
        actualMoves = pawn.calc_potential_moves()
        expectedMoves = ['pa6-a5']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        forwardMoves = pawn.get_forward_moves()
        self.assertEqual(set(map(str, forwardMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('a7', PieceType.PAWN, Color.WHITE)
        pawn = b.get_square('a7').piece
        actualMoves = pawn.calc_potential_moves()
        expectedMoves = ['pa7-a8Q', 'pa7-a8R', 'pa7-a8B', 'pa7-a8N']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        forwardMoves = pawn.get_forward_moves()
        self.assertEqual(set(map(str, forwardMoves)), set(expectedMoves))

    def test_pawn_captures(self):
        """
        pawn's captures (excluding en passant)
        """
        b = Board()
        b.place_piece('b2', PieceType.PAWN, Color.WHITE)
        pawn = b.get_square('b2').piece
        captures = pawn.get_capture_moves(1)  # captures to the right
        self.assertEqual(set(map(str, captures)), set())

        captures = pawn.get_capture_moves(-1)  # captures to the left
        self.assertEqual(set(map(str, captures)), set())

        b = Board()
        b.place_piece('b2', PieceType.PAWN, Color.WHITE)
        b.place_piece('c3', PieceType.PAWN, Color.BLACK)
        pawn = b.get_square('b2').piece
        captures = pawn.get_capture_moves(1)  # captures to the right
        expectedMoves = ['pb2-c3']
        self.assertEqual(set(map(str, captures)), set(expectedMoves))

        captures = pawn.get_capture_moves(-1)  # captures to the left
        self.assertEqual(set(map(str, captures)), set())

        b = Board()
        b.place_piece('b2', PieceType.PAWN, Color.BLACK)
        b.place_piece('c1', PieceType.KNIGHT, Color.WHITE)
        b.place_piece('a1', PieceType.ROOK, Color.WHITE)
        pawn = b.get_square('b2').piece

        captures = pawn.get_capture_moves(1)  # captures to the right
        expectedMoves = ['pb2-c1Q', 'pb2-c1R', 'pb2-c1B', 'pb2-c1N']
        self.assertEqual(set(map(str, captures)), set(expectedMoves))

        captures = pawn.get_capture_moves(-1)  # captures to the left
        expectedMoves = ['pb2-a1Q', 'pb2-a1R', 'pb2-a1B', 'pb2-a1N']
        self.assertEqual(set(map(str, captures)), set(expectedMoves))

        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.BLACK)
        b.place_piece('d4', PieceType.PAWN, Color.WHITE)
        b.place_piece('f4', PieceType.PAWN, Color.BLACK)
        pawn = b.get_square('e5').piece

        captures = pawn.get_capture_moves(1)  # captures to the right
        expectedMoves = []
        self.assertEqual(set(map(str, captures)), set(expectedMoves))

        captures = pawn.get_capture_moves(-1)  # captures to the left
        expectedMoves = ['pe5-d4']
        self.assertEqual(set(map(str, captures)), set(expectedMoves))

    def test_is_en_passant_pin(self):
        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        b.place_piece('d5', PieceType.PAWN, Color.BLACK)
        b.place_piece('e1', PieceType.KING, Color.WHITE)
        pawn = b.get_square('e5').piece
        self.assertFalse(pawn.is_en_passant_pin(b.get_square('d5')))

        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        b.place_piece('d5', PieceType.PAWN, Color.BLACK)
        b.place_piece('h5', PieceType.KING, Color.WHITE)
        b.place_piece('a5', PieceType.ROOK, Color.BLACK)
        pawn = b.get_square('e5').piece
        self.assertTrue(pawn.is_en_passant_pin(b.get_square('d5')))

        # another piece breaking the pin
        b.place_piece('b5', PieceType.BISHOP, Color.BLACK)
        self.assertFalse(pawn.is_en_passant_pin(b.get_square('d5')))

        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        b.place_piece('d5', PieceType.PAWN, Color.BLACK)
        b.place_piece('h5', PieceType.KING, Color.WHITE)
        pawn = b.get_square('e5').piece
        self.assertFalse(pawn.is_en_passant_pin(b.get_square('d5')))

        b.place_piece('a5', PieceType.KNIGHT, Color.BLACK)
        self.assertFalse(pawn.is_en_passant_pin(b.get_square('d5')))

        b.place_piece('b5', PieceType.QUEEN, Color.WHITE)
        self.assertFalse(pawn.is_en_passant_pin(b.get_square('d5')))

        b.place_piece('c5', PieceType.QUEEN, Color.BLACK)
        self.assertTrue(pawn.is_en_passant_pin(b.get_square('d5')))


    def test_pawn_en_passant(self):
        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        pawn = b.get_square('e5').piece
        enPassantMoves = pawn.get_en_passant_moves()
        self.assertEqual(set(map(str, enPassantMoves)), set())

        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        b.place_piece('d5', PieceType.PAWN, Color.BLACK)
        pawn = b.get_square('e5').piece
        enPassantMoves = pawn.get_en_passant_moves()
        self.assertEqual(set(map(str, enPassantMoves)), set())

        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        b.place_piece('d5', PieceType.PAWN, Color.BLACK)
        b.place_piece('f5', PieceType.PAWN, Color.BLACK)
        b.enPassantSquare = b.get_square('d5')
        pawn = b.get_square('e5').piece
        expectedMoves = ['pe5-d6']
        enPassantMoves = pawn.get_en_passant_moves()
        self.assertEqual(set(map(str, enPassantMoves)), set(expectedMoves))

    def test_pawn_moves_all(self):
        b = Board()
        b.place_piece('e7', PieceType.PAWN, Color.BLACK)
        b.place_piece('d6', PieceType.PAWN, Color.BLACK)
        b.place_piece('f6', PieceType.PAWN, Color.WHITE)
        pawn = b.get_square('e7').piece
        actualMoves = pawn.calc_potential_moves()
        expectedMoves = ['pe7-e6', 'pe7-e5', 'pe7-f6']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('e7', PieceType.PAWN, Color.WHITE)
        b.place_piece('d8', PieceType.ROOK, Color.BLACK)
        b.place_piece('f8', PieceType.ROOK, Color.BLACK)
        pawn = b.get_square('e7').piece
        actualMoves = pawn.calc_potential_moves()
        expectedMoves = ['pe7-e8Q', 'pe7-e8R', 'pe7-e8B', 'pe7-e8N', 'pe7-f8Q', 'pe7-f8R', 'pe7-f8B', 'pe7-f8N', 'pe7-d8Q', 'pe7-d8R', 'pe7-d8B',
                         'pe7-d8N']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        b.place_piece('d6', PieceType.PAWN, Color.BLACK)
        b.place_piece('f5', PieceType.PAWN, Color.BLACK)
        b.place_piece('e6', PieceType.PAWN, Color.BLACK)
        b.enPassantSquare = b.get_square('f5')
        pawn = b.get_square('e5').piece
        actualMoves = pawn.calc_potential_moves()
        expectedMoves = ['pe5-d6', 'pe5-f6']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        b = Board()
        b.place_piece('e2', PieceType.PAWN, Color.WHITE)
        b.place_piece('e3', PieceType.PAWN, Color.WHITE)
        pawn = b.get_square('e2').piece
        actualMoves = pawn.calc_potential_moves()
        self.assertEqual(set(map(str, actualMoves)), set())


    def test_pawn_moves_pinned(self):
        # pinned from side = no moves
        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        b.place_piece('d5', PieceType.ROOK, Color.BLACK)
        b.place_piece('h5', PieceType.KING, Color.WHITE)
        pawn = b.get_square('e5').piece
        actualMoves = pawn.calc_potential_moves_pinned(Direction.RIGHT)
        self.assertEqual(set(map(str, actualMoves)), set())

        # pinned from front or back - moves forward
        b = Board()
        b.place_piece('e7', PieceType.PAWN, Color.BLACK)
        b.place_piece('e1', PieceType.ROOK, Color.WHITE)
        b.place_piece('e8', PieceType.KING, Color.BLACK)
        pawn = b.get_square('e7').piece
        actualMoves = pawn.calc_potential_moves_pinned(Direction.UP)
        expectedMoves = ['pe7-e6', 'pe7-e5']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        # pined from diagonal - capture on the diagonal
        b = Board()
        b.place_piece('e4', PieceType.PAWN, Color.WHITE)
        b.place_piece('d5', PieceType.BISHOP, Color.BLACK)
        b.place_piece('f5', PieceType.PAWN, Color.BLACK)
        b.place_piece('h1', PieceType.KING, Color.WHITE)
        pawn = b.get_square('e4').piece
        actualMoves = pawn.calc_potential_moves_pinned(Direction.DOWN_RIGHT)
        expectedMoves = ['pe4-d5']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))

        # pinned from diagonal - capture en passant
        b = Board()
        b.place_piece('e5', PieceType.PAWN, Color.WHITE)
        b.place_piece('d5', PieceType.PAWN, Color.BLACK)
        b.place_piece('f6', PieceType.PAWN, Color.BLACK)
        b.place_piece('g3', PieceType.KING, Color.WHITE)
        b.place_piece('c7', PieceType.QUEEN, Color.BLACK)
        b.enPassantSquare = b.get_square('d5')
        pawn = b.get_square('e5').piece
        actualMoves = pawn.calc_potential_moves_pinned(Direction.DOWN_RIGHT)
        expectedMoves = ['pe5-d6']
        self.assertEqual(set(map(str, actualMoves)), set(expectedMoves))


