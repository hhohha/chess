#pragma once

#include "piece.h"

class Knight : public Piece {
public:
    Knight(Color color, Square *square);
    
    virtual void recalculate() override;
    virtual std::vector<Move *> calc_potential_moves_pinned(Direction directionFromKingToPinner) override;
    virtual std::vector<Move *> get_legal_moves() override;

};