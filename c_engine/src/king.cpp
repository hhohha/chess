#include "king.h"
#include "constants.h"
#include "move.h"
#include "square.h"
#include "board.h"
#include "utils.h"

King::King(Color color, Square *square)
    : Piece(PieceType::KING, color, square) {

    _isSliding = false;
    _isLight = false;
    _name = "K";
}

std::vector<Move *> King::calc_moves_avoiding_check(std::vector<Square *> *inaccessableSquares){
    std::vector<Move *> moves;
    for (auto move : _potentialMoves) {
        if (move->get_to_sqr()->is_attacked_by(invert_color(_color)))
            continue;
        if (inaccessableSquares != nullptr && std::find(inaccessableSquares->begin(), inaccessableSquares->end(), move->get_to_sqr()) != inaccessableSquares->end())
            continue;
        moves.push_back(move);
    }
    return moves;
}

void King::recalculate() {
    for (auto sqr : _attackedSquares) {
        auto vec = &sqr->get_attacked_by(_color);
        vec->erase(std::remove(vec->begin(), vec->end(), this), vec->end());
    }

    _attackedSquares.clear();
    for (auto move : _potentialMoves)
        delete move; 
    _potentialMoves.clear();

    for (Coordinate c : {Coordinate{1, 1}, Coordinate{1, 0}, Coordinate{1, -1}, Coordinate{0, 1},
        Coordinate{0, -1}, Coordinate{-1, 1}, Coordinate{-1, 0}, Coordinate{-1, -1}}) {

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

std::vector<Move *> King::calc_potential_moves_pinned(Direction directionFromKingToPinner) {
    throw std::runtime_error("King::calc_potential_moves_pinned() not implemented");
}

std::vector<Move *> King::get_legal_moves() {
    throw std::runtime_error("King::get_legal_moves() not implemented");
}