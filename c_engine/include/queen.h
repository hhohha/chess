#pragma once

#include "piece.h"

class Queen : public SlidingPiece {
public:
    Queen(Color color, Square *square);
};