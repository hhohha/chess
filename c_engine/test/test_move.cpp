#include "utest.h"
#include "move.h"
#include "bishop.h"
#include "square.h"

TestSuite create_test_suite_moves() {
    TestSuite testSuite("Moves");

    testSuite.addTest("Move construction", []() {
        Bishop bishop(Color::WHITE, nullptr);
        Square sqr(0, nullptr);

        Move move(&bishop, &sqr);
        assertTrue(!move.is_promotion());
    });

    return testSuite;
}