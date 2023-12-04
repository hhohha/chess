#include "utest.h"
#include "king.h"
#include "board.h"
#include "move.h"

TestSuite create_test_suite_king() {
    TestSuite testSuite("King");

    testSuite.addTest("King construction", []() {
        Board b;
        auto king = dynamic_cast<King*>(b.place_piece(PieceType::KING, Color::WHITE, "a1"));


        assertEqual(PieceType::KING, king->_kind);
        assertEqual(Color::WHITE, king->_color);
        assertEqual("a1", king->_square->get_name());
        assertEqual("K", king->_name);
        assertFalse(king->_isLight, "king is not a light piece");
    });

    testSuite.addTest("King move generation 1", []() {
        Board b;
        auto king = dynamic_cast<King*>(b.place_piece(PieceType::KING, Color::WHITE, "a1"));
        king->recalculate();

        auto moves = king->get_potential_moves();

        assertEqual(3U, moves.size());
        for (auto move : {"Ka1-a2", "Ka1-b1", "Ka1-b2"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("King move generation 2", []() {
        Board b;
        auto king = dynamic_cast<King*>(b.place_piece(PieceType::KING, Color::WHITE, "d4"));
        king->recalculate();

        auto moves = king->get_potential_moves();

        assertEqual(8U, moves.size());
        for (auto move : {"Kd4-c3", "Kd4-c4", "Kd4-c5", "Kd4-d3", "Kd4-d5", "Kd4-e3", "Kd4-e4", "Kd4-e5"})
            assertVectorContain(moves, move);
    });

    return testSuite;
}   