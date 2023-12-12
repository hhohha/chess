#pragma once

#include <stdexcept>

#include "piece.h"

class Square;

class Pawn : public Piece {
public:
    Pawn(Color color, Square *square);

    virtual void recalculate() override;

    virtual std::vector<Move *> calc_potential_moves_pinned(Direction directionFromKingToPinner) override;

    virtual std::vector<Move *> get_legal_moves() override;

    std::vector<Move *> get_potential_moves();

    std::vector<Move *> generate_pawn_moves(Square *targetSqr);
private:
    std::vector<Move *> get_forward_moves();
    std::vector<Move *> get_capture_moves(int colOffset);
    Move * get_en_passant_move();
    bool is_en_passant_pin();

    const int _moveOffset;
    const int _baseRow;
    const int _promotionRow;
    const int _enPassantRow;
};
