#pragma once

#include "constants.h"
#include "piece.h"

class King : Piece {
public:
    King(PieceType kind, Color color, Square *square);
};