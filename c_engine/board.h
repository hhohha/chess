#pragma once

#include <optional>
#include <string>
#include <vector>

class Coordinate;

class Move;
class Square;
class Pawn;
class Knight;
class Bishop;
class Rook;
class Queen;
class King;

class Board {
public:
    Board();

    Square *get_square(Coordinate c);
    Square *get_square(unsigned int col, unsigned int row);
    Square *get_square(unsigned int idx);
    Square *get_square(std::string name);

    std::vector<Move> _history;
    std::vector<Square> _squares;

    std::vector<Pawn *> _whitePawns;
    std::vector<Pawn *> _blackPawns;
    std::vector<Knight *> _whiteKnights;
    std::vector<Knight *> _blackKnights;
    std::vector<Bishop *> _whiteBishops;
    std::vector<Bishop *> _blackBishops;
    std::vector<Rook *> _whiteRooks;
    std::vector<Rook *> _blackRooks;
    std::vector<Queen *> _whiteQueens;
    std::vector<Queen *> _blackQueens;
    std::optional<King *> _whiteKing;
    std::optional<King *> _blackKing;
};
