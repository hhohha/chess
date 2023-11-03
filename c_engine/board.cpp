#include "board.h"
#include "square.h"
#include "move.h"
#include "utils.h"

Board::Board() {
    for(unsigned i = 0; i < 64; ++i) {
        _squares.push_back(Square(i, this));
    }
}

Square *Board::get_square(Coordinate c) {
    if (0 <= c.col < 8 && 0 <= c.row < 8)
        return &_squares[c.col*8 + c.row];
    return nullptr;
}

Square *Board::get_square(unsigned int col, unsigned int row) {
    if (0 <= col < 8 && 0 <= row < 8)
        return &_squares[col*8 + row];
    return nullptr;
}

Square *Board::get_square(unsigned int idx) {
    if (0 <= idx < 64)
        return &_squares[idx];
    return nullptr;
}

Square *Board::get_square(std::string name) {
    if (name.size() == 2 && 'a' <= name[0] && name[0] <= 'h' && '1' <= name[1] && name[1] <= '8')
        return &_squares[square_name_to_idx(name)];
    return nullptr;
}