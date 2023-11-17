#pragma once

#include <optional>
#include <string>

#include "constants.h"

class Piece;
class Square;

class Move {
public:
    Move(Piece *piece, Square *toSqr);

    bool operator==(Move &other);

    bool is_promotion();
    bool is_castling();
    std::string str();

private:
    Piece *_piece;
    Square *_fromSqr;
    Square *_toSqr;
    Piece *_pieceTaken = nullptr;
    std::optional<PieceType> _newPiece;
    bool _isEnPassant = false;
};
