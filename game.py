from __future__ import annotations
from typing import TYPE_CHECKING
from board import Board
from constants import FEN_INIT, Color, Result, PieceType

if TYPE_CHECKING:
    from display_handler import DisplayHandler
    from square import Square
    from piece import Piece
    from move import Move


class Game:
    def __init__(self, display: DisplayHandler):
        self.displayHandler = display
        self.board = Board()
        
    def place_piece(self, sqrIdx: int, kind: PieceType, color: Color) -> None:
        sqr = self.board.get_square_by_idx(sqrIdx)
        self.board.place_piece(sqr, kind, color)
        self.displayHandler.draw_square(sqr, sqr.piece)
        
    def remove_piece(self, piece: Piece, display: bool=False) -> None:
        self.board.remove_piece(piece)
        if display:
            self.displayHandler.draw_square(piece.square, None)
        
    def reset(self) -> None:
        self.displayHandler.unlight_squares()
        self.board.load_FEN(FEN_INIT)
        self.displayHandler.load(self.board)
        
    def clear(self) -> None:
        self.displayHandler.unlight_squares()
        self.board.clear()
        self.displayHandler.load(self.board)

    def check_game_end(self) -> None:
        if len(self.board.get_current_legal_moves()) == 0:
            if self.board.is_in_check(self.board.turn):
                if self.board.turn == Color.WHITE:
                    self.displayHandler.inform(Result.BLACK_WON.value)
                else:
                    self.displayHandler.inform(Result.WHITE_WON.value)
            else:
                self.displayHandler.inform(Result.DRAW_STALEMATE.value)

            return
        
        pieces = list(self.board.get_all_pieces())
        if len(pieces) == 2 or (len(pieces) == 3 and any(map(lambda p: p.isLight, pieces))):
            self.displayHandler.inform(Result.DRAW_INSUFFICIENT_MATERIAL.value)
            
        if self.board.halfMoves == 100:
            self.displayHandler.inform(Result.DRAW_50_MOVES.value)

    def undo_move(self) -> None:
        if len(self.board.history) == 0:
            return
        move = self.board.history.pop()

        self.board.undo_move(move)
        self.displayHandler.load(self.board)

    def perform_move(self, move: Move) -> None:
        if move.is_promotion():
            move.newPiece = self.displayHandler.get_promoted_piece_from_dialog()

        self.board.perform_move(move)
        self.displayHandler.load(self.board)
        self.check_game_end()

