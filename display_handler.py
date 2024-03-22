from __future__ import annotations

import random
from typing import TYPE_CHECKING, List, Optional, Iterable

from constants import *
import icons
import PySimpleGUI as sg

if TYPE_CHECKING:
    from piece import Piece
    from square import Square

class DisplayHandler:
    def __init__(self, display: List[List[sg.Button]]):
        self.display = display
        self.lightedSquares: List[Square] = []
    
    def clear(self) -> None:
        for i in range(8):
            for j in range(8):
                if self.display[i][j].ImageData != icons.empty:
                    self.display[i][j].Update(image_data=icons.empty)
                    self.display[i][j].ImageData=icons.empty

    def load(self, squares: List[Square]) -> None:
        for sqr in squares:
            icon = self._get_icon(sqr.piece)
            if icon != self.display[7-sqr.rowIdx][sqr.colIdx].ImageData:
                self.display[7-sqr.rowIdx][sqr.colIdx].Update(image_data=icon)
                self.display[7-sqr.rowIdx][sqr.colIdx].ImageData = icon

    def draw_square(self, sqr: Square, piece: Optional[Piece]):
        icon = self._get_icon(piece)
        self.display[7-sqr.rowIdx][sqr.colIdx].Update(image_data=icon)
        self.display[7-sqr.rowIdx][sqr.colIdx].ImageData = icon
    
    def light_squares(self, squares: Iterable[Square], intensity: int=1) -> None:
        for sqr in squares:
            self.lightedSquares.append(sqr)
            color = self._get_color(sqr, intensity)
            self.display[7-sqr.rowIdx][sqr.colIdx].Update(button_color=color)
            
    def unlight_squares(self) -> None:
        for sqr in self.lightedSquares:
            color = self._get_color(sqr, 0)
            self.display[7-sqr.rowIdx][sqr.colIdx].Update(button_color=color)
        self.lightedSquares = []
    
    @staticmethod
    def _get_icon(piece: Optional[Piece]) -> bytes:
        if piece is None:
            return icons.empty
        elif piece.color == Color.WHITE:
            if piece.kind == PieceType.PAWN:
                return icons.whitePawn
            elif piece.kind == PieceType.KNIGHT:
                return icons.whiteKnight
            elif piece.kind == PieceType.BISHOP:
                return icons.whiteBishop
            elif piece.kind == PieceType.ROOK:
                return icons.whiteRook
            elif piece.kind == PieceType.QUEEN:
                return icons.whiteQueen
            elif piece.kind == PieceType.KING:
                return icons.whiteKing
        else:
            if piece.kind == PieceType.PAWN:
                return icons.blackPawn
            elif piece.kind == PieceType.KNIGHT:
                return icons.blackKnight
            elif piece.kind == PieceType.BISHOP:
                return icons.blackBishop
            elif piece.kind == PieceType.ROOK:
                return icons.blackRook
            elif piece.kind == PieceType.QUEEN:
                return icons.blackQueen
            elif piece.kind == PieceType.KING:
                return icons.blackKing
        raise ValueError(f'invalid piece kind {piece.kind} or color {piece.color}')

    @staticmethod
    def _get_color(sqr: Square, intensity: int) -> str:
        if (sqr.rowIdx + sqr.colIdx) % 2 == 0:
            #dark square
            if intensity == 0:
                return COLOR_BG_DARK_BASIC
            elif intensity == 1:
                return COLOR_BG_DARK_HLIGHTED_1
            elif intensity == 2:
                return COLOR_BG_DARK_HLIGHTED_2
        else:
            #light square
            if intensity == 0:
                return COLOR_BG_LIGHT_BASIC
            elif intensity == 1:
                return COLOR_BG_LIGHT_HLIGHTED_1
            elif intensity == 2:
                return COLOR_BG_LIGHT_HLIGHTED_2
        raise ValueError(f'invalid intensity value {intensity}')

    @staticmethod
    def get_playing_as_from_dialog() -> Color:
        playing_as_window = sg.Window('What color do you want to play as?', [[sg.Button('White'), sg.Button('Black'), sg.Button('Random')]])
        color, _ = playing_as_window.read()
        playing_as_window.close()
        if color == 'White':
            return Color.WHITE
        elif color == 'Black':
            return Color.BLACK
        else:
            return Color.WHITE if random.randint(0, 1) == 0 else Color.BLACK

    @staticmethod
    def get_promoted_piece_from_dialog() -> PieceType:
        promote_window = sg.Window('what piece do you want', [[sg.Button('Queen'), sg.Button('Rook'), sg.Button('Bishop'), sg.Button('Knight')]])
        piece, _  = promote_window.read()
        promote_window.close()
        if piece == 'Queen':
            return PieceType.QUEEN
        elif piece == 'Rook':
            return PieceType.ROOK
        elif piece == 'Bishop':
            return PieceType.BISHOP
        else:
            return PieceType.KNIGHT
        
    @staticmethod
    def inform(msg: str) -> None:
        sg.popup(msg)
