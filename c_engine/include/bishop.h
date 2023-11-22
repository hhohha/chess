#pragma once

#include "piece.h"

class Bishop : public SlidingPiece {
public:
    Bishop(Color color, Square *square);

    virtual std::vector<Direction> get_sliding_directions() const;

    std::vector<Direction> _slidingDirections = {Direction::DOWN_RIGHT, Direction::DOWN_LEFT, Direction::UP_RIGHT, Direction::UP_LEFT};

    bool _isLight = true;
};
