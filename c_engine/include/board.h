#pragma once

#include <optional>
#include <string>
#include <vector>

#include "piece.h"
#include "pawn.h"   // to delete
#include "knight.h"   // to delete


#include "constants.h"

class Coordinate;

class Move;
class Square;
class Pawn;
class Knight;
class Bishop;
class Rook;
class Queen;
class King;
class Board;

class PieceIterator {
    using iterator_category = std::input_iterator_tag;
    using difference_type   = std::ptrdiff_t;
    using value_type        = Piece;
    using pointer           = Piece*;
    using reference         = Piece&;

public:
    PieceIterator(Board *board, Color color, bool end = false);

    Piece &operator*() const;
    Piece *operator->();

    PieceIterator &operator++();


/*
    
    PieceIterator operator++(int);

    bool operator==(const PieceIterator &other);
    bool operator!=(const PieceIterator &other);
    */
private:
    void verify_ptr_not_at_end();

    Board *_board;
    Color _color;
    Piece *_ptr;
    std::vector<std::vector<Piece *> *> _pieceLists;  // vectors which we want to iterate over
    unsigned int _currentPieceListIdx;
};

class Board {
public:
    Board();

    void clear();

    Square *get_square(Coordinate c);
    Square *get_square(unsigned int col, unsigned int row);
    Square *get_square(unsigned int idx);
    Square *get_square(std::string name);

    std::vector<Move *> *get_current_legal_moves();

//private:
    std::vector<Move> _history;
    std::vector<Square> _squares;

    Color _turn = Color::WHITE;
    Square *_enPassantSquare = nullptr;
    std::vector<unsigned int> _halfMoves = {0};
    unsigned int _fullMoves = 1;
    
    std::vector <std::vector<Move *>> legalMoves;

    // unsigned int _analysisDepth = 0;
    // std::vector<std::vector<Piece *>> piecesRecalculated;

/*
    std::vector<Pawn *> _whitePawns;
    std::vector<Pawn *> _blackPawns;
    std::vector<Knight *> _whiteKnights;
    std::vector<Knight *> _blackKnights;
    std::vector<Bishop *> _whiteBishops;
    std::vector<Bishop *> _blackBishops;
    std::vector<Rook *> _whiteRooks;
    std::vector<Rook *> _blackRooks;
    std::vector<Queen *> _whiteQueens;
    std::vector<Queen *> _blackQueens;
    std::vector<King *> _whiteKings;
    std::vector<King *> _blackKings;
    */

    std::vector<Piece *> _whitePawns;
    std::vector<Piece *> _blackPawns;
    std::vector<Piece *> _whiteKnights;
    std::vector<Piece *> _blackKnights;
    std::vector<Piece *> _whiteBishops;
    std::vector<Piece *> _blackBishops;
    std::vector<Piece *> _whiteRooks;
    std::vector<Piece *> _blackRooks;
    std::vector<Piece *> _whiteQueens;
    std::vector<Piece *> _blackQueens;
    std::vector<Piece *> _whiteKings;
    std::vector<Piece *> _blackKings;
};
