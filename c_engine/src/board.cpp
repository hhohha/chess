#include "board.h"
#include "square.h"
#include "move.h"
#include "utils.h"

PieceIterator::PieceIterator(Board *board, Color color, bool end)
    : _board(board)
    , _color(color) {

        if (!end) {
            if (color == Color::WHITE) {
                _ptr = _board->_whitePawns[0];
            } else {
                _ptr = _board->_blackPawns[0];
            }
        } else {
            if (color == Color::WHITE) {
                _ptr = _board->_whitePawns.back();
            } else {
                _ptr = _board->_blackPawns.back();
            }
        }
    }


Piece &PieceIterator::operator*() const {
    return *_ptr;
}

Piece *PieceIterator::operator->() {
    return _ptr;
}

PieceIterator &PieceIterator::operator++() {
    if (_color == Color::WHITE) {
                
    } else {

    }
    return *this;
}




// PieceIterator &operator++();
// PieceIterator operator++(int);

// bool operator==(const PieceIterator &other);
// bool operator!=(const PieceIterator &other);

Board::Board() {
    for(unsigned i = 0; i < 64; ++i) {
        _squares.push_back(Square(i, this));
    }
}

void Board::clear() {
    for (auto &sqr : _squares) {
        sqr._piece = nullptr;
    }

    _whitePawns.clear();
    _blackPawns.clear();
    _whiteKnights.clear();
    _blackKnights.clear();
    _whiteBishops.clear();
    _blackBishops.clear();
    _whiteRooks.clear();
    _blackRooks.clear();
    _whiteQueens.clear();
    _blackQueens.clear();
    _whiteKings.clear();
    _blackKings.clear();
}

Square *Board::get_square(Coordinate c) {
    if (0 <= c.col && c.col < 8 && 0 <= c.row && c.row < 8)
        return &_squares[c.col*8 + c.row];
    return nullptr;
}

Square *Board::get_square(unsigned int col, unsigned int row) {
    if (0 <= col && col < 8 && 0 <= row && row < 8)
        return &_squares[col*8 + row];
    return nullptr;
}

Square *Board::get_square(unsigned int idx) {
    if (0 <= idx && idx < 64)
        return &_squares[idx];
    return nullptr;
}

Square *Board::get_square(std::string name) {
    if (name.size() == 2 && 'a' <= name[0] && name[0] <= 'h' && '1' <= name[1] && name[1] <= '8')
        return &_squares[square_name_to_idx(name)];
    return nullptr;
}