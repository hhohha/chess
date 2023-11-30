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
        Square *sqr = b.get_square("a1");
        Bishop bishop(Color::WHITE, sqr);

        assertEqual(PieceType::BISHOP, bishop._kind);
        assertEqual(Color::WHITE, bishop._color);
        assertEqual(sqr, bishop._square);
        assertEqual("B", bishop._name);
        assertEqual(true, bishop._isLight);

        assertEqual(4U, bishop._slidingDirections.size());
        assertEqual(Direction::DOWN_RIGHT, bishop._slidingDirections[0]);
        assertEqual(Direction::DOWN_LEFT, bishop._slidingDirections[1]);
        assertEqual(Direction::UP_RIGHT, bishop._slidingDirections[2]);
        assertEqual(Direction::UP_LEFT, bishop._slidingDirections[3]);
    });

    testSuite.addTest("Bishop move generation 1", []() {
        Board b;
        Bishop bishop(Color::WHITE, b.get_square("a1"));
        bishop.recalculate();

        auto moves = bishop.get_potential_moves();

        assertEqual(7U, moves.size());
        for (auto move : {"Ba1-b2", "Ba1-c3", "Ba1-d4", "Ba1-e5", "Ba1-f6", "Ba1-g7", "Ba1-h8"})
            assertVectorContain(moves, move);

    });

    testSuite.addTest("Bishop move generation 2", []() {
        Board b;
        Bishop bishop(Color::WHITE, b.get_square("d4"));
        bishop.recalculate();

        auto moves = bishop.get_potential_moves();

        assertEqual(13U, moves.size());
        for (auto move : {"Bd4-a1", "Bd4-b2", "Bd4-c3", "Bd4-e5", "Bd4-f6", "Bd4-g7", "Bd4-h8", "Bd4-c5", "Bd4-b6",
            "Bd4-a7", "Bd4-e3", "Bd4-f2", "Bd4-g1"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("Bishop move while pinned 1", []() {
        Board b;
        Bishop bishop(Color::WHITE, b.get_square("c1"));
        King king(Color::WHITE, b.get_square("a1"));
        Rook rook(Color::BLACK, b.get_square("h1"));

        bishop.recalculate();

        auto moves = bishop.calc_potential_moves_pinned(Direction::RIGHT);

        assertEqual(0U, moves.size());
    });

    // testSuite.addTest("Bishop move while pinned 2", []() {
    //     Board b;
    //     Bishop bishop(Color::WHITE, b.get_square("c3"));
    //     King king(Color::WHITE, b.get_square("a1"));
    //     Bishop bishop2(Color::BLACK, b.get_square("h8"));

    //     bishop.recalculate();

    //     auto moves = bishop.calc_potential_moves_pinned(Direction::UP_RIGHT);

    //     assertEqual(6U, moves.size());
    //     for (auto move : {"Bc3-b2", "Bc3-d4", "Bc3-e5", "Bc3-f6", "Bc3-g7", "Bc3-h8"})
    //         assertVectorContain(moves, move);
    // });

    return testSuite;
}   