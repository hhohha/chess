#include "rook.h"
#include "constants.h"

Rook::Rook(Color color, Square *square) :
    SlidingPiece(
        PieceType::ROOK,
        color,
        square,
        {Direction::DOWN, Direction::LEFT, Direction::RIGHT, Direction::UP}) {

    _isLight = false;
    _name = "R";
    _value = 5000;
    _attackedSquares.reserve(14);
    _potentialSquares.reserve(14);
}