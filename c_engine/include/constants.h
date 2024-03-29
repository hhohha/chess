#pragma once

#include <array>
#include <iostream>

enum class Color {WHITE, BLACK};
enum class PieceType {PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING};
enum class Direction {DOWN, UP, RIGHT, LEFT, DOWN_RIGHT, DOWN_LEFT, UP_RIGHT, UP_LEFT};

std::ostream &operator<<(std::ostream &os, const Color &color);
std::ostream &operator<<(std::ostream &os, const PieceType &pieceType);
std::ostream &operator<<(std::ostream &os, const Direction &direction);

constexpr auto FEN_INIT = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
constexpr auto FEN_TEST_A = "k7/8/8/8/8/8/3p4/7K w - - 98 0";
constexpr auto FEN_TEST_B = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8";
constexpr auto FEN_TEST_C = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0";
constexpr auto FEN_TEST_D = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1";
constexpr auto FEN_TEST_D_INVERTED = "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1";
constexpr auto FEN_TEST_E = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0";
constexpr auto FEN_TEST_E_NO_CASTLE = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w - - 0 0";
constexpr auto FEN_TEST_F = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10";

using PieceMap = std::array<int, 64>;

constexpr PieceMap BLACK_KING_MAP =
 {
    2, 2, 1, 0, 0, 1, 2, 2,
    2, 1, 1, 0, 0, 1, 2, 2,
    3, 2, 2, 0, 0, 2, 2, 3,
    3, 2, 2, 0, 0, 2, 2, 3,
    4, 3, 3, 1, 1, 3, 3, 4,
    4, 3, 3, 3, 3, 3, 3, 4,
    5, 5, 3, 3, 3, 3, 5, 5,
    5, 6, 4, 4, 4, 4, 6, 5
};

constexpr PieceMap WHITE_KING_MAP =
{
    5, 6, 4, 4, 4, 4, 6, 5,
    5, 5, 3, 3, 3, 3, 5, 5,
    4, 3, 3, 3, 3, 3, 3, 4,
    4, 3, 3, 1, 1, 3, 3, 4,
    3, 2, 2, 0, 0, 2, 2, 3,
    3, 2, 2, 0, 0, 2, 2, 3,
    2, 1, 1, 0, 0, 1, 2, 2,
    2, 2, 1, 0, 0, 1, 2, 2
};

constexpr PieceMap BLACK_KNIGHT_MAP =
{
    0, 1, 2, 2, 2, 2, 1, 0,
    1, 3, 4, 4, 4, 4, 3, 1,
    2, 4, 5, 5, 5, 5, 4, 2,
    2, 4, 5, 5, 5, 5, 4, 2,
    2, 4, 5, 5, 5, 5, 4, 2,
    2, 4, 5, 5, 5, 5, 4, 2,
    1, 3, 4, 4, 4, 4, 3, 1,
    0, 1, 2, 2, 2, 2, 1, 0
};

constexpr PieceMap WHITE_KNIGHT_MAP = BLACK_KNIGHT_MAP;


constexpr PieceMap BLACK_QUEEN_MAP =
{
    0, 2, 2, 3, 3, 2, 2, 0,
    2, 4, 4, 4, 4, 4, 4, 2,
    2, 4, 5, 5, 5, 5, 4, 2,
    3, 4, 5, 5, 5, 5, 4, 3,
    4, 4, 5, 5, 5, 5, 4, 3,
    2, 5, 5, 5, 5, 5, 4, 2,
    2, 4, 5, 5, 5, 4, 4, 2,
    0, 2, 2, 3, 3, 2, 2, 0
};

constexpr PieceMap WHITE_QUEEN_MAP =
{
    0, 2, 2, 3, 3, 2, 2, 0,
    2, 4, 5, 5, 5, 4, 4, 2,
    2, 5, 5, 5, 5, 5, 4, 2,
    4, 4, 5, 5, 5, 5, 4, 3,
    3, 4, 5, 5, 5, 5, 4, 3,
    2, 4, 5, 5, 5, 5, 4, 2,
    2, 4, 4, 4, 4, 4, 4, 2,
    0, 2, 2, 3, 3, 2, 2, 0,
};

constexpr PieceMap BLACK_PAWN_MAP =
{
    2, 2, 2, 2, 2, 2, 2, 2,
    6, 6, 6, 6, 6, 6, 6, 6,
    3, 3, 4, 5, 5, 4, 3, 3,
    3, 3, 3, 5, 5, 3, 2, 2,
    2, 2, 2, 5, 5, 2, 2, 2,
    3, 2, 1, 3, 3, 1, 2, 3,
    3, 4, 4, 0, 0, 4, 4, 3,
    2, 2, 2, 2, 2, 2, 2, 2
};

constexpr PieceMap WHITE_PAWN_MAP =
{
    2, 2, 2, 2, 2, 2, 2, 2,
    3, 4, 4, 0, 0, 4, 4, 3,
    3, 2, 1, 3, 3, 1, 2, 3,
    2, 2, 2, 5, 5, 2, 2, 2,
    3, 3, 3, 5, 5, 3, 2, 2,
    3, 3, 4, 5, 5, 4, 3, 3,
    6, 6, 6, 6, 6, 6, 6, 6,
    2, 2, 2, 2, 2, 2, 2, 2,
};

constexpr PieceMap BLACK_BISHOP_MAP =
{
    0, 1, 1, 1, 1, 1, 1, 0,
    1, 3, 3, 3, 3, 3, 3, 1,
    1, 3, 4, 5, 5, 4, 3, 1,
    1, 4, 4, 5, 5, 4, 4, 1,
    1, 3, 6, 5, 5, 6, 3, 1,
    1, 5, 5, 5, 5, 5, 5, 1,
    1, 5, 3, 3, 3, 3, 5, 1,
    2, 1, 1, 1, 1, 1, 1, 2
};

constexpr PieceMap WHITE_BISHOP_MAP =
{
    2, 1, 1, 1, 1, 1, 1, 2,
    1, 5, 3, 3, 3, 3, 5, 1,
    1, 5, 5, 5, 5, 5, 5, 1,
    1, 3, 6, 5, 5, 6, 3, 1,
    1, 4, 4, 5, 5, 4, 4, 1,
    1, 3, 4, 5, 5, 4, 3, 1,
    1, 3, 3, 3, 3, 3, 3, 1,
    0, 1, 1, 1, 1, 1, 1, 0
};

constexpr PieceMap BLACK_ROOK_MAP =
{
    4, 4, 4, 4, 4, 4, 4, 4,
    5, 6, 6, 6, 6, 6, 6, 5,
    0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 2, 2, 2, 2, 2, 0,
    2, 2, 4, 5, 5, 4, 2, 2
};

constexpr PieceMap WHITE_ROOK_MAP =
{
    2, 2, 4, 5, 5, 4, 2, 2,
    0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 2, 2, 2, 2, 2, 0,
    5, 6, 6, 6, 6, 6, 6, 5,
    4, 4, 4, 4, 4, 4, 4, 4
};



