#pragma once

#include <string>
#include <vector>

#include "constants.h"

class Board;
class Piece;

class Square {
public:
    Square(unsigned int idx, Board *board);

    bool operator!=(Square &other);

    bool is_free();

    bool is_attacked_by(Color color);

    std::vector<Piece *> &get_attacked_by(Color color);

    std::string str();

    int _idx;
    int _colIdx;
    int _rowIdx;
    Piece *_piece = nullptr;
    Board *_board;
    std::vector<Piece *> _attackedByWhites;
    std::vector<Piece *> _attackedByBlacks;
    std::string _name;
};