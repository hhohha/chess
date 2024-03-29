#include "move.h"
#include "piece.h"
#include "square.h"
#include "utils.h"


Move::Move(Piece *piece, Square *toSqr, std::optional<PieceType> newPiece)
: _piece(piece),
  _toSqr(toSqr),
  _newPiece(newPiece) {

    ASSERT(piece->get_square() != nullptr, "piece has no square");
    _fromSqr = piece->get_square();

    // if the piece is a pawn and it's being promoted, the newPiece must be specified
    ASSERT(newPiece.has_value() || (piece->_kind != PieceType::PAWN || toSqr->get_coordinate().row != (piece->_color == Color::WHITE ? 7 : 0)),
        "a move must specify the new piece iff it's a promotion");
}

bool Move::operator==(Move &other) const {
    return _piece == other._piece && _fromSqr == other._fromSqr && _toSqr == other._toSqr && _newPiece == other._newPiece;
}

bool Move::is_promotion() const {
    return _newPiece.has_value();
}

bool Move::is_castling() const {
    return _piece->_kind == PieceType::KING && abs(_fromSqr->get_coordinate().col - _toSqr->get_coordinate().col) == 2;
}

std::string Move::str() const {
    return _piece->str().substr(0, 1) + _fromSqr->str() + "-" + _toSqr->str() + (is_promotion() ? piece_type_to_letter(_newPiece.value()) : "");
}

std::ostream& operator << (std::ostream &os, const Move &move) {
    return os << move.str();
}

bool operator==(Move &lhs, Move &rhs) {
    return lhs._piece == rhs._piece && lhs._fromSqr == rhs._fromSqr && lhs._toSqr == rhs._toSqr && lhs._newPiece == rhs._newPiece;
}
