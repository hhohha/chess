#include "utest.h"
#include "board.h"
#include "bishop.h"
#include "move.h"

TestSuite create_test_suite_bishop() {
    TestSuite testSuite("Bishop");

    testSuite.addTest("Bishop construction", []() {
        Board b;
        Square *sqr = b.get_square("a1");
        Bishop bishop(Color::WHITE, sqr);

        assertEqual(PieceType::BISHOP, bishop._kind);
        assertEqual(Color::WHITE, bishop._color);
        assertEqual(sqr, bishop._square);
        assertEqual("B", bishop._name);
        assertEqual(true, bishop._isLight);

        assertEqual(4U, bishop._slidingDirections.size());
        assertEqual(Direction::DOWN_RIGHT, bishop._slidingDirections[0]);
        assertEqual(Direction::DOWN_LEFT, bishop._slidingDirections[1]);
        assertEqual(Direction::UP_RIGHT, bishop._slidingDirections[2]);
        assertEqual(Direction::UP_LEFT, bishop._slidingDirections[3]);
    });

    return testSuite;
}   