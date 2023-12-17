#include "utest.h"
#include "pawn.h"
#include "move.h"
#include "constants.h"

#define private public

#include "board.h"

TestSuite create_test_suite_pawn() {
    TestSuite testSuite("Pawn");

    testSuite.add_test("Pawn construction", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "a2"));

        assert_equal(PieceType::PAWN, pawn->_kind);
        assert_equal(Color::WHITE, pawn->_color);
        assert_equal("a2", pawn->_square->get_name());
        assert_equal("p", pawn->_name);
        assert_false(pawn->_isLight);
    });

    testSuite.add_test("Pawn move generation 1", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "a2"));

        auto moves = b.squares_to_moves(pawn->get_potential_squares(), pawn);

        assert_equal(2U, moves.size());
        assert_vector_contains(moves, "pa2-a3");
        assert_vector_contains(moves, "pa2-a4");

        for (auto move : moves)
            delete move;
    });

    testSuite.add_test("Pawn move generation 2", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "d4"));

        auto moves = b.squares_to_moves(pawn->get_potential_squares(), pawn);

        assert_equal(1U, moves.size());
        assert_vector_contains(moves, "pd4-d5");

        for (auto move : moves)
            delete move;
    });

    testSuite.add_test("Pawn move generation 3", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "h7"));

        auto moves = b.squares_to_moves(pawn->get_potential_squares(), pawn);

        assert_equal(4U, moves.size());
        for (auto move : {"ph7-h8Q", "ph7-h8R", "ph7-h8B", "ph7-h8N"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;
    });

    testSuite.add_test("Pawn move generation 4", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "c7"));
        b.place_piece(PieceType::ROOK, Color::BLACK, "b8");
        b.place_piece(PieceType::ROOK, Color::BLACK, "d8");

        auto moves = b.squares_to_moves(pawn->get_potential_squares(), pawn);

        assert_equal(12U, moves.size());
        for (auto move : {"pc7-c8Q", "pc7-c8R", "pc7-c8B", "pc7-c8N", "pc7-b8Q", "pc7-b8R", "pc7-b8B", "pc7-b8N",
            "pc7-d8Q", "pc7-d8R", "pc7-d8B", "pc7-d8N"})
            assert_vector_contains(moves, move);
        
        for (auto move : moves)
            delete move;
    });

    testSuite.add_test("Pawn move generation 5", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "e2"));
        b.place_piece(PieceType::ROOK, Color::BLACK, "d3");
        b.place_piece(PieceType::ROOK, Color::BLACK, "e4");
        b.place_piece(PieceType::PAWN, Color::WHITE, "f3");

        auto moves = b.squares_to_moves(pawn->get_potential_squares(), pawn);

        assert_equal(2U, moves.size());
        for (auto move : {"pe2-e3", "pe2-d3"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;
    });

    testSuite.add_test("Test en passant 1", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "e5"));
        b.place_piece(PieceType::PAWN, Color::BLACK, "d5");
        b.update_en_passant_pawn_square(b.get_square("d5"));

        auto moves = b.squares_to_moves(pawn->get_potential_squares(), pawn);

        assert_equal(2U, moves.size());
        for (auto move : {"pe5-e6", "pe5-d6"})
            assert_vector_contains(moves, move);
    
        for (auto move : moves)
            delete move;
    });

    testSuite.add_test("Test en passant pin", []() {
        Board b;
        auto pawn = dynamic_cast<Pawn*>(b.place_piece(PieceType::PAWN, Color::WHITE, "e5"));
        b.place_piece(PieceType::PAWN, Color::BLACK, "d5");
        b.update_en_passant_pawn_square(b.get_square("d5"));
        b.place_piece(PieceType::ROOK, Color::BLACK, "b5");
        b.place_piece(PieceType::KING, Color::WHITE, "h5");
        b.place_piece(PieceType::PAWN, Color::BLACK, "f6");

        auto moves = b.squares_to_moves(pawn->get_potential_squares(), pawn);

        assert_equal(2U, moves.size());
        for (auto move : {"pe5-e6", "pe5-f6"})
            assert_vector_contains(moves, move);
    
        for (auto move : moves)
            delete move;

        b.place_piece(PieceType::PAWN, Color::BLACK, "c5");
        
        moves = b.squares_to_moves(pawn->get_potential_squares(), pawn);

        assert_equal(3U, moves.size());
        for (auto move : {"pe5-e6", "pe5-f6", "pe5-d6"})
            assert_vector_contains(moves, move);

        for (auto move : moves)
            delete move;

    });
            
    return testSuite;
}