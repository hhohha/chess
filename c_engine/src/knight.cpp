#include "knight.h"
#include "constants.h"

Knight::Knight(Color color, Square *square)
    : Piece(PieceType::KNIGHT, color, square) {

    _isSliding = false;
    _isLight = true;
    _name = "N";
}

void Knight::recalculate() {
    throw std::runtime_error("Knight::recalculate() not implemented");
}

std::vector<Move *> Knight::calc_potential_moves_pinned(Direction directionFromKingToPinner) {
    throw std::runtime_error("Knight::calc_potential_moves_pinned() not implemented");
}

std::vector<Move *> Knight::get_legal_moves() {
    throw std::runtime_error("Knight::get_legal_moves() not implemented");
}
    