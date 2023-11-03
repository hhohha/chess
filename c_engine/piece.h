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
    virtual std::vector<Move *> calc_potential_moves() = 0;
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
};

class SlidingPiece : public Piece {
public:
    SlidingPiece(PieceType kind, Color color, Square *square);

    virtual void recalculate();

    virtual std::vector<Direction> get_sliding_directions() = 0;
};

class Pawn : Piece {
public:
    Pawn(PieceType kind, Color color, Square *square);

    const int _moveOffset;
    const unsigned int _baseRow;
    const unsigned int _promotionRow;
    const unsigned int _enPassantRow;
};

class Knight : Piece {
public:
    Knight(PieceType kind, Color color, Square *square);
};

class Bishop : public SlidingPiece {
public:
    Bishop(PieceType kind, Color color, Square *square);

    virtual std::vector<Direction> get_sliding_directions();

    std::vector<Direction> _slidingDirections = {Direction::DOWN_RIGHT, Direction::DOWN_LEFT, Direction::UP_RIGHT, Direction::UP_LEFT};
};

class Rook : public SlidingPiece {
public:
    Rook(PieceType kind, Color color, Square *square);

    virtual std::vector<Direction> get_sliding_directions();

    std::vector<Direction> _slidingDirections = {Direction::DOWN, Direction::UP, Direction::RIGHT, Direction::LEFT};
};

class Queen : public SlidingPiece {
public:
    Queen(PieceType kind, Color color, Square *square);

    virtual std::vector<Direction> get_sliding_directions();

    std::vector<Direction> _slidingDirections = {Direction::DOWN, Direction::UP, Direction::RIGHT, Direction::LEFT,
        Direction::DOWN_RIGHT, Direction::DOWN_LEFT, Direction::UP_RIGHT, Direction::UP_LEFT};
};

class King : Piece {
public:
    King(PieceType kind, Color color, Square *square);
};