#include "knight.h"
#include "constants.h"
#include "board.h"
#include "move.h"

Knight::Knight(Color color, Square *square)
    : Piece(PieceType::KNIGHT, color, square) {

    _isSliding = false;
    _isLight = true;
    _name = "N";
    _attackedSquares.reserve(8);
    _potentialSquares.reserve(8);
}

void Knight::recalculate() {
    for (auto sqr : _attackedSquares) {
        // QQQ
        //auto& vec = sqr->get_attacked_by(_color);
        //vec.erase(std::find(vec.begin(), vec.end(), this));

        auto vec = &sqr->get_attacked_by(_color);
        vec->erase(std::find(vec->begin(), vec->end(), this));
    }

    _attackedSquares.clear();
    _potentialSquares.clear();

    for (Coordinate c : {Coordinate{2, 1}, Coordinate{2, -1}, Coordinate{-2, 1}, Coordinate{-2, -1},
        Coordinate{1, 2}, Coordinate{1, -2}, Coordinate{-1, 2}, Coordinate{-1, -2}}) {

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

std::vector<Square *> Knight::calc_potential_squares_pinned(Direction directionFromKingToPinner) {
    return {};
}
