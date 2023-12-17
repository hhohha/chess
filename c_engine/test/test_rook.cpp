#include "rook.h"
#include "move.h"
#include "utest.h"

#define private public

#include "board.h"

TestSuite create_test_suite_rook() {
    TestSuite testSuite("Rook");

    testSuite.add_test("Rook construction", []() {
        Board b;
        auto rook = dynamic_cast<Rook*>(b.place_piece(PieceType::ROOK, Color::WHITE, "a1"));

        assert_equal(PieceType::ROOK, rook->_kind);
        assert_equal(Color::WHITE, rook->_color);
        assert_equal("a1", rook->_square->get_name());
        assert_equal("R", rook->_name);
        assert_equal(false, rook->_isLight);

        assert_equal(4U, rook->_slidingDirections.size());
        assert_vector_contains(rook->_slidingDirections, Direction::DOWN);
        assert_vector_contains(rook->_slidingDirections, Direction::UP);
        assert_vector_contains(rook->_slidingDirections, Direction::RIGHT);
        assert_vector_contains(rook->_slidingDirections, Direction::LEFT);
    });

    testSuite.add_test("Rook move generation 1", []() {
        Board b;
        auto rook = dynamic_cast<Rook*>(b.place_piece(PieceType::ROOK, Color::WHITE, "a1"));
        rook->recalculate();

        auto moves = b.squares_to_moves(rook->get_potential_squares(), rook);

        assert_equal(14U, moves.size());
        for (auto move : {"Ra1-a2", "Ra1-a3", "Ra1-a4", "Ra1-a5", "Ra1-a6", "Ra1-a7", "Ra1-a8", "Ra1-b1", "Ra1-c1",
            "Ra1-d1", "Ra1-e1", "Ra1-f1", "Ra1-g1", "Ra1-h1"})
            assert_vector_contains(moves, move);
    });

    testSuite.add_test("Rook move while pinned 1", []() {
        Board b;
        auto rook = dynamic_cast<Rook*>(b.place_piece(PieceType::ROOK, Color::WHITE, "c2"));
        b.place_piece(PieceType::KING, Color::WHITE, "b1");
        b.place_piece(PieceType::QUEEN, Color::BLACK, "e4");

        rook->recalculate();

        auto moves = b.squares_to_moves(rook->calc_potential_squares_pinned(Direction::UP_RIGHT), rook);

        assert_equal(0U, moves.size());
    });

    testSuite.add_test("Rook move while pinned 2", []() {
        Board b;
        auto rook = dynamic_cast<Rook*>(b.place_piece(PieceType::ROOK, Color::WHITE, "d1"));
        b.place_piece(PieceType::KING, Color::WHITE, "b1");
        b.place_piece(PieceType::QUEEN, Color::BLACK, "g1");

        rook->recalculate();

        auto moves = b.squares_to_moves(rook->calc_potential_squares_pinned(Direction::RIGHT), rook);

        assert_equal(4U, moves.size());
        for (auto move : {"Rd1-c1", "Rd1-e1", "Rd1-f1", "Rd1-g1"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;
    });

    return testSuite;
}   