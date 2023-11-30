#include "knight.h"
#include "constants.h"

Knight::Knight(Color color, Square *square)
    : Piece(PieceType::KNIGHT, color, square) {

    _isSliding = false;
    _isLight = true;
    _name = "N";
}
