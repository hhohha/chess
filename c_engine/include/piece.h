#pragma once

#include <string>
#include <vector>

#include "constants.h"

class Square;
class Move;

class Piece {
public:
    Piece(PieceType kind, Color color, Square *square);

    Square *get_square();

    std::string str();

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

    virtual std::vector<Direction> get_sliding_directions() = 0;

    virtual void recalculate() override;
    virtual std::vector<Move *> calc_potential_moves_pinned(Direction directionFromKingToPinner) override;
    virtual std::vector<Move *> get_legal_moves() override;
};