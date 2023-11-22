#pragma once

#include "piece.h"

class King : Piece {
public:
    King(PieceType kind, Color color, Square *square);
};