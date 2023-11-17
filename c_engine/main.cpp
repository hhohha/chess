#include <iostream>

#include "board.h"
#include "move.h"
#include "square.h"
#include "utils.h"

#include "bishop.h"

//#include "pawn.h"


int main() {
    Board b;
    Bishop bishop(Color::WHITE, b.get_square(Coordinate{0, 2}));
}
