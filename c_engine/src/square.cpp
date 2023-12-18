#include "square.h"

Square::Square(){};

void Square::init(int idx, Board *board) {
    _idx = idx;
    _coordinate = {idx % 8, idx / 8};
    _board = board;
    ASSERT(idx >= 0 && idx < 64, "invalid square index");
    this->_name = {static_cast<char>('a' + _coordinate.col), static_cast<char>('1' + _coordinate.row)};

    _attackedByBlacks.reserve(16);
    _attackedByWhites.reserve(16);
}

bool Square::is_attacked_by(Color color) {
    return color == Color::WHITE ? !_attackedByWhites.empty() : !_attackedByBlacks.empty();
}

std::vector<Piece *> &Square::get_attacked_by(Color color) {
    return color == Color::WHITE ? _attackedByWhites : _attackedByBlacks;
}


// printing of square via ostream
std::ostream& operator << (std::ostream &os, const Square &square) {
    os << square.get_name();
    return os;
}