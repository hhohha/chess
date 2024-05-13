from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, Optional, Iterable
import re

from constants import FEN_INIT, Color, PieceType, FEN_B
from engine_protocol import EngineProtocol
from square import Square
from utils import letterToPiece
from piece import Piece
from move import Move

if TYPE_CHECKING:
    from display_handler import DisplayHandler

class CastlingRights:
    def __init__(self):
        self.whiteLeft = True
        self.whiteRight = True
        self.blackLeft = True
        self.blackRight = True

    def __str__(self) -> str:
        retStr = "K" if self.whiteRight else "" + "Q" if self.whiteLeft else "" + "k" if self.blackRight else "" +"q"\
            if self.blackLeft else ""
        return retStr if retStr != "" else "-"

    def get_updated(self, move: Move) -> CastlingRights:
        newRights = CastlingRights()
        newRights.whiteLeft = self.whiteLeft and (move.fromSqr.idx != 0 and move.fromSqr.idx != 4)
        newRights.whiteRight = self.whiteRight and (move.fromSqr.idx != 7 and move.fromSqr.idx != 4)
        newRights.blackLeft = self.blackLeft and (move.fromSqr.idx != 56 and move.fromSqr.idx != 60)
        newRights.blackRight = self.blackRight and (move.fromSqr.idx != 63 and move.fromSqr.idx != 60)
        return newRights


class Game:
    def __init__(self, display: DisplayHandler, engine: EngineProtocol):
        self.displayHandler = display
        self.engine = engine
        self.squares: List[Square] = [Square(i) for i in range(64)]
        self.history: List[Move] = []
        self.halfMoves = [0]
        self.castlingRights: List[CastlingRights] = [CastlingRights()]
        self.enPassantSquares: List[Optional[Square]] = [None]
        self.legalMoves: List[Move] = []

        self.moves = 0

        self.turn: Color = Color.WHITE
        
    def place_piece(self, sqrIdx: int, kind: PieceType, color: Color) -> None:
        sqr = self.squares[sqrIdx]
        sqr.piece = Piece(kind, color)
        self.displayHandler.draw_square(sqr, sqr.piece)
        
    def clear_square(self, sqrIdx: int) -> None:
        sqr = self.squares[sqrIdx]
        piece = sqr.piece
        self.displayHandler.draw_square(sqr, None)
        
    def reset(self) -> None:
        self.displayHandler.unlight_squares()
        self.load_fen(FEN_INIT)
        self.displayHandler.load(self.squares)
        
    def clear(self) -> None:
        self.displayHandler.unlight_squares()
        for sqr in self.squares:
            sqr.piece = None
        self.displayHandler.load(self.squares)

    def make_engine_move(self) -> None:
        strMove = self.engine.get_best_move()
        move = self.create_move_from_str(strMove)
        self.perform_move(move)

    def load_moves_from_str(self, moves: str) -> None:
        if moves == '':
            self.legalMoves = []
        else:
            self.legalMoves = list(map(lambda mv: self.create_move_from_str(mv), moves.strip().split(' ')))

    def load_fen(self, fen: str) -> None:
        """load a position from a FEN string"""
        logging.info(f'Loading FEN: {fen}')

        self.clear()
        if not re.match(r'^([rnbqkpRNBQKP1-8]*/){7}[rnbqkpRNBQKP1-8]* [wb] (-|[KQkq]{1,4}) (-|[a-h][36]) [0-9]+ [0-9]+$', fen):
            # doesn't catch all invalid FENs, but it's a good sanity check
            raise ValueError('Invalid FEN position given')

        pieces, turn, castling, enPassantSqr, halves, fulls = fen.split()

        col, row = 0, 7  # for some reason, FEN starts with a8
        for c in pieces:
            if c.isdigit():  # number of empty squares to skip
                col += int(c)
                continue

            if c == '/':  # new row
                assert col == 8, 'Invalid FEN position given'
                col, row = 0, row - 1
                continue

            # place a new piece
            piece: PieceType = letterToPiece[c.lower()]
            color: Color = Color.WHITE if c.isupper() else Color.BLACK
            self.place_piece(col + 8 * row, piece, color)

            col += 1

        self.turn = Color.WHITE if turn == 'w' else Color.BLACK

        castlingRights = CastlingRights()
        if 'K' not in castling: castlingRights.whiteRight = False
        if 'Q' not in castling: castlingRights.whiteLeft = False
        if 'k' not in castling: castlingRights.blackRight = False
        if 'q' not in castling: castlingRights.blackLeft = False
        self.castlingRights = [castlingRights]

        if enPassantSqr != '-':
            self.enPassantSquares = [self.get_square(enPassantSqr)]
        else:
            self.enPassantSquares = [None]

        self.halfMoves = [int(halves)]
        self.moves = int(fulls)

        movesFromEngine = self.engine.load_fen(fen)
        self.load_moves_from_str(movesFromEngine)

        self.displayHandler.load(self.squares)

    def get_square(self, coord: str) -> Square:
        """get a square by its coordinate"""
        col, row = ord(coord[0]) - ord('a'), int(coord[1]) - 1
        return self.squares[col + 8 * row]

    def get_possible_target_squares(self, fromSqr: Square) -> Iterable[Square]:
        legalMoves: Iterable[Move] = filter(lambda move: move.fromSqr == fromSqr, self.legalMoves)
        return map(lambda move: move.toSqr, legalMoves)


    # def check_game_end(self) -> None:
    #     if len(self.board.get_current_legal_moves()) == 0:
    #         if self.board.is_in_check(self.board.turn):
    #             if self.board.turn == Color.WHITE:
    #                 self.displayHandler.inform(Result.BLACK_WON.value)
    #             else:
    #                 self.displayHandler.inform(Result.WHITE_WON.value)
    #         else:
    #             self.displayHandler.inform(Result.DRAW_STALEMATE.value)
    #
    #         return
    #
    #     pieces = list(self.board.get_all_pieces())
    #     if len(pieces) == 2 or (len(pieces) == 3 and any(map(lambda p: p.isLight, pieces))):
    #         self.displayHandler.inform(Result.DRAW_INSUFFICIENT_MATERIAL.value)
    #
    #     if self.board.halfMoves == 100:
    #         self.displayHandler.inform(Result.DRAW_50_MOVES.value)

    def undo_move(self) -> None:
        if len(self.history) == 0:
            return
        move = self.history.pop()
        self.halfMoves.pop()
        self.castlingRights.pop()
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK
        self.moves -= 1

        if move.isPromotion:
            move.piece.kind = PieceType.PAWN
        self.squares[move.toSqr.idx].piece = None
        self.squares[move.fromSqr.idx].piece = move.piece
        if move.isCastling:
            rookSquareFrom = self.squares[move.toSqr.idx + 1] if move.toSqr.idx > move.fromSqr.idx else self.squares[move.toSqr.idx - 2]
            rookSquareTo = self.squares[move.toSqr.idx - 1] if move.toSqr.idx > move.fromSqr.idx else self.squares[move.toSqr.idx + 1]
            rookSquareFrom.piece = rookSquareTo.piece
            rookSquareTo.piece = None

        if move.isEnPassant:
            sqrCol = move.toSqr.colIdx
            sqrRow = move.fromSqr.rowIdx
            capturedPieceSqr = self.squares[sqrRow * 8 + sqrCol]
            capturedPieceSqr.piece = move.capturedPiece

        self.displayHandler.load(self.squares)
        movesFromEngine = self.engine.undo_move()
        self.legalMoves = list(map(lambda mv: self.create_move_from_str(mv), movesFromEngine.strip().split(' ')))

    def create_move_from_str(self, moveStr: str) -> Move:
        assert len(moveStr) == 6 or (len(moveStr) == 7 and moveStr[6] in 'NBQR'), f"invalid move string: {moveStr}"
        assert moveStr[1] in 'abcdefgh' and moveStr[4] in 'abcdefgh', f"invalid move string: {moveStr}"
        assert moveStr[2] in '12345678' and moveStr[5] in '12345678', f"invalid move string: {moveStr}"

        fromSqrIdx = (int(moveStr[2]) - 1) * 8 + ord(moveStr[1]) - ord('a')
        toSqrIdx = (int(moveStr[5]) - 1) * 8 + ord(moveStr[4]) - ord('a')

        move = Move(self.squares[fromSqrIdx], self.squares[toSqrIdx])
        if len(moveStr) == 5:
            move.newPiece = letterToPiece[moveStr[4]]
        return move

    def create_move(self, fromSqrIdx: int, toSqrIdx: int) -> Move:
        move = Move(self.squares[fromSqrIdx], self.squares[toSqrIdx])
        if move.isPromotion:
            move.newPiece = self.displayHandler.get_promoted_piece_from_dialog()
        return move

    def perform_move(self, move: Move) -> None:
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK
        self.moves += 1

        self.history.append(move)
        if move.piece.kind == PieceType.PAWN or move.capturedPiece is not None:
            self.halfMoves.append(0)
        else:
            self.halfMoves[-1] += 1

        self.castlingRights.append(self.castlingRights[-1].get_updated(move))

        self.squares[move.fromSqr.idx].piece = None
        self.squares[move.toSqr.idx].piece = move.piece
        if move.isCastling:
            rookSquareFrom = self.squares[move.toSqr.idx + 1] if move.toSqr.idx > move.fromSqr.idx else self.squares[move.toSqr.idx - 2]
            rookSquareTo = self.squares[move.toSqr.idx - 1] if move.toSqr.idx > move.fromSqr.idx else self.squares[move.toSqr.idx + 1]
            rookSquareTo.piece = rookSquareFrom.piece
            rookSquareFrom.piece = None

        if move.isEnPassant:
            sqrCol = move.toSqr.colIdx
            sqrRow = move.fromSqr.rowIdx
            capturedPieceSqr = self.squares[sqrRow * 8 + sqrCol]
            capturedPieceSqr.piece = None

        moveStr = str(move)
        if move.isPromotion:
            assert move.newPiece is not None, f"Invalid move: promotion move {move}"
            move.piece.kind = move.newPiece

        self.displayHandler.load(self.squares)

        movesFromEngine = self.engine.perform_move(moveStr)
        self.load_moves_from_str(movesFromEngine)

        # self.check_game_end()

