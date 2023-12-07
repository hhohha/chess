#pragma once

#include <optional>
#include <string>
#include <vector>

#include "king.h"
#include "piece.h"

class Move;
class Square;

class Board {
public:
    Board();
    ~Board();

    void clear();

    Square *get_square(Coordinate c);
    Square *get_square(unsigned int col, unsigned int row);
    Square *get_square(unsigned int idx);
    Square *get_square(std::string name);

    std::vector<Move *> *get_current_legal_moves();

    Piece *place_piece(PieceType kind, Color color, std::string squareName);

    King *get_king(Color color);
    Square *find_first_occupied_square_in_dir(Square *start, Direction dir);

    void load_fen(std::string fen);

//private:
    std::vector<Move> _history;

    Color _turn = Color::WHITE;
    Square *_enPassantPawnSquare = nullptr;  //
    std::vector<unsigned int> _halfMoves = {0};
    unsigned int _fullMoves = 1;
    
    std::vector <std::vector<Move *>> legalMoves;

    // unsigned int _analysisDepth = 0;
    // std::vector<std::vector<Piece *>> piecesRecalculated;

    std::vector<Move *> calc_all_legal_moves();


    std::vector<Piece *> _whitePieces;
    std::vector<Piece *> _blackPieces;
    std::vector<Piece *> _whiteSlidingPieces;
    std::vector<Piece *> _blackSlidingPieces;

    std::vector<std::vector<Move *>> _legalMoves;

private:
    Square _squares[64];
};
