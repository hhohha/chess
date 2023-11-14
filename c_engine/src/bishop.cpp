#include "bishop.h"

Bishop::Bishop(PieceType kind, Color color, Square *square)
    : SlidingPiece(kind, color, square) {

    _isLight = true;
    _name = "B";
}

std::vector<Direction> Bishop::get_sliding_directions() {
    return _slidingDirections;
}
