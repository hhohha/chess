#pragma once

#include "constants.h"
#include "piece.h"

class Knight : Piece {
public:
    Knight(PieceType kind, Color color, Square *square);
};