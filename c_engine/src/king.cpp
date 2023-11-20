#include "king.h"

King::King(PieceType kind, Color color, Square *square)
    : Piece(kind, color, square) {

    _isSliding = false;
    _isLight = true;
    _name = "K";
}