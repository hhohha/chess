#pragma once

#include <optional>
#include <string>

#include "constants.h"

class Piece;
class Square;

class Move {
public:
    Move(Piece *piece, Square *toSqr, std::optional<PieceType> newPiece = std::nullopt);

    bool operator==(const Move &other) const;

    bool is_promotion() const;
    bool is_castling() const;
    bool is_en_passant() const {return _isEnPassant;}
    std::string str() const;

    Piece *get_piece() const {return _piece;}
    Square *get_from_sqr() const {return _fromSqr;}
    Square *get_to_sqr() const {return _toSqr;}
    Piece *get_piece_taken() const {return _pieceTaken;}
    std::optional<PieceType> get_new_piece() const {return _newPiece;}

    void mark_as_en_passant() {_isEnPassant = true;}

private:
    Piece *_piece;
    Square *_fromSqr;
    Square *_toSqr;
    Piece *_pieceTaken = nullptr;
    std::optional<PieceType> _newPiece;
    bool _isEnPassant = false;
};

std::ostream& operator << (std::ostream &os, const Move &move);