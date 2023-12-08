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

    // testSuite.addTest("Board load fen", []() {
    //     Board b;
    //     b.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");

    //     assertEqual(16U, b._whitePieces.size());
    //     assertEqual(16U, b._blackPieces.size());
    //     assertEqual(5U, b._whiteSlidingPieces.size());
    //     assertEqual(5U, b._blackSlidingPieces.size());
    //     assertEqual(PieceType::KING, b._whitePieces[0]->_kind);
    //     assertEqual(Color::WHITE, b._whitePieces[0]->_color);
    //     assertEqual(PieceType::KING, b._blackPieces[0]->_kind);
    //     assertEqual(Color::BLACK, b._blackPieces[0]->_color);

    //     assertEqual(PieceType::ROOK, b.get_square("a1")->get_piece()->_kind);
    //     assertEqual(Color::WHITE, b.get_square("a1")->get_piece()->_color);
    //     assertEqual(PieceType::BISHOP, b.get_square("c8")->get_piece()->_kind);
    //     assertEqual(Color::BLACK, b.get_square("c8")->get_piece()->_color);

    //     assertEqual(Color::WHITE, b._turn);
    // });

    return testSuite;
}   