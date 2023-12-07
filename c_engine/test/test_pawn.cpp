#include "utest.h"
#include "board.h"
#include "pawn.h"
#include "move.h"
#include "constants.h"

TestSuite create_test_suite_pawn() {
    TestSuite testSuite("Pawn");

    testSuite.addTest("Pawn construction", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "a2"));

        assertEqual(PieceType::PAWN, pawn->_kind);
        assertEqual(Color::WHITE, pawn->_color);
        assertEqual("a2", pawn->_square->get_name());
        assertEqual("p", pawn->_name);
        assertFalse(pawn->_isLight);
    });

    testSuite.addTest("Pawn move generation 1", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "a2"));

        auto moves = pawn->get_potential_moves();

        assertEqual(2U, moves.size());
        assertVectorContain(moves, "pa2-a3");
        assertVectorContain(moves, "pa2-a4");
    });

    testSuite.addTest("Pawn move generation 2", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "d4"));

        auto moves = pawn->get_potential_moves();

        assertEqual(1U, moves.size());
        assertVectorContain(moves, "pd4-d5");
    });

    testSuite.addTest("Pawn move generation 3", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "h7"));

        auto moves = pawn->get_potential_moves();

        assertEqual(4U, moves.size());
        for (auto move : {"ph7-h8Q", "ph7-h8R", "ph7-h8B", "ph7-h8N"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("Pawn move generation 4", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "c7"));
        b.place_piece(PieceType::ROOK, Color::BLACK, "b8");
        b.place_piece(PieceType::ROOK, Color::BLACK, "d8");

        auto moves = pawn->get_potential_moves();

        assertEqual(12U, moves.size());
        for (auto move : {"pc7-c8Q", "pc7-c8R", "pc7-c8B", "pc7-c8N", "pc7-b8Q", "pc7-b8R", "pc7-b8B", "pc7-b8N",
            "pc7-d8Q", "pc7-d8R", "pc7-d8B", "pc7-d8N"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("Pawn move generation 5", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "e2"));
        b.place_piece(PieceType::ROOK, Color::BLACK, "d3");
        b.place_piece(PieceType::ROOK, Color::BLACK, "e4");
        b.place_piece(PieceType::PAWN, Color::WHITE, "f3");

        auto moves = pawn->get_potential_moves();

        assertEqual(2U, moves.size());
        for (auto move : {"pe2-e3", "pe2-d3"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("Test en passant 1", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "e5"));
        b.place_piece(PieceType::PAWN, Color::BLACK, "d5");
        b._enPassantPawnSquare = b.get_square("d5");

        auto moves = pawn->get_potential_moves();

        assertEqual(2U, moves.size());
        for (auto move : {"pe5-e6", "pe5-d6"})
            assertVectorContain(moves, move);
    });

    testSuite.addTest("Test en passant pin", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "e5"));
        b.place_piece(PieceType::PAWN, Color::BLACK, "d5");
        b._enPassantPawnSquare = b.get_square("d5");
        b.place_piece(PieceType::ROOK, Color::BLACK, "b5");
        b.place_piece(PieceType::KING, Color::WHITE, "h5");
        b.place_piece(PieceType::PAWN, Color::BLACK, "f6");

        auto moves = pawn->get_potential_moves();

        assertEqual(2U, moves.size());
        for (auto move : {"pe5-e6", "pe5-f6"})
            assertVectorContain(moves, move);

        b.place_piece(PieceType::PAWN, Color::BLACK, "c5");
        
        moves = pawn->get_potential_moves();

        assertEqual(3U, moves.size());
        for (auto move : {"pe5-e6", "pe5-f6", "pe5-d6"})
            assertVectorContain(moves, move);

    });
            
    return testSuite;
}