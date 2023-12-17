#include "utest.h"
#include "king.h"
#include "move.h"

#define private public

#include "board.h"

TestSuite create_test_suite_king() {
    TestSuite testSuite("King");

    testSuite.add_test("King construction", []() {
        Board b;
        auto king = dynamic_cast<King*>(b.place_piece(PieceType::KING, Color::WHITE, "a1"));


        assert_equal(PieceType::KING, king->_kind);
        assert_equal(Color::WHITE, king->_color);
        assert_equal("a1", king->_square->get_name());
        assert_equal("K", king->_name);
        assert_false(king->_isLight, "king is not a light piece");
    });

    testSuite.add_test("King move generation 1", []() {
        Board b;
        auto king = dynamic_cast<King*>(b.place_piece(PieceType::KING, Color::WHITE, "a1"));
        king->recalculate();

        auto moves = b.squares_to_moves(king->get_potential_squares(), king);

        assert_equal(3U, moves.size());
        for (auto move : {"Ka1-a2", "Ka1-b1", "Ka1-b2"})
            assert_vector_contains(moves, move);
    });

    testSuite.add_test("King move generation 2", []() {
        Board b;
        auto king = dynamic_cast<King*>(b.place_piece(PieceType::KING, Color::WHITE, "d4"));
        king->recalculate();

        auto moves = b.squares_to_moves(king->get_potential_squares(), king);

        assert_equal(8U, moves.size());
        for (auto move : {"Kd4-c3", "Kd4-c4", "Kd4-c5", "Kd4-d3", "Kd4-d5", "Kd4-e3", "Kd4-e4", "Kd4-e5"})
            assert_vector_contains(moves, move);
    });

    return testSuite;
}   