#include <cassert>

#include "move.h"
#include "piece.h"
#include "square.h"
#include "utils.h"

Move::Move(Piece *piece, Square *toSqr)
: _piece(piece),
  _toSqr(toSqr) {

    assert(_fromSqr != nullptr);

    _fromSqr = piece->get_square();

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
    return _piece->str() + _fromSqr->str() + "-" + _toSqr->str() + (is_promotion() ? piece_type_to_letter(_newPiece.value()) : "");
}