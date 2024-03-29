from __future__ import annotations
from enum import Enum


class Color(Enum):
    WHITE = 0
    BLACK = 1

    def invert(self) -> Color:
        return Color.BLACK if self == Color.WHITE else Color.WHITE

class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7

class Result(Enum):
    BLACK_WON = 'Black has won!'
    WHITE_WON = 'White has won!'
    DRAW_STALEMATE = 'Draw by stalemate!'
    DRAW_50_MOVES = 'Draw by 50 moves rule!'
    DRAW_3_REPETITIONS = 'Draw by 3 repetitions!'
    DRAW_INSUFFICIENT_MATERIAL = 'Draw by insufficient material!'
    DRAW_AGREEMENT = 'Draw by agreement!'

FEN_INIT = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
FEN_A = 'k7/8/8/8/8/8/3p4/7K w - - 98 0'
FEN_B = 'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8'
FEN_C = '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0'
FEN_D = 'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1'
FEN_D_INVERTED = 'r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1'
FEN_E = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0'
FEN_E_NO_CASTLE = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w - - 0 0'
FEN_F = 'r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10'

COLOR_BG_LIGHT_BASIC =      '#EDEAE0'
COLOR_BG_LIGHT_HLIGHTED_1 = '#8DCA80'
COLOR_BG_LIGHT_HLIGHTED_2 = '#6DFA60'

COLOR_BG_DARK_BASIC =       '#8F9779'
COLOR_BG_DARK_HLIGHTED_1 =  '#5F9749'
COLOR_BG_DARK_HLIGHTED_2 =  '#2FA719'

COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_WHITE = '\x1b[0m'
