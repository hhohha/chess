#include "rook.h"

Rook::Rook(PieceType kind, Color color, Square *square)
    : SlidingPiece(kind, color, square) {

    _isLight = false;
    _name = "R";
}

std::vector<Direction> Rook::get_sliding_directions() {
    return _slidingDirections;
}
