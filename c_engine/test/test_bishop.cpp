#include "constants.h"
#include "king.h"
#include "rook.h"
#include "utest.h"
#include "bishop.h"
#include "move.h"

#define private public

#include "board.h"

TestSuite create_test_suite_bishop() {
    TestSuite testSuite("Bishop");

    testSuite.add_test("Bishop construction", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "a1"));

        assert_equal(PieceType::BISHOP, bishop->_kind);
        assert_equal(Color::WHITE, bishop->_color);
        assert_equal("a1", bishop->_square->get_name());
        assert_equal("B", bishop->_name);
        assert_true(bishop->_isLight);

        assert_equal(4U, bishop->_slidingDirections.size());
        assert_vector_contains(bishop->_slidingDirections, Direction::DOWN_RIGHT);
        assert_vector_contains(bishop->_slidingDirections, Direction::DOWN_LEFT);
        assert_vector_contains(bishop->_slidingDirections, Direction::UP_RIGHT);
        assert_vector_contains(bishop->_slidingDirections, Direction::UP_LEFT);
    });

    testSuite.add_test("Move generation 1", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "a1"));
        bishop->recalculate();

        auto moves = b.squares_to_moves(bishop->get_potential_squares(), bishop);

        assert_equal(7U, moves.size());
        for (auto move : {"Ba1-b2", "Ba1-c3", "Ba1-d4", "Ba1-e5", "Ba1-f6", "Ba1-g7", "Ba1-h8"})
            assert_vector_contains(moves, move);

    });

    testSuite.add_test("Bishop move generation 2", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "d4"));
        bishop->recalculate();

        auto moves = b.squares_to_moves(bishop->get_potential_squares(), bishop);

        assert_equal(13U, moves.size());
        for (auto move : {"Bd4-a1", "Bd4-b2", "Bd4-c3", "Bd4-e5", "Bd4-f6", "Bd4-g7", "Bd4-h8", "Bd4-c5", "Bd4-b6",
            "Bd4-a7", "Bd4-e3", "Bd4-f2", "Bd4-g1"})
            assert_vector_contains(moves, move);
    });

    testSuite.add_test("Bishop move while pinned 1", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "c1"));
        b.place_piece(PieceType::KING, Color::WHITE, "a1");
        b.place_piece(PieceType::ROOK, Color::BLACK, "h1");

        bishop->recalculate();

        auto moves = b.squares_to_moves(bishop->calc_potential_squares_pinned(Direction::RIGHT), bishop);

        assert_equal(0U, moves.size());
    });

    testSuite.add_test("Bishop move while pinned 2", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "c3"));
        b.place_piece(PieceType::KING, Color::WHITE, "a1");
        b.place_piece(PieceType::QUEEN, Color::BLACK, "h8");

        bishop->recalculate();

        auto moves = b.squares_to_moves(bishop->calc_potential_squares_pinned(Direction::UP_RIGHT), bishop);

        assert_equal(6U, moves.size());
        for (auto move : {"Bc3-b2", "Bc3-d4", "Bc3-e5", "Bc3-f6", "Bc3-g7", "Bc3-h8"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;
    });

    return testSuite;
}   