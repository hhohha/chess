#pragma once

#include "piece.h"

class Rook : public SlidingPiece {
public:
    Rook(Color color, Square *square);

    void recalculate() override;
    std::vector<Move *> calc_potential_moves_pinned(Direction directionFromKingToPinner) override;
    std::vector<Move *> get_legal_moves() override;
};
