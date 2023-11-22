#pragma once

#include "piece.h"

class Queen : public SlidingPiece {
public:
    Queen(PieceType kind, Color color, Square *square);

    virtual std::vector<Direction> get_sliding_directions();

    std::vector<Direction> _slidingDirections = {Direction::DOWN, Direction::UP, Direction::RIGHT, Direction::LEFT,
        Direction::DOWN_RIGHT, Direction::DOWN_LEFT, Direction::UP_RIGHT, Direction::UP_LEFT};
};