#pragma once

#include <map>
#include <optional>
#include <string>
#include <vector>
#include <set>

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
    Piece *place_piece(PieceType kind, Color color, int squareIdx);
    Piece *place_piece(PieceType kind, Color color, Square *sqr);

    std::vector<Move *> calc_all_legal_moves();
    bool is_in_check(Color color);

    King *get_king(Color color);
    Square *find_first_occupied_square_in_dir(Square *start, Direction dir);

    std::vector<Piece *> & get_pieces(Color color);
    std::vector<Piece *> & get_sliding_pieces(Color color);

    void load_fen(std::string fen);

    bool is_castle_possible(Color color, Direction dir);

    void perform_move(Move *move, bool shouldRecalculate = true);
    void undo_move(bool shouldRecalculate = true);

    void remove_piece(Piece *piece);

    int generate_successors(int depth);

    std::vector<Move *> _history;

    Square * get_en_passant_pawn_square();
    void update_en_passant_pawn_square(Square *sqr);

    Color _turn = Color::WHITE;
    std::vector<Square *>_enPassantPawnSquareHistory = {nullptr};  // this needs to be a vector to keep track of history
    std::vector<unsigned int> _halfMoves = {0U}; // this needs to be a vector to keep track of history
    unsigned int _fullMoves = 1;
    
    std::vector <std::vector<Move *>> legalMoves;

    std::vector<Piece *> _whitePieces;
    std::vector<Piece *> _blackPieces;
    std::vector<Piece *> _whiteSlidingPieces;
    std::vector<Piece *> _blackSlidingPieces;

    std::vector<std::vector<Move *>> _legalMoves;

private:
    std::vector<std::set<Piece *>> _piecesToRecalculate;

    std::vector<Move *> squares_to_moves(std::vector<Square *> squares, Piece *piece);
    void store_piece_in_vectors(Piece *piece);

    std::vector<Square *> get_squares_in_dir(Square *sqr, Direction dir);
    std::tuple<int, int> get_castle_rook_squares(Move *move);
    void update_en_passant_history(Move *move);
    void promote_pawn(Piece *pawn, PieceType kind);
    void recalculation(Move *move);
    void recalculation();

    std::vector<Move *> calc_all_legal_moves_check();
    std::vector<Move *> calc_all_legal_moves_no_check();
    std::map<Piece *, Direction> calc_pinned_pieces(Color color);

    std::vector<Move *> calc_legal_moves_check_move_king();
    std::vector<Move *> calc_legal_moves_check_captures(Piece *attacker, std::map<Piece *, Direction> &pinnedPieces);
    std::vector<Move *> calc_legal_moves_check_blocks(Piece *attacker, std::map<Piece *, Direction> &pinnedPieces);


    std::array<Square, 64> _squares;
};
