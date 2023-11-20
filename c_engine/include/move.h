#pragma once

#include <optional>
#include <string>

#include "constants.h"

class Piece;
class Square;

class Move {
public:
    Move(Piece *piece, Square *toSqr, std::optional<PieceType> newPiece = std::nullopt);

    bool operator==(Move &other);

    bool is_promotion();
    bool is_castling();
    bool is_en_passant() {return _isEnPassant;}
    std::string str();

    Piece *get_piece() {return _piece;}
    Square *get_from_sqr() {return _fromSqr;}
    Square *get_to_sqr() {return _toSqr;}
    Piece *get_piece_taken() {return _pieceTaken;}
    std::optional<PieceType> get_new_piece() {return _newPiece;}

private:
    Piece *_piece;
    Square *_fromSqr;
    Square *_toSqr;
    Piece *_pieceTaken = nullptr;
    std::optional<PieceType> _newPiece;
    bool _isEnPassant = false;
};
