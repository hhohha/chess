#pragma once

#include "piece.h"

class Knight : public Piece {
public:
    Knight(Color color, Square *square);
    
    virtual void recalculate() override;
    virtual std::vector<Square *> calc_potential_squares_pinned(Direction directionFromKingToPinner) override;
};