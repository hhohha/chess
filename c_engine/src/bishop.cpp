#include "bishop.h"

Bishop::Bishop(Color color, Square *square) :
    SlidingPiece(
        PieceType::BISHOP,
        color,
        square,
        {Direction::DOWN_RIGHT, Direction::DOWN_LEFT, Direction::UP_RIGHT, Direction::UP_LEFT}) {

    _isLight = true;
    _name = "B";
}
