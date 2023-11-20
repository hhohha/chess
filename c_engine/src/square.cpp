#include <cassert>

#include "square.h"

Square::Square(int idx, Board *board)
: _idx(idx),
    _coordinate({idx % 8, idx / 8}),
    _board(board) {

    assert(idx >= 0 && idx < 64);
    this->_name = {static_cast<char>('a' + _coordinate.col), static_cast<char>('1' + _coordinate.row)};
}

bool Square::is_attacked_by(Color color) {
    return color == Color::WHITE ? !_attackedByWhites.empty() : !_attackedByBlacks.empty();
}

std::vector<Piece *> &Square::get_attacked_by(Color color) {
    return color == Color::WHITE ? _attackedByWhites : _attackedByBlacks;
}

std::ostream& operator << (std::ostream &os, const Square &square) {
    os << square.get_name();
    return os;
}