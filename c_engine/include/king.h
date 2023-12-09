#pragma once

#include "piece.h"
#include <vector>

class King : public Piece {
public:
    King(Color color, Square *square);
    void recalculate() override;
    std::vector<Move *> calc_potential_moves_pinned(Direction directionFromKingToPinner) override;
    std::vector<Move *> get_legal_moves() override;
    std::vector<Move *> calc_moves_avoiding_check(std::vector<Square *> * inaccessableSquares = nullptr);
};