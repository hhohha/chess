#include "constants.h"
#include "piece.h"


class Square;

class Pawn : public Piece {
public:
    Pawn(PieceType kind, Color color, Square *square);

    const int _moveOffset;
    const unsigned int _baseRow;
    const unsigned int _promotionRow;
    const unsigned int _enPassantRow;
};
