#include "square.h"

Square::Square(unsigned int idx, Board *board)
: _idx(idx),
    _colIdx(idx % 8),
    _rowIdx(idx / 8),
    _board(board) {

    this->_name = {static_cast<char>('a' + _colIdx), static_cast<char>('1' + _rowIdx)};
}

bool Square::operator!=(Square &other) {
    return _colIdx != other._colIdx || _rowIdx != other._rowIdx;
}

bool Square::is_free() {
    return _piece == nullptr;
}

bool Square::is_attacked_by(Color color) {
    return color == Color::WHITE ? !_attackedByWhites.empty() : !_attackedByBlacks.empty();
}

std::vector<Piece *> Square::get_attacked_by(Color color) {
    return color == Color::WHITE ? _attackedByWhites : _attackedByBlacks;
}

std::string Square::str() {
    return _name;
}