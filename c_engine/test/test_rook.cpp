#include "board.h"
#include "rook.h"
#include "move.h"
#include "utest.h"

TestSuite create_test_suite_rook() {
    TestSuite testSuite("Rook");

    testSuite.addTest("Rook construction", []() {
        Board b;
        auto rook = dynamic_cast<Rook*>(b.place_piece(PieceType::ROOK, Color::WHITE, "a1"));

        assertEqual(PieceType::ROOK, rook->_kind);
        assertEqual(Color::WHITE, rook->_color);
        assertEqual("a1", rook->_square->get_name());
        assertEqual("R", rook->_name);
        assertEqual(false, rook->_isLight);

        assertEqual(4U, rook->_slidingDirections.size());
        assertVectorContain(rook->_slidingDirections, Direction::DOWN);
        assertVectorContain(rook->_slidingDirections, Direction::UP);
        assertVectorContain(rook->_slidingDirections, Direction::RIGHT);
        assertVectorContain(rook->_slidingDirections, Direction::LEFT);
    });

    testSuite.addTest("Rook move generation 1", []() {
        Board b;
        auto rook = dynamic_cast<Rook*>(b.place_piece(PieceType::ROOK, Color::WHITE, "a1"));
        rook->recalculate();

        auto moves = rook->get_potential_moves();

        assertEqual(14U, moves.size());
        for (auto move : {"Ra1-a2", "Ra1-a3", "Ra1-a4", "Ra1-a5", "Ra1-a6", "Ra1-a7", "Ra1-a8", "Ra1-b1", "Ra1-c1",
            "Ra1-d1", "Ra1-e1", "Ra1-f1", "Ra1-g1", "Ra1-h1"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("Rook move while pinned 1", []() {
        Board b;
        auto rook = dynamic_cast<Rook*>(b.place_piece(PieceType::ROOK, Color::WHITE, "c2"));
        b.place_piece(PieceType::KING, Color::WHITE, "b1");
        b.place_piece(PieceType::QUEEN, Color::BLACK, "e4");

        rook->recalculate();

        auto moves = rook->calc_potential_moves_pinned(Direction::UP_RIGHT);

        assertEqual(0U, moves.size());
    });

    testSuite.addTest("Rook move while pinned 2", []() {
        Board b;
        auto rook = dynamic_cast<Rook*>(b.place_piece(PieceType::ROOK, Color::WHITE, "d1"));
        b.place_piece(PieceType::KING, Color::WHITE, "b1");
        b.place_piece(PieceType::QUEEN, Color::BLACK, "g1");

        rook->recalculate();

        auto moves = rook->calc_potential_moves_pinned(Direction::RIGHT);

        assertEqual(4U, moves.size());
        for (auto move : {"Rd1-c1", "Rd1-e1", "Rd1-f1", "Rd1-g1"})
            assertVectorContain(moves, move);
    });

    return testSuite;
}   