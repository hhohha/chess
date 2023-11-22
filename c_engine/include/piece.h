#pragma once

#include <string>
#include <vector>

#include "square.h"

class Square;
class Move;

class Piece {
public:
    Piece(PieceType kind, Color color, Square *square);

    Square *get_square();

    std::string str() const {return _name + _square->str();}

    virtual void recalculate() = 0;
    virtual std::vector<Move *> calc_potential_moves_pinned(Direction directionFromKingToPinner) = 0;
    virtual std::vector<Move *> get_legal_moves() = 0;

    PieceType _kind;
    Color _color;
    Square *_square;
    bool _isSliding;
    bool _isLight;
    bool _isActive = true;
    unsigned _movesCnt = 0;
    std::string _name;
    std::vector<Square *> _attackedSquares;
    std::vector<Move *> _potentialMoves;

    friend class Square;
    friend class Board;
};

class SlidingPiece : public Piece {
public:
    SlidingPiece(PieceType kind, Color color, Square *square);

    virtual std::vector<Direction> get_sliding_directions() const = 0;

    virtual void recalculate() override;
    virtual std::vector<Move *> calc_potential_moves_pinned(Direction directionFromKingToPinner) override;
    virtual std::vector<Move *> get_legal_moves() override;
};

std::ostream& operator << (std::ostream &os, const Piece &piece);