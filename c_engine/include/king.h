#pragma once

#include "piece.h"
#include <vector>

class King : public Piece {
public:
    King(Color color, Square *square);
    void recalculate() override;
    std::vector<Square *> calc_potential_squares_pinned(Direction directionFromKingToPinner) override;
    std::vector<Square *> calc_squares_avoiding_check(std::vector<Square *> * inaccessableSquares = nullptr);
};