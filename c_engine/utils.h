#pragma once

#include <string>

#include "constants.h"

class Square;

struct Coordinate {
    unsigned int col;
    unsigned int row;
};

std::string piece_type_to_letter(PieceType type, bool printPawn=false);
int square_name_to_idx(std::string name);
Direction reverse_direction(Direction d);
void move_in_direction(Coordinate &c, Direction d);
bool is_same_col_or_row(Square &sqr1, Square &sqr2);
bool is_same_diag(Square &sqr1, Square &sqr2);
Direction get_direction(Square &sqr1, Square &sqr2);