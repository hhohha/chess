#include "constants.h"
#include "piece.h"

class Rook : public SlidingPiece {
public:
    Rook(PieceType kind, Color color, Square *square);

    virtual std::vector<Direction> get_sliding_directions();

    std::vector<Direction> _slidingDirections = {Direction::DOWN, Direction::UP, Direction::RIGHT, Direction::LEFT};
};
