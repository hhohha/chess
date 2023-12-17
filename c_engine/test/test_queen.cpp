#include "constants.h"
#include "utest.h"
#include "queen.h"
#include "move.h"

#define private public

#include "board.h"

TestSuite create_test_suite_queen() {
    TestSuite testSuite("Queen");

    testSuite.add_test("Queen construction", []() {
        Board b;
        auto queen = dynamic_cast<Queen*>(b.place_piece(PieceType::QUEEN, Color::WHITE, "a1"));

        assert_equal(PieceType::QUEEN, queen->_kind);
        assert_equal(Color::WHITE, queen->_color);
        assert_equal("a1", queen->_square->get_name());
        assert_equal("Q", queen->_name);
        assert_equal(false, queen->_isLight);

        assert_equal(8U, queen->_slidingDirections.size());
        for (auto dir : {Direction::DOWN, Direction::UP, Direction::RIGHT, Direction::LEFT, Direction::DOWN_RIGHT,
            Direction::DOWN_LEFT, Direction::UP_RIGHT, Direction::UP_LEFT}) {
            assert_vector_contains(queen->_slidingDirections, dir);
            }
    });

    testSuite.add_test("Queen move generation 1", []() {
        Board b;
        auto queen = dynamic_cast<Queen*>(b.place_piece(PieceType::QUEEN, Color::WHITE, "a1"));
        queen->recalculate();

        auto moves = b.squares_to_moves(queen->get_potential_squares(), queen);

        assert_equal(21U, moves.size());
        for (auto move : {"Qa1-a2", "Qa1-a3", "Qa1-a4", "Qa1-a5", "Qa1-a6", "Qa1-a7", "Qa1-a8", "Qa1-b1", "Qa1-c1",
            "Qa1-d1", "Qa1-e1", "Qa1-f1", "Qa1-g1", "Qa1-h1", "Qa1-b2", "Qa1-c3", "Qa1-d4", "Qa1-e5", "Qa1-f6",
            "Qa1-g7", "Qa1-h8"})
            assert_vector_contains(moves, move);
    });

    testSuite.add_test("Queen move generation 2", []() {
        Board b;
        auto queen = dynamic_cast<Queen*>(b.place_piece(PieceType::QUEEN, Color::WHITE, "d4"));
        queen->recalculate();

        auto moves = b.squares_to_moves(queen->get_potential_squares(), queen);

        assert_equal(27U, moves.size());
        for (auto move : {"Qd4-a1", "Qd4-b2", "Qd4-c3", "Qd4-e5", "Qd4-f6", "Qd4-g7", "Qd4-h8", "Qd4-c5", "Qd4-b6",
            "Qd4-a7", "Qd4-e3", "Qd4-f2", "Qd4-g1", "Qd4-d1", "Qd4-d2", "Qd4-d3", "Qd4-d5", "Qd4-d6", "Qd4-d7",
            "Qd4-d8", "Qd4-a4", "Qd4-b4", "Qd4-c4", "Qd4-e4", "Qd4-f4", "Qd4-g4", "Qd4-h4"})
            assert_vector_contains(moves, move);
    });

    testSuite.add_test("Queen move while pinned 1", []() {
        Board b;
        auto queen = dynamic_cast<Queen*>(b.place_piece(PieceType::QUEEN, Color::WHITE, "c2"));
        b.place_piece(PieceType::KING, Color::WHITE, "b1");
        b.place_piece(PieceType::QUEEN, Color::BLACK, "e4");

        queen->recalculate();

        auto moves = b.squares_to_moves(queen->calc_potential_squares_pinned(Direction::UP_RIGHT), queen);

        assert_equal(2U, moves.size());
        assert_vector_contains(moves, "Qc2-d3");
        assert_vector_contains(moves, "Qc2-e4");

        for (auto move : moves)
            delete move;
    });

    return testSuite;
}   