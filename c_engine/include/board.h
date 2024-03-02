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

    // python callable methods
    // 1. default constructor void -> void
    // 2. load_fen            string -> void
    // 3. make_move           string -> void
    // 4. undo_move           void -> void
    // 5. get_legal_moves     void -> list of string
    // 6. place_piece         string -> void
    // 7. clear board         void -> void
    // 8. get best move       void -> string
    // setting some configs...
    // get best x moves
    // get move evaluation



    Board();
    ~Board();

    void clear();
    void tprint(){
        for (int i = 0; i < 64; i++) {
            if (i % 8 == 0) {
                std::cout << std::endl;
            }
            std::cout << _squares[i].str() << " ";
        }
        std::cout << std::endl;
    }

    void make_move(std::string moveStr);
    std::string get_legal_moves_str();

    Square *get_square(Coordinate c);
    Square *get_square(int col, int row);
    Square *get_square(int idx);
    Square *get_square(std::string name);

    Piece *place_piece(PieceType kind, Color color, std::string squareName);
    Piece *place_piece(PieceType kind, Color color, int squareIdx);
    Piece *place_piece(PieceType kind, Color color, Square *sqr);

    std::vector<Move *> get_legal_moves();
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

    int test_move_generation(int depth);

    std::vector<Move *> _history;

    Square * get_en_passant_pawn_square();
    void update_en_passant_pawn_square(Square *sqr);

    unsigned int _fullMoves = 1;

    std::vector<Piece *> _whitePieces;
    std::vector<Piece *> _blackPieces;
    std::vector<Piece *> _whiteSlidingPieces;
    std::vector<Piece *> _blackSlidingPieces;

    std::vector<std::vector<Move *>> _legalMoves;

    std::pair<Move, int> get_best_move(int analysisDepth = 4);

private:
    int _leavesAnalysed = 0;
    int _nodesAnalysed = 0;
    Color _originalTurn;

    Color _turn = Color::WHITE;

    std::vector<Square *>_enPassantPawnSquareHistory = {nullptr};  // this needs to be a vector to keep track of history
    std::vector<unsigned int> _halfMoves = {0U}; // this needs to be a vector to keep track of history

    std::vector<std::set<Piece *>> _piecesToRecalculate;

    std::vector<Move *> squares_to_moves(std::vector<Square *> squares, Piece *piece);
    void store_piece_in_vectors(Piece *piece);

    std::vector<Square *> get_squares_in_dir(Square *sqr, Direction dir);
    std::tuple<int, int> get_castle_rook_squares(Move *move);
    void update_en_passant_history(Move *move);
    void promote_pawn(Piece *pawn, PieceType kind);
    void recalculation(Move *move);
    void recalculation();

    int calc_position_score(int depth, int alpha, int beta);
    int estimate_current_position();


    std::vector<Move *> calc_all_legal_moves_check();
    std::vector<Move *> calc_all_legal_moves_no_check();
    std::map<Piece *, Direction> calc_pinned_pieces(Color color);

    std::vector<Move *> calc_legal_moves_check_move_king();
    std::vector<Move *> calc_legal_moves_check_captures(Piece *attacker, std::map<Piece *, Direction> &pinnedPieces);
    std::vector<Move *> calc_legal_moves_check_blocks(Piece *attacker, std::map<Piece *, Direction> &pinnedPieces);

    std::array<Square, 64> _squares;
};
