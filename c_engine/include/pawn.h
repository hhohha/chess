#pragma once

#include <stdexcept>

#include "piece.h"

class Square;

class Pawn : public Piece {
public:
    Pawn(Color color, Square *square);

    virtual void recalculate() override;

    virtual std::vector<Square *> calc_potential_squares_pinned(Direction directionFromKingToPinner) override;

    std::vector<Square *> get_potential_squares() override;

    //std::vector<Move *> generate_pawn_moves(Square *targetSqr);
private:
    std::vector<Square *> get_forward_squares();
    std::vector<Square *> get_capture_squares(int colOffset);
    Square * get_en_passant_square();
    bool is_en_passant_pin();

    const int _moveOffset;
    const int _baseRow;
    const int _promotionRow;
    const int _enPassantRow;
};
