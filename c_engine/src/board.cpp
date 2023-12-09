#include <regex>

#include "bishop.h"
#include "board.h"
#include "constants.h"
#include "king.h"
#include "knight.h"
#include "pawn.h"
#include "queen.h"
#include "rook.h"
#include "square.h"
#include "move.h"
#include "utils.h"

Board::Board() {
    for(unsigned i = 0; i < 64; ++i) {
        _squares[i].init(i, this);
    }
}

Board::~Board() {
    for (auto piece : _whitePieces)
        delete piece;
    for (auto piece : _blackPieces)
        delete piece;
}

void Board::clear() {
    for (auto &sqr : _squares) {
        sqr._piece = nullptr;
    }
    _whitePieces.clear();
    _blackPieces.clear();
}

Square *Board::get_square(Coordinate c) {
    if (0 <= c.col && c.col < 8 && 0 <= c.row && c.row < 8)
        return &_squares[c.col + c.row*8];
    return nullptr;
}

Square *Board::get_square(unsigned int col, unsigned int row) {
    if (0 <= col && col < 8 && 0 <= row && row < 8)
        return &_squares[col + row*8];
    return nullptr;
}

Square *Board::get_square(unsigned int idx) {
    if (0 <= idx && idx < 64)
        return &_squares[idx];
    return nullptr;
}

Square *Board::get_square(std::string name) {
    if (name.size() == 2 && 'a' <= name[0] && name[0] <= 'h' && '1' <= name[1] && name[1] <= '8')
        return &_squares[square_name_to_idx(name)];
    return nullptr;
}

Piece *Board::place_piece(PieceType kind, Color color, std::string squareName) {

    auto sqr = get_square(squareName);
    ASSERT(sqr != nullptr, "invalid square name");
    ASSERT(sqr->is_free(), squareName + " square is not free");
    
    Piece *piece;
    switch (kind) {
        case PieceType::PAWN:
            piece = new Pawn(color, sqr);
            break;
        case PieceType::KNIGHT:
            piece = new Knight(color, sqr);
            break;
        case PieceType::BISHOP:
            piece = new Bishop(color, sqr);
            break;
        case PieceType::ROOK:
            piece = new Rook(color, sqr);
            break;
        case PieceType::QUEEN:
            piece = new Queen(color, sqr);
            break;
        default:  // KING
            piece = new King(color, sqr);
            break;
    }

    piece->_square = sqr;
    sqr->_piece = piece;

    if (PieceType::KING == kind) {
        if (Color::WHITE == color)
            // king must be the first piece in the list
            _whitePieces.insert(_whitePieces.begin(), piece);
        else
            _blackPieces.insert(_blackPieces.begin(), piece);
    } else {
        if (Color::WHITE == color)
            _whitePieces.push_back(piece);
        else
            _blackPieces.push_back(piece);
    }

    if (PieceType::BISHOP == kind || PieceType::ROOK == kind || PieceType::QUEEN == kind) {
        if (Color::WHITE == color)
            _whiteSlidingPieces.push_back(piece);
        else
            _blackSlidingPieces.push_back(piece);
    }

    return piece;
}


// void Board::remove_piece(Piece *piece) {
//     ASSERT(piece != nullptr, "piece is null");
//     ASSERT(piece->_square != nullptr, "piece is not on the board");
//     ASSERT(!piece->_square->is_free(), "piece is not on the board");

//     for (auto sqr : piece->_attackedSquares) {
//         if (piece->_color == Color::WHITE) {
//             sqr->_attackedByWhites.erase(std::remove(sqr->_attackedByWhites.begin(), sqr->_attackedByWhites.end(), piece), sqr->_attackedByWhites.end());
//             _whitePieces.erase(std::remove(_whitePieces.begin(), _whitePieces.end(), piece), _whitePieces.end());
//             if (piece->_isSliding)
//                 _whiteSlidingPieces.erase(std::remove(_whiteSlidingPieces.begin(), _whiteSlidingPieces.end(), piece), _whiteSlidingPieces.end());
//         }
//         else {
//             sqr->_attackedByBlacks.erase(std::remove(sqr->_attackedByBlacks.begin(), sqr->_attackedByBlacks.end(), piece), sqr->_attackedByBlacks.end());
//             _blackPieces.erase(std::remove(_blackPieces.begin(), _blackPieces.end(), piece), _blackPieces.end());
//             if (piece->_isSliding)
//                 _blackSlidingPieces.erase(std::remove(_blackSlidingPieces.begin(), _blackSlidingPieces.end(), piece), _blackSlidingPieces.end());
//         }
//     }

//     piece->_attackedSquares.clear();
//     piece->_isActive = false;
// }


King *Board::get_king(Color color) {
    // king is always the first piece in the list
    if (Color::WHITE == color)
        return dynamic_cast<King *>(_whitePieces[0]);
    else
        return dynamic_cast<King *>(_blackPieces[0]);
}

Square * Board::find_first_occupied_square_in_dir(Square *sqr, Direction dir) {
    // Find the square with first piece in the given direction from the given square

    Coordinate c(sqr->get_coordinate());
    while (true) {
        move_in_direction(c, dir);
        auto sqr = get_square(c);
        if (sqr == nullptr || !sqr->is_free())
            return sqr;
    }
    return nullptr;
}

void Board::load_fen(std::string fen) {
    clear();

     // doesn't catch all invalid FENs, but it's a good sanity check
    if (!std::regex_match(fen, std::regex("^([rnbqkpRNBQKP1-8]*/){7}[rnbqkpRNBQKP1-8]* [wb] (-|[KQkq]{1,4}) (-|[a-h][36]) [0-9]+ [0-9]+$")))
        throw std::invalid_argument("invalid fen string");

    unsigned int spaceIdx = fen.find(' ');
    auto pieces = fen.substr(0, spaceIdx);
    fen.erase(0, spaceIdx + 1);

    spaceIdx = fen.find(' ');
    auto turn = fen.substr(0, spaceIdx);
    fen.erase(0, spaceIdx + 1);

    spaceIdx = fen.find(' ');
    auto castling = fen.substr(0, spaceIdx);
    fen.erase(0, spaceIdx + 1);

    spaceIdx = fen.find(' ');
    auto enPassantSqr = fen.substr(0, spaceIdx);
    fen.erase(0, spaceIdx + 1);

    spaceIdx = fen.find(' ');
    auto halves = fen.substr(0, spaceIdx);
    fen.erase(0, spaceIdx + 1);

    auto fulls = fen;

    Coordinate coord(0, 7); //  for some reason, FEN starts with a8

    for (auto c : pieces) {
        if (isdigit(c)) {
            coord.col += c - '0';
            continue;
        }
        
        if (c == '/') {
            ASSERT(coord.col == 8, "invalid FEN string");
            coord.col = 0;
            coord.row--;
            continue;
        }

        Color color = isupper(c) ? Color::WHITE : Color::BLACK;
        c = tolower(c);

        PieceType kind;
        if (c == 'p') kind = PieceType::PAWN;
        else if (c == 'n') kind = PieceType::KNIGHT;
        else if (c == 'b') kind = PieceType::BISHOP;
        else if (c == 'r') kind = PieceType::ROOK;
        else if (c == 'q') kind = PieceType::QUEEN;
        else kind = PieceType::KING; // c == 'k'

        place_piece(kind, color, get_square(coord)->get_name());
        coord.col++;
    }

    _turn = turn == "w" ? Color::WHITE : Color::BLACK;

    auto cornerPiece = get_square("h1")->get_piece();
    if (castling.find('K') == std::string::npos && cornerPiece != nullptr && cornerPiece->_kind == PieceType::ROOK && cornerPiece->_color == Color::WHITE)
        cornerPiece->_movesCnt = 1;

    cornerPiece = get_square("a1")->get_piece();
    if (castling.find('Q') == std::string::npos && cornerPiece != nullptr && cornerPiece->_kind == PieceType::ROOK && cornerPiece->_color == Color::WHITE)
        cornerPiece->_movesCnt = 1;

    cornerPiece = get_square("h8")->get_piece();
    if (castling.find('k') == std::string::npos && cornerPiece != nullptr && cornerPiece->_kind == PieceType::ROOK && cornerPiece->_color == Color::BLACK)
        cornerPiece->_movesCnt = 1;

    cornerPiece = get_square("a8")->get_piece();
    if (castling.find('q') == std::string::npos && cornerPiece != nullptr && cornerPiece->_kind == PieceType::ROOK && cornerPiece->_color == Color::BLACK)
        cornerPiece->_movesCnt = 1;

    if (enPassantSqr != "-") {
        // we need the square of the pawn, not the square behind it
        Coordinate coord(enPassantSqr[0] - 'a' + (_turn == Color::WHITE ? 1 : -1), enPassantSqr[1] - '1');
        _enPassantPawnSquare = get_square(coord);
    }

    _halfMoves.clear();
    _halfMoves.push_back(std::stoi(halves));
    _fullMoves = std::stoi(fulls);

    for (auto piece : _whitePieces)
        piece->recalculate();
    for (auto piece : _blackPieces)
        piece->recalculate();

    // _legalMoves.clear();
    // _legalMoves.push_back(calc_all_legal_moves());
}

bool Board::is_in_check(Color color) {
    auto king = get_king(color);
    return king != nullptr && king->_square->is_attacked_by(invert_color(color));
}

std::vector<Move *> Board::calc_all_legal_moves_no_check(){
    std::vector<Move *> legalMoves;
    auto pinnedPieces = calc_pinned_pieces(_turn);

    for (auto piece : get_pieces(_turn)) {
        if (pinnedPieces.find(piece) != pinnedPieces.end()) {
            auto moves = piece->calc_potential_moves_pinned(pinnedPieces[piece]);
            legalMoves.insert(legalMoves.end(), moves.begin(), moves.end());
        } else if (piece->_kind == PieceType::KING) {
            auto moves = dynamic_cast<King *>(piece)->calc_moves_avoiding_check();
            legalMoves.insert(legalMoves.end(), moves.begin(), moves.end());
        } else {
            auto moves = piece->get_potential_moves();
            legalMoves.insert(legalMoves.end(), moves.begin(), moves.end());
        }
    }

    return legalMoves;
}

std::vector<Move *> Board::get_legal_moves_check_move_king(){

    King *king = get_king(_turn);
    auto attackers = king->_square->get_attacked_by(invert_color(_turn));

    std::vector<Square *> inaccessableSquares;
    for (auto piece : attackers) {
        if (piece->_isSliding) {
            auto direction = get_direction(piece->_square, king->_square);
            Coordinate c(king->_square->get_coordinate());
            move_in_direction(c, direction);
            auto sqr = get_square(c);
            if (sqr != nullptr)
                inaccessableSquares.push_back(sqr);
        }
    }
    return king->calc_moves_avoiding_check(&inaccessableSquares);
}

std::vector<Move *> Board::get_legal_moves_check_captures(){

}

std::vector<Move *> Board::get_legal_moves_check_blocks(){

}


std::vector<Move *> Board::calc_all_legal_moves_check(){

    std::vector<Move *> legalMoves = get_legal_moves_check_move_king();
    
    King *king = get_king(_turn);
    ASSERT(king != nullptr, "king is in check but no king found");

    auto attackers = king->_square->get_attacked_by(invert_color(_turn));

    if (attackers.size() == 1) {
        auto pinnedPieces = calc_pinned_pieces(_turn);

        auto attacker = attackers[0];

        
    }

}

std::map<Piece *, Direction> Board::calc_pinned_pieces(Color color){
    // get all pinned pieces of the given color, a pinned piece is the only piece that is between the own king
    // and a sliding piece that would otherwise attack the king
    // the direction is the direction from the king towards the pinner!!!

    auto king = get_king(color);
    if (king == nullptr)
        return {};

    auto pinnedPieces = std::map<Piece *, Direction>();

    // look at all opponent's sliding pieces (rooks, bishops, queens)
    for (auto piece : get_sliding_pieces(invert_color(color))) {
        // if the piece is not on the same row, column (rook, queen) or diagonal (bishop, queen) as the king, it cannot pin
        if (piece->_kind == PieceType::ROOK && !is_same_col_or_row(piece->_square, king->_square))
            continue;
        if (piece->_kind == PieceType::BISHOP && !is_same_diag(piece->_square, king->_square))
            continue;
        if (!is_same_col_or_row(piece->_square, king->_square) && !is_same_diag(piece->_square, king->_square)) // _kind == queen
            continue;

        // go from own king towards the potential pinner: the first piece must be a piece of the same color, otherwise not a pin
        auto direction = get_direction(king->_square, piece->_square);
        auto firstSquare = find_first_occupied_square_in_dir(king->_square, direction);

        ASSERT(firstSquare != nullptr, "the potentially pinned piece not found");
        ASSERT(firstSquare->get_piece() != nullptr, "the potentially pinned piece not found");

        if (firstSquare->get_piece()->_color != color)
            continue;

        // the second piece must be the potential pinner - then all conditions are met, the first piece is pinned
        auto secondSquare = find_first_occupied_square_in_dir(firstSquare, direction);

        ASSERT(secondSquare != nullptr && secondSquare->get_piece(), "the potential pinner not found"); 

        if (secondSquare->get_piece() == piece)
            pinnedPieces[firstSquare->get_piece()] = direction;
    }

    return pinnedPieces;
}

std::vector<Move *> Board::calc_all_legal_moves() {
    if (is_in_check(_turn)) 
        return calc_all_legal_moves_check();
    else
        return calc_all_legal_moves_no_check();
}

std::vector<Piece *> & Board::get_pieces(Color color) {
    return color == Color::WHITE ? _whitePieces : _blackPieces;
}

std::vector<Piece *> & Board::get_sliding_pieces(Color color) {
    return color == Color::WHITE ? _whiteSlidingPieces : _blackSlidingPieces;
}