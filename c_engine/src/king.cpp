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
    _attackedSquares.reserve(8);
    _potentialSquares.reserve(8);
}

std::vector<Square *> King::calc_squares_avoiding_check(std::vector<Square *> *inaccessableSquares){
    std::vector<Square *> squares;
    for (auto square : _potentialSquares) {
        if (square->is_attacked_by(invert_color(_color)))
            continue;
        if (inaccessableSquares != nullptr && std::find(inaccessableSquares->begin(), inaccessableSquares->end(), square) != inaccessableSquares->end())
            continue;
        squares.push_back(square);
    }
    return squares;
}

void King::recalculate() {
    for (auto sqr : _attackedSquares) {
        auto& attackedBy = sqr->get_attacked_by(_color);
        attackedBy.erase(std::find(attackedBy.begin(), attackedBy.end(), this));
    }

    _attackedSquares.clear();
    _potentialSquares.clear();

    for (Coordinate c : {Coordinate{1, 1}, Coordinate{1, 0}, Coordinate{1, -1}, Coordinate{0, 1},
        Coordinate{0, -1}, Coordinate{-1, 1}, Coordinate{-1, 0}, Coordinate{-1, -1}}) {

        Coordinate newCoordinate = _square->get_coordinate() + c;
        auto sqr = _square->get_board()->get_square(newCoordinate);

        if (sqr != nullptr) {
            _attackedSquares.push_back(sqr);
            if (sqr->is_free() || sqr->get_piece()->_color != _color)
                _potentialSquares.push_back(sqr);
        }
    }

    for (auto sqr : _attackedSquares)
        sqr->get_attacked_by(_color).push_back(this);
}

std::vector<Square *> King::calc_potential_squares_pinned(Direction directionFromKingToPinner) {
    throw std::runtime_error("King cannot be pinned");
}