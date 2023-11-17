#include <cassert>

#include "utils.h"
#include "square.h"

std::string piece_type_to_letter(PieceType type, bool printPawn) {
    if (type == PieceType::PAWN) return printPawn ? "p" : "";
    else if (type == PieceType::PAWN) return "N";
    else if (type == PieceType::BISHOP) return "B";
    else if (type == PieceType::ROOK) return "R";
    else if (type == PieceType::QUEEN) return "Q";
    else if (type == PieceType::KING) return "K";
    else assert(false);
}

int square_name_to_idx(std::string name) {
    if (name.size() != 2 || !('a' <= name[0] && name[0] <= 'h') || !('1' <= name[1] && name[1] <= '8'))
        return -1;
    else {
        return int(name[0]) - 97 + (int(name[1] - 49) * 8);
    }
}

Direction reverse_direction(Direction d) {
    if (d == Direction::UP) return Direction::DOWN;
    else if (d == Direction::DOWN) return Direction::UP;
    else if (d == Direction::LEFT) return Direction::RIGHT;
    else if (d == Direction::RIGHT) return Direction::LEFT;
    else if (d == Direction::UP_LEFT) return Direction::DOWN_RIGHT;
    else if (d == Direction::UP_RIGHT) return Direction::DOWN_LEFT;
    else if (d == Direction::DOWN_LEFT) return Direction::UP_RIGHT;
    else if (d == Direction::DOWN_RIGHT) return Direction::UP_LEFT;
    else assert(false);
}

void move_in_direction(Coordinate &c, Direction d) {
    if (d == Direction::DOWN) c.row -= 1;
    else if (d == Direction::UP) c.row += 1;
    else if (d == Direction::LEFT) c.col -= 1;
    else if (d == Direction::RIGHT) c.col += 1;
    else if (d == Direction::DOWN_RIGHT) {c.row -= 1; c.col += 1;}
    else if (d == Direction::DOWN_LEFT) {c.row -= 1; c.col -= 1;}
    else if (d == Direction::UP_RIGHT) {c.row += 1; c.col += 1;}
    else if (d == Direction::UP_LEFT) {c.row += 1; c.col -= 1;}
    else assert(false);
}

bool is_same_col_or_row(Square &sqr1, Square &sqr2) {
    return sqr1.get_col() == sqr2.get_col() || sqr1.get_row() == sqr2.get_row();
}

bool is_same_diag(Square &sqr1, Square &sqr2) {
    return abs(sqr1.get_col() - sqr2.get_col()) == abs(sqr1.get_row() - sqr2.get_row());
}

Direction get_direction(Square &sqr1, Square &sqr2) {
    assert(sqr1 != sqr2);
    if (sqr1.get_col() == sqr2.get_col())
        return sqr1.get_row() < sqr2.get_row() ? Direction::UP : Direction::DOWN;
    if (sqr1.get_row() == sqr2.get_row())
        return sqr1.get_col() < sqr2.get_col() ? Direction::RIGHT : Direction::LEFT;
    if (sqr1.get_col() - sqr2.get_col() == sqr1.get_row() - sqr2.get_row())
        return sqr1.get_col() > sqr2.get_col() ? Direction::DOWN_LEFT : Direction::UP_RIGHT;
    if (sqr1.get_col() - sqr2.get_col() == sqr2.get_row() - sqr1.get_row())
        return sqr1.get_col() > sqr2.get_col() ? Direction::UP_LEFT : Direction::DOWN_RIGHT;
    assert(false);
}