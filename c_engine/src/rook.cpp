#include "rook.h"
#include "constants.h"

Rook::Rook(Color color, Square *square) :
    SlidingPiece(
        PieceType::ROOK,
        color,
        square,
        {Direction::DOWN, Direction::LEFT, Direction::RIGHT, Direction::UP}) {

    _isLight = false;
    _name = "R";
}

std::vector<Move *> Rook::get_legal_moves() {
    throw std::runtime_error("Rook::get_legal_moves() not implemented");
}