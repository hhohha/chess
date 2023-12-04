#include "constants.h"
#include "king.h"
#include "rook.h"
#include "utest.h"
#include "board.h"
#include "bishop.h"
#include "move.h"

TestSuite create_test_suite_bishop() {
    TestSuite testSuite("Bishop");

    testSuite.addTest("Bishop construction", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "a1"));

        assertEqual(PieceType::BISHOP, bishop->_kind);
        assertEqual(Color::WHITE, bishop->_color);
        assertEqual("a1", bishop->_square->get_name());
        assertEqual("B", bishop->_name);
        assertTrue(bishop->_isLight);

        assertEqual(4U, bishop->_slidingDirections.size());
        assertVectorContain(bishop->_slidingDirections, Direction::DOWN_RIGHT);
        assertVectorContain(bishop->_slidingDirections, Direction::DOWN_LEFT);
        assertVectorContain(bishop->_slidingDirections, Direction::UP_RIGHT);
        assertVectorContain(bishop->_slidingDirections, Direction::UP_LEFT);
    });

    testSuite.addTest("Bishop move generation 1", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "a1"));
        bishop->recalculate();

        auto moves = bishop->get_potential_moves();

        assertEqual(7U, moves.size());
        for (auto move : {"Ba1-b2", "Ba1-c3", "Ba1-d4", "Ba1-e5", "Ba1-f6", "Ba1-g7", "Ba1-h8"})
            assertVectorContain(moves, move);

    });

    testSuite.addTest("Bishop move generation 2", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "d4"));
        bishop->recalculate();

        auto moves = bishop->get_potential_moves();

        assertEqual(13U, moves.size());
        for (auto move : {"Bd4-a1", "Bd4-b2", "Bd4-c3", "Bd4-e5", "Bd4-f6", "Bd4-g7", "Bd4-h8", "Bd4-c5", "Bd4-b6",
            "Bd4-a7", "Bd4-e3", "Bd4-f2", "Bd4-g1"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("Bishop move while pinned 1", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "c1"));
        b.place_piece(PieceType::KING, Color::WHITE, "a1");
        b.place_piece(PieceType::ROOK, Color::BLACK, "h1");

        bishop->recalculate();

        auto moves = bishop->calc_potential_moves_pinned(Direction::RIGHT);

        assertEqual(0U, moves.size());
    });

    testSuite.addTest("Bishop move while pinned 2", []() {
        Board b;
        auto bishop = dynamic_cast<Bishop*>(b.place_piece(PieceType::BISHOP, Color::WHITE, "c3"));
        b.place_piece(PieceType::KING, Color::WHITE, "a1");
        b.place_piece(PieceType::QUEEN, Color::BLACK, "h8");

        bishop->recalculate();

        auto moves = bishop->calc_potential_moves_pinned(Direction::UP_RIGHT);

        assertEqual(6U, moves.size());
        for (auto move : {"Bc3-b2", "Bc3-d4", "Bc3-e5", "Bc3-f6", "Bc3-g7", "Bc3-h8"})
            assertVectorContain(moves, move);

        for (auto move : moves)
            delete move;
    });

    return testSuite;
}   