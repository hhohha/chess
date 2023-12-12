#include "constants.h"
#include "utest.h"
#include "move.h"

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

    testSuite.addTest("Load fen", []() {
        Board b;
        b.load_fen(FEN_INIT);

        assertEqual(16U, b._whitePieces.size());
        assertEqual(16U, b._blackPieces.size());
        assertEqual(5U, b._whiteSlidingPieces.size());
        assertEqual(5U, b._blackSlidingPieces.size());
        assertEqual(PieceType::KING, b._whitePieces[0]->_kind);
        assertEqual(Color::WHITE, b._whitePieces[0]->_color);
        assertEqual(PieceType::KING, b._blackPieces[0]->_kind);
        assertEqual(Color::BLACK, b._blackPieces[0]->_color);

        assertEqual(PieceType::ROOK, b.get_square("a1")->get_piece()->_kind);
        assertEqual(Color::WHITE, b.get_square("a1")->get_piece()->_color);
        assertEqual(PieceType::BISHOP, b.get_square("c8")->get_piece()->_kind);
        assertEqual(Color::BLACK, b.get_square("c8")->get_piece()->_color);

        assertEqual(Color::WHITE, b._turn);
    });

    testSuite.addTest("Pin calculation 1", []() {
        Board b;
        b.load_fen(FEN_INIT);

        auto pinnedWhites = b.calc_pinned_pieces(Color::WHITE);
        assertEqual(0U, pinnedWhites.size());

        auto pinnedBlacks = b.calc_pinned_pieces(Color::BLACK);
        assertEqual(0U, pinnedBlacks.size());

    });

    testSuite.addTest("Pin calculation 2", []() {
        Board b;
        b.load_fen(FEN_TEST_C);

        auto pinnedWhites = b.calc_pinned_pieces(Color::WHITE);
        assertEqual(1U, pinnedWhites.size());
        assertTrue(b.get_square("b5")->get_piece() == pinnedWhites.begin()->first, "Pinned piece should be on b5");
        assertTrue(Direction::RIGHT == pinnedWhites.begin()->second, "Direction should be RIGHT");
        
        auto pinnedBlacks = b.calc_pinned_pieces(Color::BLACK);
        assertEqual(1U, pinnedBlacks.size());
        assertTrue(b.get_square("f4")->get_piece() == pinnedBlacks.begin()->first, "Pinned piece should be on f4");
        assertTrue(Direction::LEFT == pinnedBlacks.begin()->second, "Direction should be LEFT");
    });

    testSuite.addTest("Pin calculation 3", []() {
        Board b;
        // king surrounded by own pawns, all pinned by queens
        b.load_fen("k7/8/2q1q1q1/3PPP2/2qPKPq1/3PPP2/2q1q1q1/8 w - - 0 0");

        auto pinnedWhites = b.calc_pinned_pieces(Color::WHITE);
        assertEqual(8U, pinnedWhites.size());
        for (auto piece : b._whitePieces)
            if (piece->_kind != PieceType::KING)
                assertTrue(pinnedWhites.find(piece) != pinnedWhites.end(), "All white pawns should be pinned");
    });

    testSuite.addTest("Pin calculation 4", []() {
        Board b;
        // previous position, but rooks instead of queens, only 4 pawns are pinned
        b.load_fen("k7/8/2r1r1r1/3PPP2/2rPKPr1/3PPP2/2r1r1r1/8 w - - 0 0");

        auto pinnedWhites = b.calc_pinned_pieces(Color::WHITE);
        assertEqual(4U, pinnedWhites.size());
        assertTrue(pinnedWhites.find(b.get_square("d4")->get_piece()) != pinnedWhites.end(), "d4  pawn should be pinned");
        assertTrue(pinnedWhites.find(b.get_square("f4")->get_piece()) != pinnedWhites.end(), "f4  pawn should be pinned");
        assertTrue(pinnedWhites.find(b.get_square("e3")->get_piece()) != pinnedWhites.end(), "e3  pawn should be pinned");
        assertTrue(pinnedWhites.find(b.get_square("e5")->get_piece()) != pinnedWhites.end(), "e5  pawn should be pinned");
    });

    testSuite.addTest("Get legal moves 1", []() {
        Board b;
        b.load_fen(FEN_INIT);
        auto moves = b.calc_all_legal_moves();

        assertEqual(20U, moves.size());
    });

    testSuite.addTest("Get legal moves 2", []() {
        Board b;
        b.load_fen(FEN_TEST_A);
        auto moves = b.calc_all_legal_moves();

        assertEqual(3U, moves.size());
    });

    testSuite.addTest("Get legal moves 3", []() {
        Board b;
        b.load_fen(FEN_TEST_B);
        auto moves = b.calc_all_legal_moves();

        assertEqual(44U, moves.size());
    });

    testSuite.addTest("Get legal moves 4", []() {
        Board b;
        b.load_fen(FEN_TEST_C);
        auto moves = b.calc_all_legal_moves();

        assertEqual(14U, moves.size());
    });

    testSuite.addTest("Get legal moves 5", []() {
        Board b;
        b.load_fen(FEN_TEST_D);
        auto moves = b.calc_all_legal_moves();

        assertEqual(6U, moves.size());
    });

    testSuite.addTest("Get legal moves 6", []() {
        Board b;
        b.load_fen(FEN_TEST_D_INVERTED);
        auto moves = b.calc_all_legal_moves();

        assertEqual(6U, moves.size());
    });

    testSuite.addTest("Get legal moves 7", []() {
        Board b;
        b.load_fen(FEN_TEST_E);
        auto moves = b.calc_all_legal_moves();

        assertEqual(48U, moves.size());
    });

    testSuite.addTest("Get legal moves 8", []() {
        Board b;
        b.load_fen(FEN_TEST_E_NO_CASTLE);
        auto moves = b.calc_all_legal_moves();

        assertEqual(46U, moves.size());
    });

    testSuite.addTest("Get legal moves 9", []() {
        Board b;
        b.load_fen(FEN_TEST_F);
        auto moves = b.calc_all_legal_moves();

        assertEqual(46U, moves.size());
    });

    return testSuite;
}   