#include "utest.h"

#define private public

#include "board.h"


TestSuite create_test_suite_board() {
    TestSuite testSuite("Board");

    testSuite.addTest("Board construction", []() {
        Board b;

        assertEqual(0U, b._whitePieces.size());
        assertEqual(0U, b._blackPieces.size());
        assertEqual(0U, b._whiteSlidingPieces.size());
        assertEqual(0U, b._blackSlidingPieces.size());
    });

    testSuite.addTest("Board load fen", []() {
        Board b;
        b.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");

        assertEqual(16U, b._whitePieces.size());
        assertEqual(16U, b._blackPieces.size());
        assertEqual(5U, b._whiteSlidingPieces.size());
        assertEqual(5U, b._blackSlidingPieces.size());

        assertIsNull(b._squares[0].get_piece());
    });

    return testSuite;
}   