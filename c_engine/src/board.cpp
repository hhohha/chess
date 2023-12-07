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

    _legalMoves.clear();
    _legalMoves.push_back(calc_all_legal_moves());
}

std::vector<Move *> Board::calc_all_legal_moves() {
    return std::vector<Move *>();
}