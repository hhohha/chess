from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Iterable
from constants import FEN_INIT, Color, PieceType
from engine_protocol import EngineProtocol

if TYPE_CHECKING:
    from display_handler import DisplayHandler
    from square import Square
    from piece import Piece
    from move import Move

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

    def load_fen(self, fen: str) -> None:
        pass

    def generate_fen(self) -> str:
        fenLst: List[str] = []

        for row in range(8):
            emptySquares = 0

            for col in range(8):
                sqr = self.squares[row * 8 + col]
                if sqr.piece is not None:
                    emptySquares += 1
                else:
                    if emptySquares > 0:
                        fenLst.append(str(emptySquares))
                        emptySquares = 0
                    fenLst.append(str(sqr.piece))
            if emptySquares > 0:
                fenLst.append(str(emptySquares))

            if row < 7:
                fenLst.append('/')

        fenLst.append(' ')
        fenLst.append('w' if self.turn == Color.WHITE else 'b')
        fenLst.append(' ')

    def get_possible_target_squares(self, fromSqr: Square) -> Iterable[Square]:
        legalMoves = filter(lambda move: move.fromSqr == fromSqr, self.legalMoves)
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

        if move.isPromotion():
            move.piece.kind = PieceType.PAWN
        self.squares[move.toSqr.idx].piece = None
        self.squares[move.fromSqr.idx].piece = move.piece
        if move.isCastling():
            rookSquareFrom = self.squares[move.toSqr.idx + 1] if move.toSqr.idx > move.fromSqr.idx else self.squares[move.toSqr.idx - 2]
            rookSquareTo = self.squares[move.toSqr.idx - 1] if move.toSqr.idx > move.fromSqr.idx else self.squares[move.toSqr.idx + 1]
            rookSquareFrom.piece = rookSquareTo.piece
            rookSquareTo.piece = None

        if move.isEnPassant():
            sqrCol = move.toSqr.colIdx
            sqrRow = move.fromSqr.rowIdx
            capturedPieceSqr = self.squares[sqrRow * 8 + sqrCol]
            capturedPieceSqr.piece = move.capturedPiece

        self.displayHandler.load(self.squares)
        self.engine.undo_move()# TODO - remove 2nd call, undo move returns new possible moves
        self.legalMoves = self.engine.get_moves()

    def make_move(self, fromSqrIdx: int, toSqrIdx: int) -> Move:
        move = Move(self.squares[fromSqrIdx], self.squares[toSqrIdx])
        if move.isPromotion():
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
        if move.isCastling():
            rookSquareFrom = self.squares[move.toSqr.idx + 1] if move.toSqr.idx > move.fromSqr.idx else self.squares[move.toSqr.idx - 2]
            rookSquareTo = self.squares[move.toSqr.idx - 1] if move.toSqr.idx > move.fromSqr.idx else self.squares[move.toSqr.idx + 1]
            rookSquareTo.piece = rookSquareFrom.piece
            rookSquareFrom.piece = None

        if move.isEnPassant():
            sqrCol = move.toSqr.colIdx
            sqrRow = move.fromSqr.rowIdx
            capturedPieceSqr = self.squares[sqrRow * 8 + sqrCol]
            capturedPieceSqr.piece = None

        if move.isPromotion():
            move.piece.kind = move.newPiece

        self.displayHandler.load(self.squares)

        self.engine.perform_move(move) # TODO - remove 2nd call, perform move returns new possible moves
        self.legalMoves = self.engine.get_moves()

        # self.check_game_end()

