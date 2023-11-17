#include <algorithm>
#include <cassert>

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

std::string Piece::str() {
    return _name + _square->str();
}

SlidingPiece::SlidingPiece(PieceType kind, Color color, Square *square)
    : Piece(kind, color, square) {

    _isSliding = true;
}

void SlidingPiece::recalculate() {
    //for (auto sqr : _attackedSquares) {
        //auto vec = &sqr->get_attacked_by(_color);
        //vec->erase(std::remove(vec->begin(), vec->end(), this), vec->end());
    //}

    _attackedSquares.clear();
    _potentialMoves.clear();

    for (auto direction : get_sliding_directions()) {
        Coordinate c{0, 0};
        
        while (true) {
            move_in_direction(c, direction);
            auto sqr = _square->get_board()->get_square(c);

            if (sqr == nullptr) {
                break; //reached the edge of the board
            }

            if (sqr->is_free()) {
                _attackedSquares.push_back(sqr);
                _potentialMoves.push_back(new Move(this, sqr));
            } else if (sqr->get_piece()->_color != _color) {
                _attackedSquares.push_back(sqr);
                _potentialMoves.push_back(new Move(this, sqr));
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
std::vector<Move *> SlidingPiece::calc_potential_moves_pinned(Direction directionFromKingToPinner) {

    if (std::find(get_sliding_directions().begin(), get_sliding_directions().end(), directionFromKingToPinner) != get_sliding_directions().end())
        return {};

    std::vector<Move *> potentialMoves;
    Coordinate coordinate(_square->get_coordinate());

    while (true) {
        // the piece can move towards the king but cannot capture
        move_in_direction(coordinate, reverse_direction(directionFromKingToPinner));
        Square *sqr = _square->get_board()->get_square(coordinate);
        assert(sqr != nullptr);

        if (sqr->get_piece() != nullptr) {
            assert(sqr->get_piece()->_color == _color && sqr->get_piece()->_kind == PieceType::KING);
            break;
        }

        
        potentialMoves.push_back(new Move(this, sqr)); // TODO: use emplace_back
    }

    while (true) {
        // the piece can move in the direction of the pinner including its capture
        move_in_direction(coordinate, directionFromKingToPinner);
        Square *sqr = _square->get_board()->get_square(coordinate);
        assert(sqr != nullptr);

        potentialMoves.push_back(new Move(this, sqr)); // TODO: use emplace_back
        if (sqr->get_piece() != nullptr) {
            assert(sqr->get_piece()->_color != _color && sqr->get_piece()->_isSliding);
            break;
        }
    }

    return potentialMoves;
}


std::vector<Move *> SlidingPiece::get_legal_moves() {

}


