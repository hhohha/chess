#include "queen.h"
#include "constants.h"

Queen::Queen(Color color, Square *square) :
    SlidingPiece(
        PieceType::QUEEN,
        color,
        square,
        {Direction::DOWN_RIGHT, Direction::DOWN_LEFT, Direction::UP_RIGHT, Direction::UP_LEFT, Direction::UP,
            Direction::DOWN, Direction::LEFT, Direction::RIGHT}) {

    _isLight = false;
    _name = "Q";
}
