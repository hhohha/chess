#include <cassert>

#include "move.h"
#include "piece.h"
#include "square.h"
#include "utils.h"

Move::Move(Piece *piece, Square *toSqr, std::optional<PieceType> newPiece)
: _piece(piece),
  _toSqr(toSqr),
  _newPiece(newPiece) {

    assert(piece->get_square() != nullptr);
    _fromSqr = piece->get_square();
    
    // if the piece is a pawn and it's being promoted, the newPiece must be specified
    assert(newPiece.has_value() || (piece->_kind != PieceType::PAWN || toSqr->get_coordinate().row != (piece->_color == Color::WHITE ? 7 : 0)));


    
}

bool Move::operator==(Move &other) {
    return _piece == other._piece && _fromSqr == other._fromSqr && _toSqr == other._toSqr && _newPiece == other._newPiece;
}

bool Move::is_promotion() {
    return _newPiece.has_value();
}

bool Move::is_castling() {
    return _piece->_kind == PieceType::KING && abs(_fromSqr->get_coordinate().col - _toSqr->get_coordinate().col) == 2;
}

std::string Move::str() {
    return _piece->str() + "-" + _toSqr->str() + (is_promotion() ? piece_type_to_letter(_newPiece.value()) : "");
}