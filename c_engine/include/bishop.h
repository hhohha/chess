#pragma once

#include "piece.h"

class Bishop : public SlidingPiece {
public:
    Bishop(Color color, Square *square);
    bool _isLight = true;
};
