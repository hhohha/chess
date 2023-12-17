#include "constants.h"
#include "utest.h"
#include "move.h"

#define private public
#include "board.h"


TestSuite create_test_suite_board() {
    TestSuite testSuite("Board");

    testSuite.add_test("Board construction", []() {
        Board b;

        assert_equal(0U, b._whitePieces.size());
        assert_equal(0U, b._blackPieces.size());
        assert_equal(0U, b._whiteSlidingPieces.size());
        assert_equal(0U, b._blackSlidingPieces.size());
    });

    testSuite.add_test("Load fen", []() {
        Board b;
        b.load_fen(FEN_INIT);

        assert_equal(16U, b._whitePieces.size());
        assert_equal(16U, b._blackPieces.size());
        assert_equal(5U, b._whiteSlidingPieces.size());
        assert_equal(5U, b._blackSlidingPieces.size());
        assert_equal(PieceType::KING, b._whitePieces[0]->_kind);
        assert_equal(Color::WHITE, b._whitePieces[0]->_color);
        assert_equal(PieceType::KING, b._blackPieces[0]->_kind);
        assert_equal(Color::BLACK, b._blackPieces[0]->_color);

        assert_equal(PieceType::ROOK, b.get_square("a1")->get_piece()->_kind);
        assert_equal(Color::WHITE, b.get_square("a1")->get_piece()->_color);
        assert_equal(PieceType::BISHOP, b.get_square("c8")->get_piece()->_kind);
        assert_equal(Color::BLACK, b.get_square("c8")->get_piece()->_color);

        assert_equal(Color::WHITE, b._turn);
    });

    testSuite.add_test("Pin calculation 1", []() {
        Board b;
        b.load_fen(FEN_INIT);

        auto pinnedWhites = b.calc_pinned_pieces(Color::WHITE);
        assert_equal(0U, pinnedWhites.size());

        auto pinnedBlacks = b.calc_pinned_pieces(Color::BLACK);
        assert_equal(0U, pinnedBlacks.size());

    });

    testSuite.add_test("Pin calculation 2", []() {
        Board b;
        b.load_fen(FEN_TEST_C);

        auto pinnedWhites = b.calc_pinned_pieces(Color::WHITE);
        assert_equal(1U, pinnedWhites.size());
        assert_true(b.get_square("b5")->get_piece() == pinnedWhites.begin()->first, "Pinned piece should be on b5");
        assert_true(Direction::RIGHT == pinnedWhites.begin()->second, "Direction should be RIGHT");
        
        auto pinnedBlacks = b.calc_pinned_pieces(Color::BLACK);
        assert_equal(1U, pinnedBlacks.size());
        assert_true(b.get_square("f4")->get_piece() == pinnedBlacks.begin()->first, "Pinned piece should be on f4");
        assert_true(Direction::LEFT == pinnedBlacks.begin()->second, "Direction should be LEFT");
    });

    testSuite.add_test("Pin calculation 3", []() {
        Board b;
        // king surrounded by own pawns, all pinned by queens
        b.load_fen("k7/8/2q1q1q1/3PPP2/2qPKPq1/3PPP2/2q1q1q1/8 w - - 0 0");

        auto pinnedWhites = b.calc_pinned_pieces(Color::WHITE);
        assert_equal(8U, pinnedWhites.size());
        for (auto piece : b._whitePieces)
            if (piece->_kind != PieceType::KING)
                assert_true(pinnedWhites.find(piece) != pinnedWhites.end(), "All white pawns should be pinned");
    });

    testSuite.add_test("Pin calculation 4", []() {
        Board b;
        // previous position, but rooks instead of queens, only 4 pawns are pinned
        b.load_fen("k7/8/2r1r1r1/3PPP2/2rPKPr1/3PPP2/2r1r1r1/8 w - - 0 0");

        auto pinnedWhites = b.calc_pinned_pieces(Color::WHITE);
        assert_equal(4U, pinnedWhites.size());
        assert_true(pinnedWhites.find(b.get_square("d4")->get_piece()) != pinnedWhites.end(), "d4  pawn should be pinned");
        assert_true(pinnedWhites.find(b.get_square("f4")->get_piece()) != pinnedWhites.end(), "f4  pawn should be pinned");
        assert_true(pinnedWhites.find(b.get_square("e3")->get_piece()) != pinnedWhites.end(), "e3  pawn should be pinned");
        assert_true(pinnedWhites.find(b.get_square("e5")->get_piece()) != pinnedWhites.end(), "e5  pawn should be pinned");
    });

    testSuite.add_test("Get legal moves 1", []() {
        Board b;
        b.load_fen(FEN_INIT);
        auto moves = b.calc_all_legal_moves();

        assert_equal(20U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Get legal moves 2", []() {
        Board b;
        b.load_fen(FEN_TEST_A);
        auto moves = b.calc_all_legal_moves();

        assert_equal(3U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Get legal moves 3", []() {
        Board b;
        b.load_fen(FEN_TEST_B);
        auto moves = b.calc_all_legal_moves();

        assert_equal(44U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Get legal moves 4", []() {
        Board b;
        b.load_fen(FEN_TEST_C);
        auto moves = b.calc_all_legal_moves();

        assert_equal(14U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Get legal moves 5", []() {
        Board b;
        b.load_fen(FEN_TEST_D);
        auto moves = b.calc_all_legal_moves();

        assert_equal(6U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Get legal moves 6", []() {
        Board b;
        b.load_fen(FEN_TEST_D_INVERTED);
        auto moves = b.calc_all_legal_moves();

        assert_equal(6U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Get legal moves 7", []() {
        Board b;
        b.load_fen(FEN_TEST_E);
        auto moves = b.calc_all_legal_moves();

        assert_equal(48U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Get legal moves 8", []() {
        Board b;
        b.load_fen(FEN_TEST_E_NO_CASTLE);
        auto moves = b.calc_all_legal_moves();

        assert_equal(46U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Get legal moves 9", []() {
        Board b;
        b.load_fen(FEN_TEST_F);
        auto moves = b.calc_all_legal_moves();

        assert_equal(46U, moves.size());
        delete_vector(moves);
    });

    testSuite.add_test("Perform move 1", []() {
        Board b;
        b.load_fen(FEN_TEST_A);
        
        auto whiteKing = b.get_square("h1")->get_piece();
        auto destSquare = b.get_square("h2");
        auto move = new Move(whiteKing, destSquare);
        b.perform_move(move);

        assert_equal(destSquare, move->get_to_sqr());
        assert_equal(whiteKing->_square, move->get_to_sqr());
        assert_equal(move->get_from_sqr(), b.get_square("h1"));

        delete move;
    });


    testSuite.add_test("Perform move 2", []() {
        Board b;
        b.load_fen("k7/8/8/8/8/3p4/4P3/7K w - - 98 0");
        auto whiteKing = b.get_square("h1")->get_piece();
        auto whitePawn = b.get_square("e2")->get_piece();
        
        // step 1. initial position: white Kh1, pe2; black Ka8, pd3
        auto moves = b.calc_all_legal_moves();
        assert_equal(6U, moves.size());
        for (auto move : {"Kh1-h2", "Kh1-g2", "Kh1-g1", "pe2-e3", "pe2-e4", "pe2-d3"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;

        // step 2. white pawn to e3
        auto destSquare = b.get_square("e3");
        auto move = new Move(whitePawn, destSquare);
        b.perform_move(move);

        assert_equal(b.get_square("e3"), whitePawn->_square);
        assert_equal(b.get_square("e3")->get_piece(), whitePawn);
        assert_is_null(b.get_square("e2")->get_piece());

        moves = b.calc_all_legal_moves();

        assert_equal(4U, moves.size());
        for (auto move : {"Ka8-b8", "Ka8-a7", "Ka8-b7", "pd3-d2"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;

        // step 3. back to initial position
        b.undo_move();
        assert_equal(b.get_square("e2"), whitePawn->_square);
        assert_equal(b.get_square("e2")->get_piece(), whitePawn);
        assert_is_null(b.get_square("e3")->get_piece());

        moves = b.calc_all_legal_moves();
        assert_equal(6U, moves.size());
        for (auto move : {"Kh1-h2", "Kh1-g2", "Kh1-g1", "pe2-e3", "pe2-e4", "pe2-d3"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;

        // step 4. Kh1-h2
        move = new Move(whiteKing, b.get_square("h2"));
        b.perform_move(move);

        moves = b.calc_all_legal_moves();
        assert_equal(5U, moves.size());
        for (auto move : {"Ka8-b8", "Ka8-a7", "Ka8-b7", "pd3-d2", "pd3-e2"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;

        // step 5. - back to initial position
        b.undo_move();
        assert_equal(b.get_square("e2"), whitePawn->_square);
        assert_equal(b.get_square("e2")->get_piece(), whitePawn);
        assert_is_null(b.get_square("e3")->get_piece());

        moves = b.calc_all_legal_moves();
        assert_equal(6U, moves.size());
        for (auto move : {"Kh1-h2", "Kh1-g2", "Kh1-g1", "pe2-e3", "pe2-e4", "pe2-d3"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;
    });

    testSuite.add_test("Perform move 3", []() {
        Board b;
        b.load_fen(FEN_TEST_C);
        
        b.perform_move(new Move(b.get_square("a5")->_piece, b.get_square("a6")), false);
        b.perform_move(new Move(b.get_square("c7")->_piece, b.get_square("c5")), false);

        auto moves = b.calc_all_legal_moves();

        for (auto move : moves)
            std::cout << *move << std::endl;

    });

    testSuite.add_test("Perform move 4", []() {
        Board b;
        b.load_fen(FEN_TEST_B);


        auto move = new Move(b.get_square("a2")->get_piece(), b.get_square("a3"));
        b.perform_move(move);

        b.generate_successors(2);
    });


    return testSuite;
}   