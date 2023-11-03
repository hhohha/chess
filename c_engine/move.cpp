#include "move.h"
#include "piece.h"
#include "square.h"
#include "utils.h"

Move::Move(Piece *piece, Square *toSqr)
: _piece(piece),
    _toSqr(toSqr) {

    _fromSqr = piece->get_square();

}

bool Move::is_promotion() {
    return _newPiece.has_value();
}

bool Move::is_castling() {
    return _piece->_kind == PieceType::KING && abs(_fromSqr->_colIdx - _toSqr->_colIdx) == 2;
}

std::string Move::str() {
    return _piece->str() + _fromSqr->str() + "-" + _toSqr->str() + (is_promotion() ? piece_type_to_letter(_newPiece.value()) : "");
}