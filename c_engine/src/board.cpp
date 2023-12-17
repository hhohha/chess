#include <optional>
#include <regex>
#include <set>


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
    return place_piece(kind, color, get_square(squareName));
}

Piece *Board::place_piece(PieceType kind, Color color, int squareIdx) {
    return place_piece(kind, color, get_square(squareIdx));
}

Piece *Board::place_piece(PieceType kind, Color color, Square *sqr) {
    ASSERT(sqr->is_free(), sqr->_name + " square is not free");
    ASSERT(sqr != nullptr, "invalid square name");
    
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

Square * Board::get_en_passant_pawn_square(){
    ASSERT(_enPassantPawnSquareHistory.size() > 0, "en passant pawn square history is empty");
    return _enPassantPawnSquareHistory.back();
}

void Board::update_en_passant_pawn_square(Square *sqr){
    ASSERT(_enPassantPawnSquareHistory.size() > 0, "en passant pawn square history is empty");
    //_enPassantPawnSquareHistory.pop_back();
    //_enPassantPawnSquareHistory.push_back(sqr);
    _enPassantPawnSquareHistory.back() = sqr;
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

        place_piece(kind, color, get_square(coord));
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
        update_en_passant_pawn_square(get_square(coord));
    }

    _halfMoves.clear();
    _halfMoves.push_back(std::stoi(halves));
    _fullMoves = std::stoi(fulls);

    for (auto piece : _whitePieces)
        piece->recalculate();
    for (auto piece : _blackPieces)
        piece->recalculate();

    _legalMoves.clear();
    //_legalMoves.push_back(calc_all_legal_moves());
}

std::vector<Square *> Board::get_squares_in_dir(Square *sqr, Direction dir){
    // Get all empty squares in the given direction from the given square

    std::vector<Square *> squares;
    Coordinate c(sqr->get_coordinate());

    while (true) {
        move_in_direction(c, dir);
        auto sqr = get_square(c);
        if (sqr == nullptr || !sqr->is_free())
            return squares;
        squares.push_back(sqr);
    }    
}

bool Board::is_in_check(Color color) {
    auto king = get_king(color);
    return king != nullptr && king->_square->is_attacked_by(invert_color(color));
}

bool Board::is_castle_possible(Color color, Direction side) {
    // Checks the preconditions for castling

    ASSERT(side == Direction::LEFT || side == Direction::RIGHT, "invalid direction");
    Square *kingSqr, *rookSqr, *rookPassingSqr, *kingPassingSqr, *kingDestSqr;

    // based on color and side, get the king and the rook squares, also the king passing squares and the rook passing square
    // the king passing and destination squares need to be empty and not attacked by the opponent
    // the rook passing square needs (just b1 or b8) to be empty
    if (color == Color::WHITE) {
        kingSqr = get_square(4);                             // e1
        if (side == Direction::RIGHT) {
            rookSqr = get_square(7);                         // h1
            kingPassingSqr = get_square(5);                  // f1
            kingDestSqr = get_square(6);                     // g1
            rookPassingSqr = nullptr;
        } else {
            rookSqr = get_square(0);                         // a1
            kingPassingSqr = get_square(3);                  // d1
            kingDestSqr = get_square(2);                     // c1
            rookPassingSqr = get_square(1);                  // b1
        }
    } else {
        kingSqr = get_square(60);                            // e8
        if (side == Direction::RIGHT) {
            rookSqr = get_square(63);                        // h8
            kingPassingSqr = get_square(61);                 // f8
            kingDestSqr = get_square(62);                    // g8
            rookPassingSqr = nullptr;
        } else {
            rookSqr = get_square(56);                        // a8
            kingPassingSqr = get_square(59);                 // d8
            kingDestSqr = get_square(58);                    // c8
            rookPassingSqr = get_square(57);                 // b8
        }
    }

    // the king must be on its initial square and not moved
    if (kingSqr->get_piece() == nullptr || kingSqr->get_piece()->_kind != PieceType::KING || kingSqr->get_piece()->_color != color ||
        kingSqr->get_piece()->_movesCnt > 0)
        return false;

    // the rook must be on its initial square and not moved
    if (rookSqr->get_piece() == nullptr || rookSqr->get_piece()->_kind != PieceType::ROOK || rookSqr->get_piece()->_color != color ||
        rookSqr->get_piece()->_movesCnt > 0)
        return false;

    // the king cannot be in check
    if (is_in_check(color))
        return false;

    // the king passing and destination squares must be empty and not attacked by the opponent
    if (!kingPassingSqr->is_free() || !kingDestSqr->is_free() || kingPassingSqr->is_attacked_by(invert_color(color)) ||
        kingDestSqr->is_attacked_by(invert_color(color)))
        return false;

    // if castling queenside, the rook passing square must be empty
    if (side == Direction::LEFT && !rookPassingSqr->is_free())
        return false;

    return true;
}

std::vector<Move *> Board::squares_to_moves(std::vector<Square *> squares, Piece *piece) {
    std::vector<Move *> moves;
    for (auto sqr : squares) {
        if (piece->_kind == PieceType::PAWN && sqr->get_row() == (piece->_color == Color::WHITE ? 7 : 0)) {
            for (auto newPiece : {PieceType::KNIGHT, PieceType::BISHOP, PieceType::ROOK, PieceType::QUEEN})
                moves.push_back(new Move(piece, sqr, newPiece));
        } else {
            moves.push_back(new Move(piece, sqr));
            if (piece->_kind == PieceType::PAWN && sqr->get_piece() == nullptr && sqr->get_col() != piece->_square->get_col())
                moves.back()->mark_as_en_passant();
        }
    }
    return moves;
}

std::vector<Move *> Board::calc_all_legal_moves_no_check(){
    std::vector<Move *> legalMoves;
    auto pinnedPieces = calc_pinned_pieces(_turn);

    for (auto piece : get_pieces(_turn)) {
        std::vector<Square *> squares;

        if (pinnedPieces.find(piece) != pinnedPieces.end())
            squares = piece->calc_potential_squares_pinned(pinnedPieces[piece]);
        else if (piece->_kind == PieceType::KING)
            squares = dynamic_cast<King *>(piece)->calc_squares_avoiding_check();
        else 
            squares = piece->get_potential_squares();
            
        for (auto move : squares_to_moves(squares, piece))
                legalMoves.push_back(move);
    }

    // castling
    auto king = get_king(_turn);
    if (king != nullptr) {
        if (is_castle_possible(_turn, Direction::RIGHT))
            legalMoves.push_back(new Move(king, get_square(king->_square->get_col() + 2, king->_square->get_row())));
        if (is_castle_possible(_turn, Direction::LEFT))
            legalMoves.push_back(new Move(king, get_square(king->_square->get_col() - 2, king->_square->get_row())));
    }

    return legalMoves;
}

std::vector<Move *> Board::calc_legal_moves_check_move_king(){

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

    std::vector<Move *> legalMoves;
    for (auto sqr : king->calc_squares_avoiding_check(&inaccessableSquares)) 
        legalMoves.push_back(new Move(king, sqr));

    return legalMoves;
}

std::vector<Move *> Board::calc_legal_moves_check_captures(Piece *attacker, std::map<Piece *, Direction> &pinnedPieces){
    // Get all legal capture moves of the current player provided that the king is in check (captures of the attacker)

    std::vector<Move *> legalMoves;

    for (auto piece : attacker->get_square()->get_attacked_by(_turn)) {
        // a pinned piece cannot capture the attacker
        if (pinnedPieces.find(piece) != pinnedPieces.end())
            continue;

        if (piece->_kind == PieceType::PAWN) {
            for (auto move : squares_to_moves({attacker->_square}, piece))
                legalMoves.push_back(move);
            
        } else if (piece->_kind != PieceType::KING)
            legalMoves.push_back(new Move(piece, attacker->_square));
    }

    // the attacker can also be captured en passant
    auto enPassantPawnSquare = get_en_passant_pawn_square();
    if (enPassantPawnSquare != nullptr && attacker->_square == enPassantPawnSquare) {
        ASSERT(attacker->_kind == PieceType::PAWN, "en passant capture by non-pawn");

        for (int offset : {-1, 1}) {
            auto potentialPawnSqr = get_square(enPassantPawnSquare->get_col() + offset, enPassantPawnSquare->get_row());
            if (potentialPawnSqr != nullptr && potentialPawnSqr->get_piece() != nullptr &&
                potentialPawnSqr->get_piece()->_kind == PieceType::PAWN && potentialPawnSqr->get_piece()->_color == _turn) {

                legalMoves.push_back(new Move(potentialPawnSqr->get_piece(), get_square(attacker->_square->get_col(),
                    attacker->_square->get_row() + (attacker->_color == Color::WHITE ? 1 : -1))));
            }
        }
    }

    return legalMoves;
}

std::vector<Move *> Board::calc_legal_moves_check_blocks(Piece *attacker, std::map<Piece *, Direction> &pinnedPieces){
    // Get all legal blocking moves of the current player provided that the king is in check

    std::vector<Move *> legalMoves;

    auto king = get_king(_turn);
    ASSERT(king != nullptr, "king is in check but no king found");

    auto direction = get_direction(king->_square, attacker->_square);

    // look at all the squares between the king and the attacker - what pieces can access them?
    for (auto blockingSquare : get_squares_in_dir(king->_square, direction)) {
        for (auto piece : blockingSquare->get_attacked_by(_turn)) {
            // a pinned piece cannot block the attacker, king cannot block, pawn cannot block to a place it is attacking (diagonally)
            if (piece->_kind != PieceType::PAWN && piece->_kind != PieceType::KING && pinnedPieces.find(piece) == pinnedPieces.end())
                legalMoves.push_back(new Move(piece, blockingSquare));
        }

        // look one square in the direction of attackers pawns, if there is a defending pawn, it can block the attack
        // consider potential promotion as well
        auto potentialPawnSqr = get_square(blockingSquare->get_col(), blockingSquare->get_row() + (attacker->_color == Color::WHITE ? 1 : -1));
        if(potentialPawnSqr != nullptr && potentialPawnSqr->get_piece() != nullptr && potentialPawnSqr->get_piece()->_kind == PieceType::PAWN &&
            potentialPawnSqr->get_piece()->_color == _turn) {
            // look for possible block by pawn stepping one squares forward
            for (auto move : squares_to_moves({blockingSquare}, potentialPawnSqr->get_piece()))
                legalMoves.push_back(move);
        } else if (blockingSquare->get_row() == (attacker->_color == Color::WHITE ? 4 : 3)) {
            // look for possible block by pawn stepping two squares forward

            potentialPawnSqr = get_square(blockingSquare->get_col(), blockingSquare->get_row() + (attacker->_color == Color::WHITE ? 2 : -2));
            if (potentialPawnSqr->get_piece() != nullptr && potentialPawnSqr->get_piece()->_kind == PieceType::PAWN &&
                potentialPawnSqr->get_piece()->_color == _turn && get_square(blockingSquare->get_col(), blockingSquare->get_row() + (attacker->_color == Color::WHITE ? 1 : -1))->is_free()) {

                legalMoves.push_back(new Move(potentialPawnSqr->get_piece(), blockingSquare)); // cannot be promotion
            }
        }    
        // NOTE: en passant capture can never block a check   
    }

    return legalMoves;
}


std::vector<Move *> Board::calc_all_legal_moves_check(){

    std::vector<Move *> legalMoves = calc_legal_moves_check_move_king();
    
    King *king = get_king(_turn);
    ASSERT(king != nullptr, "king is in check but no king found");

    auto attackers = king->_square->get_attacked_by(invert_color(_turn));

    if (attackers.size() == 1) {
        auto pinnedPieces = calc_pinned_pieces(_turn);

        auto attacker = attackers[0];
        auto moves = calc_legal_moves_check_captures(attacker, pinnedPieces);
        legalMoves.insert(legalMoves.end(), moves.begin(), moves.end());

        if (attacker->_isSliding) {
            auto moves = calc_legal_moves_check_blocks(attacker, pinnedPieces);
            legalMoves.insert(legalMoves.end(), moves.begin(), moves.end());
        }
    }

    return legalMoves;
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

void Board::perform_move(Move *move, bool treeSearch) {
    _history.push_back(move);

    auto fromSqr = move->get_from_sqr();
    auto toSqr = move->get_to_sqr();
    auto movingPiece = move->get_piece();


    if (_turn == Color::BLACK)
        _fullMoves++;

    // if capturing a piece, store the reference in the move and remove it ...
    if (toSqr->get_piece() != nullptr) {
        move->set_piece_taken(toSqr->get_piece());
        remove_piece(toSqr->get_piece());
    }

    //... and the same for en passant capture
    if (move->is_en_passant()) {
        auto enPassantPawn = get_en_passant_pawn_square()->get_piece();
        move->set_piece_taken(enPassantPawn);
        remove_piece(enPassantPawn);
        // move->get_piece_taken()->_square = nullptr;
    }

    if (move->get_piece_taken() != nullptr || movingPiece->_kind == PieceType::PAWN)
        _halfMoves.push_back(0);
    else {
        ASSERT(_halfMoves.size() > 0, "half moves history is empty");
        _halfMoves.push_back(_halfMoves.back() + 1);
    }

    toSqr->_piece = movingPiece;
    fromSqr->_piece = nullptr;
    movingPiece->_square = toSqr;
    ++movingPiece->_movesCnt;

    if (move->is_castling()) {
        auto [rookFrom, rookTo] = get_castle_rook_squares(move);
        auto rook = get_square(rookFrom)->get_piece();
        ASSERT(rook != nullptr, "rook not found");

        get_square(rookTo)->_piece = rook;
        get_square(rookFrom)->_piece = nullptr;
        rook->_square = get_square(rookTo);
    }

    update_en_passant_history(move);

    if(move->is_promotion()) {
        ASSERT(move->get_new_piece() != std::nullopt, "promotion piece not set");
        promote_pawn(movingPiece, move->get_new_piece().value());
    }

    _turn = invert_color(_turn);

    if (!treeSearch)
        recalculation(move);
    //_legalMoves.push_back(calc_all_legal_moves());
}

void Board::store_piece_in_vectors(Piece *piece) {
    if (piece->_color == Color::WHITE) {
        if (piece->_kind == PieceType::KING)
            _whitePieces.insert(_whitePieces.begin(), piece);
        else
            _whitePieces.push_back(piece);

        if (piece->_isSliding)
            _whiteSlidingPieces.push_back(piece);
    } else {
        if (piece->_kind == PieceType::KING)
            _blackPieces.insert(_blackPieces.begin(), piece);
        else
            _blackPieces.push_back(piece);

        if (piece->_isSliding)
            _blackSlidingPieces.push_back(piece);
    }

}

void Board::undo_move(bool treeSearch) {
    ASSERT(_history.size() > 0, "no moves to undo");

    auto move = _history.back();
    _history.pop_back();

    auto fromSqr = move->get_from_sqr();
    auto toSqr = move->get_to_sqr();
    auto movingPiece = move->get_piece();

    if (move->is_promotion()) {
        ASSERT(move->get_piece()->_kind == PieceType::PAWN, "promotion piece is not a pawn");
        ASSERT(move->get_to_sqr()->get_row() == (move->get_piece()->_color == Color::WHITE ? 7 : 0), "promotion piece is not on the last rank");
        ASSERT(move->get_to_sqr()->get_piece() != nullptr, "promotion piece is not on the board");
        ASSERT(move->get_to_sqr()->get_piece()->_kind != PieceType::PAWN && move->get_to_sqr()->get_piece()->_kind != PieceType::KING,
            "promotion piece is invalid");

        auto newPiece = move->get_to_sqr()->get_piece();
        remove_piece(newPiece);
            
        delete newPiece;
        move->get_piece()->_isActive = true;
        store_piece_in_vectors(move->get_piece());
    }

    if (move->get_piece_taken() != nullptr) {
        if (move->is_en_passant())  {
            // restore the piece taken en passant
            // it's column is the same as the takers destination square, it's row as the taker's starting square
            get_square(toSqr->get_col(), fromSqr->get_row())->_piece  = move->get_piece_taken();
            toSqr->_piece = nullptr;
            movingPiece->_square = fromSqr;
            fromSqr->_piece = movingPiece;
        } else
            toSqr->_piece = move->get_piece_taken();
        
        move->get_piece_taken()->_isActive = true;
        store_piece_in_vectors(move->get_piece_taken());
    } else
        toSqr->_piece = nullptr;

    fromSqr->_piece = movingPiece;
    movingPiece->_square = fromSqr;
    --movingPiece->_movesCnt;

    if (move->is_castling()) {
        auto [rookFrom, rookTo] = get_castle_rook_squares(move);
        get_square(rookFrom)->_piece = get_square(rookTo)->_piece;
        get_square(rookTo)->_piece = nullptr;
        get_square(rookFrom)->_piece->_square = get_square(rookFrom);
    }

    if (movingPiece->_color == Color::BLACK)
        _fullMoves--;

    _halfMoves.pop_back();
    _enPassantPawnSquareHistory.pop_back();

    if (!treeSearch)
        recalculation(move, true);
    _turn = invert_color(_turn);
    //_legalMoves.pop_back();
    delete move;
}

void Board::recalculation() {
    for (auto piece : _whitePieces)
        piece->recalculate();
    for (auto piece : _blackPieces)
        piece->recalculate();
}

void Board::recalculation(Move *move, bool undo) {
    // recalculates which squares are attacked by which pieces after a move
    // not all pieces must be recalculated, only those that are affected by the move
    //     1. the moving piece, in case of promotion the new piece
    //     2. the piece being taken
    //     3. the pieces that were previously blocked by the moving piece
    //     4. the pieces that are now blocked by the moving piece
    //     5. if the move is castling, the rook and the pieces now blocked by the rook (before the rook couldn't block anyone, it was in the corner)
    //     6. if the move is en passant, the pieces previously blocked by the captured pawn

    auto piecesToRecalculate = std::set<Piece *>();

    if (!move->is_promotion() || undo)
        piecesToRecalculate.insert(move->get_piece());
    else
        piecesToRecalculate.insert(move->get_to_sqr()->get_piece());

    for (auto piece : move->get_from_sqr()->get_attacked_by(Color::WHITE))
        piecesToRecalculate.insert(piece);
    for (auto piece : move->get_from_sqr()->get_attacked_by(Color::BLACK))
        piecesToRecalculate.insert(piece);
    for (auto piece : move->get_to_sqr()->get_attacked_by(Color::WHITE))
        piecesToRecalculate.insert(piece);
    for (auto piece : move->get_to_sqr()->get_attacked_by(Color::BLACK))
        piecesToRecalculate.insert(piece);

    if (move->get_piece_taken() != nullptr && move->get_piece_taken()->_isActive)
        piecesToRecalculate.insert(move->get_piece_taken());

    if (move->is_castling()){
        auto [rookFrom, rookTo] = get_castle_rook_squares(move);
        auto rookFromSqr = get_square(rookFrom);
        auto rookToSqr = get_square(rookTo);

        if (!undo)
            piecesToRecalculate.insert(rookToSqr->get_piece());
        else 
            piecesToRecalculate.insert(rookFromSqr->get_piece());

        for (auto piece : rookFromSqr->get_attacked_by(Color::WHITE))
            piecesToRecalculate.insert(piece);
        for (auto piece : rookFromSqr->get_attacked_by(Color::BLACK))
            piecesToRecalculate.insert(piece);
        for (auto piece : rookToSqr->get_attacked_by(Color::WHITE))
            piecesToRecalculate.insert(piece);
        for (auto piece : rookToSqr->get_attacked_by(Color::BLACK))
            piecesToRecalculate.insert(piece);
    }

    if (move->is_en_passant()) {
        ASSERT(move->get_piece_taken() != nullptr, "en passant capture without piece taken");
        for (auto piece : move->get_piece_taken()->_square->get_attacked_by(Color::WHITE))
            piecesToRecalculate.insert(piece);
        for (auto piece : move->get_piece_taken()->_square->get_attacked_by(Color::BLACK))
            piecesToRecalculate.insert(piece);
    }

    for (auto piece : piecesToRecalculate)
        piece->recalculate();

}

void Board::promote_pawn(Piece *pawn, PieceType newKind) {
    remove_piece(pawn);
    place_piece(newKind, pawn->_color, pawn->_square);
}


void Board::remove_piece(Piece *piece) {

    for (auto sqr : piece->_attackedSquares) {
        if (piece->_color == Color::WHITE)
            sqr->_attackedByWhites.erase(std::remove(sqr->_attackedByWhites.begin(), sqr->_attackedByWhites.end(), piece), sqr->_attackedByWhites.end());
        else
            sqr->_attackedByBlacks.erase(std::remove(sqr->_attackedByBlacks.begin(), sqr->_attackedByBlacks.end(), piece), sqr->_attackedByBlacks.end());
    }

    piece->_attackedSquares.clear();

    // used when piece is captured, also removes pawn that is being promoted
    piece->_square->_piece = nullptr;
    //piece->_square = nullptr;
    piece->_isActive = false;

    if (piece->_color == Color::WHITE){
        _whitePieces.erase(std::remove(_whitePieces.begin(), _whitePieces.end(), piece), _whitePieces.end());
        if (piece->_isSliding)
            _whiteSlidingPieces.erase(std::remove(_whiteSlidingPieces.begin(), _whiteSlidingPieces.end(), piece), _whiteSlidingPieces.end());
    } else {
        _blackPieces.erase(std::remove(_blackPieces.begin(), _blackPieces.end(), piece), _blackPieces.end());    
        if (piece->_isSliding)
            _blackSlidingPieces.erase(std::remove(_blackSlidingPieces.begin(), _blackSlidingPieces.end(), piece), _blackSlidingPieces.end());
    }
}

void Board::update_en_passant_history(Move *move) {
    // if the current move is a 2 square pawn move, remember that it can be taken e.p.
    if (move->get_piece()->_kind == PieceType::PAWN && abs(move->get_from_sqr()->get_row() - move->get_to_sqr()->get_row()) == 2)
        _enPassantPawnSquareHistory.push_back(move->get_to_sqr());
    else
        _enPassantPawnSquareHistory.push_back(nullptr);
}

std::tuple<int, int> Board::get_castle_rook_squares(Move *move) {
    // get the from and to squares of the rook that is castling
    auto toSqrIdx = move->get_to_sqr()->get_idx();
    ASSERT(toSqrIdx == 6 || toSqrIdx == 2 || toSqrIdx == 62 || toSqrIdx == 58, "invalid castling move");

    if (toSqrIdx == 6)
        return {7, 5};
    else if (toSqrIdx == 2)
        return {0, 3};
    else if (toSqrIdx == 62)
        return {63, 61};
    else
        return {56, 59};
}

int Board::generate_successors(int depth) {
    int total = 0;

    if (_history.size() > 0 && _history.back() != nullptr)
        recalculation(_history.back());
    else
        recalculation();

    _legalMoves.push_back(calc_all_legal_moves());
    for (auto move : _legalMoves.back()) {
        // if (depth == 2) 
        //     std::cout << "move " << *move;
        perform_move(move);

        // std::cout << std::string(10-depth*2, ' ') << *move << std::endl;

        int n;
        if (depth > 1)
            n = generate_successors(depth - 1);
        else
            n = 1;

        total += n;

        // if (depth == 2) 
            // std::cout << ": " << n << std::endl;
        undo_move();
    }

    // for (auto move : _legalMoves.back())
        // delete move;
    _legalMoves.pop_back();

    return total;
}