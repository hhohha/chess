#include "constants.h"
#include "knight.h"
#include "utest.h"
#include "move.h"

#define private public

#include "board.h"

TestSuite create_test_suite_knight() {
    TestSuite testSuite("Knight");

    testSuite.add_test("Knight construction", []() {
        Board b;
        auto knight = dynamic_cast<Knight*>(b.place_piece(PieceType::KNIGHT, Color::WHITE, "a1"));

        assert_equal(PieceType::KNIGHT, knight->_kind);
        assert_equal(Color::WHITE, knight->_color);
        assert_equal("a1", knight->_square->get_name());
        assert_equal("N", knight->_name);
        assert_true(knight->_isLight);
    });
    
    testSuite.add_test("Knight move generation 1", []() {
        Board b;
        auto knight = dynamic_cast<Knight*>(b.place_piece(PieceType::KNIGHT, Color::WHITE, "a1"));
        knight->recalculate();

        auto moves = b.squares_to_moves(knight->get_potential_squares(), knight);

        assert_equal(2U, moves.size());
        for (auto move : {"Na1-b3", "Na1-c2"})
            assert_vector_contains(moves, move);
    });

    testSuite.add_test("Knight move generation 2", []() {
        Board b;
        auto knight = dynamic_cast<Knight*>(b.place_piece(PieceType::KNIGHT, Color::WHITE, "d4"));
        knight->recalculate();

        auto moves = b.squares_to_moves(knight->get_potential_squares(), knight);

        assert_equal(8U, moves.size());
        for (auto move : {"Nd4-b3", "Nd4-b5", "Nd4-c2", "Nd4-c6", "Nd4-e2", "Nd4-e6", "Nd4-f3", "Nd4-f5"})
            assert_vector_contains(moves, move);
    });

    return testSuite;
}