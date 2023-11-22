#pragma once

#include <iostream>

enum class Color {WHITE, BLACK};
enum class PieceType {PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING};
enum class Direction {DOWN, UP, RIGHT, LEFT, DOWN_RIGHT, DOWN_LEFT, UP_RIGHT, UP_LEFT};

std::ostream &operator<<(std::ostream &os, const Color &color);
std::ostream &operator<<(std::ostream &os, const PieceType &pieceType);
std::ostream &operator<<(std::ostream &os, const Direction &direction);
