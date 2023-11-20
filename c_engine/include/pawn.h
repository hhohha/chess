#pragma once

#include "constants.h"
#include "piece.h"


class Square;

class Pawn : public Piece {
public:
    Pawn(Color color, Square *square);

    const int _moveOffset;
    const unsigned int _baseRow;
    const unsigned int _promotionRow;
    const unsigned int _enPassantRow;

    std::vector<Move *> calc_potential_moves();
    std::vector<Move *> get_legal_moves() override;
    void recalculate() override;
};
