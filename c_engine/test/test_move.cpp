#include "utest.h"
#include "move.h"
#include "bishop.h"
#include "pawn.h"
#include "square.h"
#include "board.h"
#include <optional>

TestSuite create_test_suite_moves() {
    TestSuite testSuite("Moves");

    testSuite.add_test("Move construction", []() {
        Board b;
        Square *pieceSqr = b.get_square("a1");
        Bishop bishop(Color::WHITE, pieceSqr);

        Square *destSqr = b.get_square("h8");

        Move move(&bishop, destSqr);

        assert_equal(&bishop, move.get_piece());
        assert_equal(destSqr, move.get_to_sqr());
        assert_false(move.is_promotion());
        assert_false(move.is_castling());

        assert_equal("Ba1-h8", move.str());
        assert_equal(pieceSqr, move.get_from_sqr());
        assert_equal(destSqr, move.get_to_sqr());
        assert_is_null(move.get_piece_taken());
        assert_false(move.get_new_piece().has_value());
        assert_false(move.is_en_passant());
    });

    
    testSuite.add_test("Move comparison", []() {
        Board b;
        Square *pieceSqr1 = b.get_square("a1");
        Square *pieceSqr2 = b.get_square("b2");
        Bishop bishop1(Color::WHITE, pieceSqr1);
        Bishop bishop2(Color::WHITE, pieceSqr2);

        Square *destSqr1 = b.get_square("h8");
        Square *destSqr2 = b.get_square("g7");

        Move move1(&bishop1, destSqr1);
        Move move2(&bishop1, destSqr1);
        Move move3(&bishop1, destSqr2);
        Move move4(&bishop2, destSqr1);

        assert_true(move1 == move2); // Same piece, same destination square
        assert_false(move1 == move3); // Same piece, different destination square
        assert_false(move1 == move4); // Different piece, same destination square
    });

    
    testSuite.add_test("Pawn promotion move comparison", []() {
        Board b;
        Square *pieceSqr1 = b.get_square("a7");
        Square *pieceSqr2 = b.get_square("b2");
        Pawn pawn1(Color::WHITE, pieceSqr1);
        Pawn pawn2(Color::WHITE, pieceSqr2);
        

        Square *destSqr1 = b.get_square("a8");
        Square *destSqr2 = b.get_square("b1");

        Move move1(&pawn1, destSqr1, PieceType::QUEEN);
        Move move2(&pawn1, destSqr1, PieceType::QUEEN);
        Move move3(&pawn1, destSqr1, PieceType::ROOK);
        Move move4(&pawn2, destSqr2, PieceType::KNIGHT);

        assert_true(move1 == move2); // Same piece, same destination square, same promotion piece
        assert_false(move1 == move3); // Same piece, same destination square, different promotion piece
        assert_false(move1 == move4); // Different piece, different destination square, different promotion piece
    });

    return testSuite;
}