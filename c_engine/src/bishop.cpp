#include "bishop.h"

Bishop::Bishop(Color color, Square *square)
    : SlidingPiece(PieceType::BISHOP, color, square) {

    _isLight = true;
    _name = "B";
}

std::vector<Direction> Bishop::get_sliding_directions() const {
    return _slidingDirections;
}
