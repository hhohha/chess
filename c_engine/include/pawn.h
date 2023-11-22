#pragma once

#include <stdexcept>

#include "piece.h"


class Square;

class Pawn : public Piece {
public:
    Pawn(Color color, Square *square);

    const int _moveOffset;
    const unsigned int _baseRow;
    const unsigned int _promotionRow;
    const unsigned int _enPassantRow;

    virtual void recalculate() override;

    virtual std::vector<Move *> calc_potential_moves_pinned(Direction directionFromKingToPinner) override;

    virtual std::vector<Move *> get_legal_moves() override;
};
