#pragma once

#include <string>
#include <vector>

#include "utils.h"

class Board;
class Piece;

class Square {
public:
    Square();

    void init(int idx, Board *board);
    //Square(int idx, Board *board);

    bool operator!=(Square &other) {return _coordinate != other._coordinate;}
    bool operator==(Square &other) {return !(_coordinate != other._coordinate);}

    bool is_free() const {return _piece == nullptr;}

    bool is_attacked_by(Color color);
    std::vector<Piece *> &get_attacked_by(Color color);

    Coordinate &get_coordinate() {return _coordinate;}

    std::string str() {return _name;}
    std::string get_name() const {return _name;}

    Board *get_board() {return _board;}
    Piece *get_piece() {return _piece;}

    int get_col() {return _coordinate.col;}
    int get_row() {return _coordinate.row;}

    friend class Piece;
    friend class Board;

private:
    int _idx;
    Coordinate _coordinate;
    Piece *_piece = nullptr;
    Board *_board;
    std::vector<Piece *> _attackedByWhites;
    std::vector<Piece *> _attackedByBlacks;
    std::string _name;
};

std::ostream& operator << (std::ostream &os, const Square &square);
