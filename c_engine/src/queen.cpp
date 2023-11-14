#include "queen.h"

Queen::Queen(PieceType kind, Color color, Square *square)
    : SlidingPiece(kind, color, square) {

    _isLight = false;
    _name = "Q";
}

std::vector<Direction> Queen::get_sliding_directions() {
    return _slidingDirections;
}
