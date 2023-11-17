#include "pawn.h"
#include "constants.h"

 Pawn::Pawn(Color color, Square *square)
    : Piece(PieceType::PAWN, color, square),
    _moveOffset(color == Color::WHITE ? 1 : -1),
    _baseRow(color == Color::WHITE ? 1 : 6),
    _promotionRow(color == Color::WHITE ? 7 : 0),
    _enPassantRow(color == Color::WHITE ? 4 : 3) {

    _name = "p";
    _isSliding = false;
    _isLight = false;
}

    // virtual void recalculate() = 0;
    // virtual std::vector<Move *> calc_potential_moves() = 0;
    // virtual std::vector<Move *> get_legal_moves() = 0;



std::vector<Move *> Pawn::calc_potential_moves() {
    return std::vector<Move *>();
}

std::vector<Move *> Pawn::get_legal_moves() {
    return std::vector<Move *>();
}


void Pawn::recalculate() {}