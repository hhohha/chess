#pragma once

#include <string>
#include <vector>

#include "square.h"

class Square;
class Move;

class Piece {
protected:
    Piece(PieceType kind, Color color, Square *square);

public:
    
    Square *get_square();
    virtual ~Piece() = default;

    std::string str() const {return _name + _square->str();}

    virtual std::vector<Square *> get_potential_squares() {return _potentialSquares;}

    virtual void recalculate() = 0;
    virtual std::vector<Square *> calc_potential_squares_pinned(Direction directionFromKingToPinner) = 0;

    PieceType _kind;
    Color _color;
    Square *_square;
    bool _isSliding;
    bool _isLight;
    bool _isActive = true;
    unsigned int _value;
    unsigned _movesCnt = 0;
    std::string _name;
    std::vector<Square *> _attackedSquares;
    std::vector<Square *> _potentialSquares;
};

class SlidingPiece : public Piece {
protected:
    SlidingPiece(PieceType kind, Color color, Square *square, const std::vector<Direction> slidingDirections);

public:
    const std::vector<Direction> & get_sliding_directions() const {return _slidingDirections;}

    virtual void recalculate() override;
    virtual std::vector<Square *> calc_potential_squares_pinned(Direction directionFromKingToPinner) override;

    const std::vector<Direction> _slidingDirections;
};

std::ostream& operator << (std::ostream &os, const Piece &piece);