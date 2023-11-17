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


    std::vector<Piece *> _whitePieces;
    std::vector<Piece *> _blackPieces;
    // TODO: std::vector<Piece *> _whiteSlidingPieces;
    // TODO: std::vector<Piece *> _blackSlidingPieces;
};
