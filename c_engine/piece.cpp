#include "piece.h"
#include "board.h"
#include "utils.h"

Piece::Piece(PieceType kind, Color color, Square *square)
    : _kind(kind),
      _color(color),
      _square(square) {}

Square *Piece::get_square() {
    return _square;
}

std::string Piece::str() {
    return _name;
}

SlidingPiece::SlidingPiece(PieceType kind, Color color, Square *square)
    : Piece(kind, color, square) {

    _isSliding = true;
}

void SlidingPiece::recalculate() {
    //for sqr in self.attackedSquares:
    //    sqr.get_attacked_by(self.color).remove(self)

    //self.potentialMoves.clear()
    //self.attackedSquares.clear();

    for (auto direction : get_sliding_directions()) {
        Coordinate c{0, 0};
        
        while (true) {
            move_in_direction(c, direction);
            //auto sqr = _square->_board->get_square(c);

            // square: Optional[Square] = self.square.board.get_square_by_coords_opt(self.square.colIdx + i, self.square.rowIdx + j)
            //   if square is None:
            //     break  # reached the edge of the board
            // if square.piece is None:
            //     self.attackedSquares.add(square)
            //     self.potentialMoves.append(Move(self, square))
            // elif square.piece.color != self.color:
            //     self.attackedSquares.add(square)
            //     self.potentialMoves.append(Move(self, square))
            //     break
            // else:
            //     self.attackedSquares.add(square)
            //     break
        }
    }

    
    // for sqr in self.attackedSquares:
        // sqr.get_attacked_by(self.color).add(self)

}

 Pawn::Pawn(PieceType kind, Color color, Square *square)
    : Piece(kind, color, square),
    _moveOffset(color == Color::WHITE ? 1 : -1),
    _baseRow(color == Color::WHITE ? 1 : 6),
    _promotionRow(color == Color::WHITE ? 7 : 0),
    _enPassantRow(color == Color::WHITE ? 4 : 3) {

    _name = "p";
    _isSliding = false;
    _isLight = false;
}

Knight::Knight(PieceType kind, Color color, Square *square)
    : Piece(kind, color, square) {

    _isSliding = false;
    _isLight = true;
    _name = "N";
}

Bishop::Bishop(PieceType kind, Color color, Square *square)
    : SlidingPiece(kind, color, square) {

    _isLight = true;
    _name = "B";
}

std::vector<Direction> Bishop::get_sliding_directions() {
    return _slidingDirections;
}

Rook::Rook(PieceType kind, Color color, Square *square)
    : SlidingPiece(kind, color, square) {

    _isLight = false;
    _name = "R";
}

std::vector<Direction> Rook::get_sliding_directions() {
    return _slidingDirections;
}

Queen::Queen(PieceType kind, Color color, Square *square)
    : SlidingPiece(kind, color, square) {

    _isLight = false;
    _name = "Q";
}

std::vector<Direction> Queen::get_sliding_directions() {
    return _slidingDirections;
}

King::King(PieceType kind, Color color, Square *square)
    : Piece(kind, color, square) {

    _isSliding = false;
    _isLight = true;
    _name = "K";
}