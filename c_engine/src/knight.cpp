#include "knight.h"
#include "constants.h"
#include "board.h"
#include "move.h"

Knight::Knight(Color color, Square *square)
    : Piece(PieceType::KNIGHT, color, square) {

    _isSliding = false;
    _isLight = true;
    _name = "N";
}

void Knight::recalculate() {
    for (auto sqr : _attackedSquares) {
        auto vec = &sqr->get_attacked_by(_color);
        vec->erase(std::remove(vec->begin(), vec->end(), this), vec->end());
    }

    _attackedSquares.clear();
    for (auto move : _potentialMoves)
        delete move;
    _potentialMoves.clear();

    for (Coordinate c : {Coordinate{2, 1}, Coordinate{2, -1}, Coordinate{-2, 1}, Coordinate{-2, -1},
        Coordinate{1, 2}, Coordinate{1, -2}, Coordinate{-1, 2}, Coordinate{-1, -2}}) {

        Coordinate newCoordinate = _square->get_coordinate() + c;
        auto sqr = _square->get_board()->get_square(newCoordinate);

        if (sqr != nullptr) {
            _attackedSquares.push_back(sqr);
            if (sqr->is_free() || sqr->get_piece()->_color != _color)
                _potentialMoves.push_back(new Move(this, sqr));
        }
    }

    for (auto sqr : _attackedSquares)
        sqr->get_attacked_by(_color).push_back(this);
}

std::vector<Move *> Knight::calc_potential_moves_pinned(Direction directionFromKingToPinner) {
    return {};
}

std::vector<Move *> Knight::get_legal_moves() {
    throw std::runtime_error("Knight::get_legal_moves() not implemented");
}
