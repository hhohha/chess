#include "king.h"
#include "constants.h"

King::King(Color color, Square *square)
    : Piece(PieceType::KING, color, square) {

    _isSliding = false;
    _isLight = true;
    _name = "K";
}

void King::recalculate() {
    throw std::runtime_error("King::recalculate() not implemented");
}

std::vector<Move *> King::calc_potential_moves_pinned(Direction directionFromKingToPinner) {
    throw std::runtime_error("King::calc_potential_moves_pinned() not implemented");
}

std::vector<Move *> King::get_legal_moves() {
    throw std::runtime_error("King::get_legal_moves() not implemented");
}