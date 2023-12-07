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
}

std::vector<Move *> Pawn::get_potential_moves() {
    std::vector<Move *> moves;

    for (auto move : get_forward_moves()) // move forward
        moves.push_back(move);

    for (auto move : get_capture_moves(-1)) // capture to the left
        moves.push_back(move);

    for (auto move : get_capture_moves(1)) // capture to the right
        moves.push_back(move);

    auto enPassantMove = get_en_passant_move(); // en passant
    if (enPassantMove != nullptr)
        moves.push_back(enPassantMove);

    return moves;
}

Move * Pawn::get_en_passant_move() {
    // check the possibility that the pawn can take en passant
    // if en passant is possible, the enPassantSqr is the square behind the pawn
    auto enPassantSqr = _square->get_board()->_enPassantPawnSquare;
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

    auto destSquare = _square->get_board()->get_square(enPassantSqr->get_col(), _square->get_row() + _moveOffset);

    auto move = new Move(this, destSquare);
    move->mark_as_en_passant();
    return move;
}

bool Pawn::is_en_passant_pin() {
    // handles a very special case, in which the pawn is technically not pinned, but en passant capture would
    // still expose the king
    // e.g. white:  pe5, Kg5, black: Rb5, pd7 and black moves pd7-d5 - then "exd6 e.p."" is not possible 

    auto enPassantSqr = _square->get_board()->_enPassantPawnSquare;
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

std::vector<Move *> Pawn::get_capture_moves(int colOffset) {
    std::vector<Move *> moves;

    auto sqr = _square->get_board()->get_square(_square->get_coordinate() + Coordinate{colOffset, _moveOffset});
    if (sqr != nullptr && !sqr->is_free() && sqr->get_piece()->_color != _color)
        for (auto move : generate_pawn_moves(sqr))
            moves.push_back(move);

    return moves;
}

std::vector<Move *> Pawn::get_forward_moves() {
    std::vector<Move *> moves;

    // if the square in front if the pawn is free, it can move there
    auto sqr = _square->get_board()->get_square(_square->get_coordinate() + Coordinate{0, _moveOffset});
    ASSERT(sqr != nullptr, "square in front of pawn is not valid");
    if (sqr->is_free()) {
        for (auto move : generate_pawn_moves(sqr))
            moves.push_back(move);

        // if the pawn is on its base row, it can move two squares forward
        if (_square->get_coordinate().row == _baseRow) {
            sqr = _square->get_board()->get_square(_square->get_coordinate() + Coordinate{0, 2 * _moveOffset});
            ASSERT(sqr != nullptr, "square two squares in front of pawn is not valid");
            if (sqr->is_free())
                for (auto move : generate_pawn_moves(sqr))
                    moves.push_back(move);
        }      
    }

    return moves;
}

std::vector<Move *> Pawn::generate_pawn_moves(Square *targetSqr) {
    // if the pawn is about to promote, generate all possible promotions
    if (targetSqr->get_row() == _promotionRow) {
        return {
            new Move(this, targetSqr, PieceType::QUEEN),
            new Move(this, targetSqr, PieceType::ROOK),
            new Move(this, targetSqr, PieceType::BISHOP),
            new Move(this, targetSqr, PieceType::KNIGHT)
        };
    } else {
        return {new Move(this, targetSqr)};
    }
}


void Pawn::recalculate() {
    //throw std::runtime_error("not implemented");
}

std::vector<Move *> Pawn::calc_potential_moves_pinned(Direction directionFromKingToPinner) {
    throw std::runtime_error("not implemented");
}

std::vector<Move *> Pawn::get_legal_moves() {
    throw std::runtime_error("not implemented");
}