#pragma once

#include "piece.h"

class Rook : public SlidingPiece {
public:
    Rook(Color color, Square *square);
};
