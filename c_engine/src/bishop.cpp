#include "bishop.h"

Bishop::Bishop(Color color, Square *square) :
    SlidingPiece(
        PieceType::BISHOP,
        color,
        square,
        {Direction::DOWN_RIGHT, Direction::DOWN_LEFT, Direction::UP_RIGHT, Direction::UP_LEFT}) {

    _attackedSquares.reserve(13);
    _potentialSquares.reserve(13);
    _isLight = true;
    _name = "B";
    _value = 3;
}
