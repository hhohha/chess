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

void Pawn::recalculate() {
    throw std::runtime_error("not implemented");
}

std::vector<Move *> Pawn::calc_potential_moves_pinned(Direction directionFromKingToPinner) {
    throw std::runtime_error("not implemented");
}

std::vector<Move *> Pawn::get_legal_moves() {
    throw std::runtime_error("not implemented");
}