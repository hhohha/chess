#include "board.h"
#include "constants.h"
#include "knight.h"
#include "utest.h"
#include "move.h"

TestSuite create_test_suite_knight() {
    TestSuite testSuite("Knight");

    testSuite.addTest("Knight construction", []() {
        Board b;
        auto knight = dynamic_cast<Knight*>(b.place_piece(PieceType::KNIGHT, Color::WHITE, "a1"));

        assertEqual(PieceType::KNIGHT, knight->_kind);
    });
    
    testSuite.addTest("Knight move generation 1", []() {
        Board b;
        auto knight = dynamic_cast<Knight*>(b.place_piece(PieceType::KNIGHT, Color::WHITE, "a1"));
        knight->recalculate();

        auto moves = knight->get_potential_moves();

        assertEqual(2U, moves.size());
        for (auto move : {"Na1-b3", "Na1-c2"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("Knight move generation 2", []() {
        Board b;
        auto knight = dynamic_cast<Knight*>(b.place_piece(PieceType::KNIGHT, Color::WHITE, "d4"));
        knight->recalculate();

        auto moves = knight->get_potential_moves();

        assertEqual(8U, moves.size());
        for (auto move : {"Nd4-b3", "Nd4-b5", "Nd4-c2", "Nd4-c6", "Nd4-e2", "Nd4-e6", "Nd4-f3", "Nd4-f5"})
            assertVectorContain(moves, move);
    });

    return testSuite;
}