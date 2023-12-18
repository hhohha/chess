#include "pawn.h"
#include "board.h"
#include "constants.h"
#include "move.h"

 Pawn::Pawn(Color color, Square *square)
    : Piece(PieceType::PAWN, color, square),
    _moveOffset(color == Color::WHITE ? 1 : -1),
    _baseRow(color == Color::WHITE ? 1 : 6),
    _promotionRow(color == Color::WHITE ? 7 : 0),
    _enPassantRow(color == Color::WHITE ? 4 : 3) {

    _name = "p";
    _isSliding = false;
    _isLight = false;
    _attackedSquares.reserve(2);
}

std::vector<Square *> Pawn::get_potential_squares() {
    std::vector<Square *> squares;

    for (auto square : get_forward_squares()) // move forward
        squares.push_back(square);

    for (auto square : get_capture_squares(-1)) // capture to the left
        squares.push_back(square);

    for (auto square : get_capture_squares(1)) // capture to the right
        squares.push_back(square);

    auto enPassantSquare = get_en_passant_square(); // en passant
    if (enPassantSquare != nullptr)
        squares.push_back(enPassantSquare);

    return squares;
}

Square * Pawn::get_en_passant_square() {
    // check the possibility that the pawn can take en passant
    // if en passant is possible, the enPassantSqr is the square behind the pawn
    auto enPassantSqr = _square->get_board()->get_en_passant_pawn_square();
    if (enPassantSqr == nullptr)
        return nullptr;

    // the pawn must be on the right row (4 for white, 3 for black indexed from 0)
    if (_square->get_row() != _enPassantRow)
        return nullptr;

    // the pawn must be on the neighboring column of the en passant square
    if (abs(_square->get_col() - enPassantSqr->get_col()) != 1)
        return nullptr;

    if (is_en_passant_pin())
        return nullptr;

    return _square->get_board()->get_square(enPassantSqr->get_col(), _square->get_row() + _moveOffset);
}

bool Pawn::is_en_passant_pin() {
    // handles a very special case, in which the pawn is technically not pinned, but en passant capture would
    // still expose the king
    // e.g. white:  pe5, Kg5, black: Rb5, pd7 and black moves pd7-d5 - then "exd6 e.p."" is not possible 

    auto enPassantSqr = _square->get_board()->get_en_passant_pawn_square();
    ASSERT(enPassantSqr != nullptr, "en passant square is null");
    ASSERT(enPassantSqr->get_piece() != nullptr, "en passant square is free");
    ASSERT(enPassantSqr->get_piece()->_kind == PieceType::PAWN, "en passant square is not occupied by a pawn");
    ASSERT(enPassantSqr->get_piece()->_color != _color, "en passant square is occupied by a pawn of the same color");

    auto king = _square->get_board()->get_king(_color);
    if (king == nullptr)  // cannot happen in a regular game
        return false;

    // the special pin can only occur on the en passant row
    if (king->get_square()->get_row() != enPassantSqr->get_row())
        return false;

    // what is the direction of the potential pin (from king to pinner)
    auto direction = king->get_square()->get_col() > enPassantSqr->get_col() ? Direction::LEFT : Direction::RIGHT;

    // on the way from own king towards the pinner, the first piece must be the own pawn (that wants to take en passant)
    // or the opponent's pawn
    auto firstSquare = _square->get_board()->find_first_occupied_square_in_dir(king->get_square(), direction);
    if (firstSquare == nullptr || (firstSquare != enPassantSqr && firstSquare->get_piece() != this))
        return false;

    // the second piece must be the other pawn (taker or being taken) and must be right next to the first piece
    auto secondSquare = _square->get_board()->
        get_square(firstSquare->get_col() + (direction == Direction::RIGHT ? 1 : -1), firstSquare->get_row());
    if (secondSquare == nullptr || secondSquare->get_piece() == nullptr)
        return false;

    // now check that those two pawns have been found
    bool firstSquareIsEnPassant = firstSquare == enPassantSqr && secondSquare->get_piece() == this;
    bool secondSquareIsEnPassant = firstSquare->get_piece() == this && secondSquare == enPassantSqr;
    if (!(firstSquareIsEnPassant || secondSquareIsEnPassant))
        return false;


    // the third piece must be the opponent's queen or rook
    auto thirdSquare = _square->get_board()->find_first_occupied_square_in_dir(secondSquare, direction);
    if (thirdSquare == nullptr)
        return false;

    // the third piece must be the opponent's queen or rook
    if (thirdSquare->get_piece()->_color == _color)
        return false;
    if (thirdSquare->get_piece()->_kind != PieceType::QUEEN && thirdSquare->get_piece()->_kind != PieceType::ROOK)
        return false;

    // all conditions are met, the pawn is "pinned"
    return true;
}

std::vector<Square *> Pawn::get_capture_squares(int colOffset) {
    std::vector<Square *> squares;

    auto sqr = _square->get_board()->get_square(_square->get_coordinate() + Coordinate{colOffset, _moveOffset});
    if (sqr != nullptr && !sqr->is_free() && sqr->get_piece()->_color != _color)
        squares.push_back(sqr);
        //for (auto move : generate_pawn_moves(sqr))
        //    moves.push_back(move);

    return squares;
}

std::vector<Square *> Pawn::get_forward_squares() {
    std::vector<Square *> squares;

    // if the square in front if the pawn is free, it can move there
    auto sqr = _square->get_board()->get_square(_square->get_coordinate() + Coordinate{0, _moveOffset});
    ASSERT(sqr != nullptr, "square in front of pawn is not valid");
    if (sqr->is_free()) {
        //for (auto square : generate_pawn_moves(sqr))
        squares.push_back(sqr);

        // if the pawn is on its base row, it can move two squares forward
        if (_square->get_coordinate().row == _baseRow) {
            sqr = _square->get_board()->get_square(_square->get_coordinate() + Coordinate{0, 2 * _moveOffset});
            ASSERT(sqr != nullptr, "square two squares in front of pawn is not valid");
            if (sqr->is_free())
                //for (auto move : generate_pawn_moves(sqr))
                    squares.push_back(sqr);
        }      
    }

    return squares;
}

void Pawn::recalculate() {
    // pawn doesn't store potential moves, only attacked squares (possible todo)

    for (auto sqr : _attackedSquares) {
        // QQQ
        // auto& attackedBy = sqr->get_attacked_by(_color);
        // attackedBy.erase(std::find(attackedBy.begin(), attackedBy.end(), this));
        auto attackedBy = &sqr->get_attacked_by(_color);
        attackedBy->erase(std::find(attackedBy->begin(), attackedBy->end(), this));

    }
    _attackedSquares.clear();

    if (_square->get_col() == 0)
        _attackedSquares.push_back(_square->get_board()->get_square(1, _square->get_row() + _moveOffset));
    else if (_square->get_col() == 7)
        _attackedSquares.push_back(_square->get_board()->get_square(6, _square->get_row() + _moveOffset));
    else {
        _attackedSquares.push_back(_square->get_board()->get_square(_square->get_col() - 1, _square->get_row() + _moveOffset));
        _attackedSquares.push_back(_square->get_board()->get_square(_square->get_col() + 1, _square->get_row() + _moveOffset));
    }

    for (auto sqr : _attackedSquares)
        sqr->get_attacked_by(_color).push_back(this);
}

std::vector<Square *> Pawn::calc_potential_squares_pinned(Direction directionFromKingToPinner) {
    // the piece is pinned in the given direction, it can potentially still move in the pin and the opposite direction

    if (directionFromKingToPinner == Direction::RIGHT || directionFromKingToPinner == Direction::LEFT)
        // a pawn pinned from side can never move
        return {};

    if (directionFromKingToPinner == Direction::UP || directionFromKingToPinner == Direction::DOWN)
        // a pawn pinned from front or back can only move forward
        return get_forward_squares();

    auto enPassantSqr = _square->get_board()->get_en_passant_pawn_square();
    if (directionFromKingToPinner == Direction::UP_RIGHT || directionFromKingToPinner == Direction::DOWN_LEFT) {
        // pawn pinned diagonally can possibly capture in the pin direction
        std::vector<Square *> squares = get_capture_squares(_moveOffset);

        // a diagonally pinned pawn can even capture en passant, en passant pin special pin is impossible in this case
        // as the pawn is already pinned
        if (enPassantSqr != nullptr && _square->get_row() == _enPassantRow && enPassantSqr->get_idx() - _square->get_idx() == _moveOffset) {
            squares.push_back(_square->get_board()->get_square(enPassantSqr->get_col(), _square->get_row() + _moveOffset));
            //moves.back()->mark_as_en_passant();
        }

        return squares;
    }

    // directionFromKingToPinner == Direction::UP_LEFT || directionFromKingToPinner == Direction::DOWN_RIGHT
    // capture in the other direction is analogous to the previous case
    std::vector<Square *> squares = get_capture_squares(-_moveOffset);

    if (enPassantSqr != nullptr && _square->get_row() == _enPassantRow && _square->get_idx() - enPassantSqr->get_idx() == _moveOffset) {
        squares.push_back(_square->get_board()->get_square(enPassantSqr->get_col(), _square->get_row() + _moveOffset));
        //moves.back()->mark_as_en_passant();
    }

    return squares;
}