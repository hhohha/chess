#include <algorithm>
#include <stdexcept>


#include "piece.h"
#include "board.h"
#include "utils.h"
#include "square.h"
#include "move.h"

Piece::Piece(PieceType kind, Color color, Square *square)
    : _kind(kind),
      _color(color),
      _square(square) {}

Square *Piece::get_square() {
    return _square;
}

SlidingPiece::SlidingPiece(PieceType kind, Color color, Square *square, const std::vector<Direction> slidingDirections) : 
    Piece(kind, color, square),
    _slidingDirections(slidingDirections) {

    _isSliding = true;
}

void SlidingPiece::recalculate() {
    for (auto sqr : _attackedSquares) {
        auto vec = &sqr->get_attacked_by(_color);
        vec->erase(std::remove(vec->begin(), vec->end(), this), vec->end());
    }

    _attackedSquares.clear();
    _potentialSquares.clear();

    for (auto direction : get_sliding_directions()) {
        Coordinate c(_square->get_coordinate());
        
        while (true) {
            move_in_direction(c, direction);
            auto sqr = _square->get_board()->get_square(c);

            if (sqr == nullptr) {
                break; //reached the edge of the board
            }

            if (sqr->is_free()) {
                _attackedSquares.push_back(sqr);
                _potentialSquares.push_back(sqr);
            } else if (sqr->get_piece()->_color != _color) {
                _attackedSquares.push_back(sqr);
                _potentialSquares.push_back(sqr);
                break;
            } else {
                _attackedSquares.push_back(sqr);
                break;
            }
        }
    }

    for (auto sqr : _attackedSquares)
        sqr->get_attacked_by(_color).push_back(this);
}

/*
 * what are potential moves if the piece is pinned in the given direction?
 */
std::vector<Square *> SlidingPiece::calc_potential_squares_pinned(Direction directionFromKingToPinner) {

    if (std::find(get_sliding_directions().begin(), get_sliding_directions().end(), directionFromKingToPinner) == get_sliding_directions().end())
        return {};

    std::vector<Square *> potentialSquares;
    Coordinate coordinate(_square->get_coordinate());

    while (true) {
        // the piece can move towards the king but cannot capture
        move_in_direction(coordinate, reverse_direction(directionFromKingToPinner));
        Square *sqr = _square->get_board()->get_square(coordinate);
        ASSERT(sqr != nullptr, "moving towards king but reached the edge of the board");

        if (sqr->get_piece() != nullptr) {
            ASSERT(sqr->get_piece()->_color == _color && sqr->get_piece()->_kind == PieceType::KING,
                "moving towards own king but reached a different piece");
            break;
        }
        
        potentialSquares.push_back(sqr);
    }

    coordinate = _square->get_coordinate();

    while (true) {
        // the piece can move in the direction of the pinner including its capture
        move_in_direction(coordinate, directionFromKingToPinner);
        Square *sqr = _square->get_board()->get_square(coordinate);
        ASSERT(sqr != nullptr, "moving towards the pinner but reached the edge of the board");

        potentialSquares.push_back(sqr);
        if (sqr->get_piece() != nullptr) {
            ASSERT(sqr->get_piece()->_color != _color && sqr->get_piece()->_isSliding,
                "moving towards the pinner but reached a different piece");
            break;
        }
    }

    return potentialSquares;
}


std::ostream& operator << (std::ostream &os, const Piece &piece) {
    os << piece.str();
    return os;
}