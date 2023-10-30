from __future__ import annotations
from typing import List, Set, TYPE_CHECKING
from constants import Color
from utils import *
from abc import ABC, abstractmethod
from move import Move

if TYPE_CHECKING:
    from square import Square

class Piece(ABC):
    def __init__(self, kind: PieceType, color: Color, square: Square):
        self.kind = kind
        self.color = color
        self.square = square
        self.isActive = True
        if not hasattr(self, 'movesCnt'):
            self.movesCnt = 0
        if not hasattr(self, 'attackedSquares'):
            self.attackedSquares: Set[Square] = set()
        if not hasattr(self, 'potentialMoves'):
            self.potentialMoves: List[Move] = []

    @abstractmethod
    def recalculate(self) -> None:
        pass

    @abstractmethod
    def calc_potential_moves_pinned(self, direction: Direction) -> List[Move]:
        pass

    def get_potential_moves(self) -> List[Move]:
        return self.potentialMoves

    def is_sliding(self) -> bool:
        return False

    def get_legal_moves(self) -> List[Move]:
        """
        Gets legal moves of the piece by filtering all current legal moves, not performance critical since it is used by UI only
        :return: list of legal moves of the piece
        """
        if self.square.board.turn != self.color:
            return []
        return list(filter(lambda move: move.fromSqr == self.square, self.square.board.legalMoves[-1]))
    
    def __hash__(self):
        return id(self)

class SlidingPiece(Piece, ABC):
    def is_sliding(self) -> bool:
        return True

    @abstractmethod
    def get_sliding_directions(self) -> List[Direction]:
        pass

    def recalculate(self) -> None:
        """
        updates potential moves and attacked squares
        potential moves are all possible moves without considering checks and pins,
        e.i. potential moves can be impossible if the king is in check or the piece is pinned
        with ownPieces=True, the potential moves are all possible moves including captures of own pieces - to see if a piece is covered
        for most pieces the difference between potential moves and attacked squares is that piece can attack squares with the piece of the same color
        """
        for sqr in self.attackedSquares:
            sqr.get_attacked_by(self.color).remove(self)

        self.potentialMoves.clear()
        self.attackedSquares.clear()

        for direction in self.get_sliding_directions():
            i, j = 0, 0
            while True:
                i, j = move_in_direction(i, j, direction)
                square: Optional[Square] = self.square.board.get_square_by_coords_opt(self.square.colIdx + i, self.square.rowIdx + j)

                if square is None:
                    break  # reached the edge of the board
                if square.piece is None:
                    self.attackedSquares.add(square)
                    self.potentialMoves.append(Move(self, square))
                elif square.piece.color != self.color:
                    self.attackedSquares.add(square)
                    self.potentialMoves.append(Move(self, square))
                    break
                else:
                    self.attackedSquares.add(square)
                    break

        for sqr in self.attackedSquares:
            sqr.get_attacked_by(self.color).add(self)

    def calc_potential_moves_pinned(self, directionFromKingToPinner: Direction) -> List[Move]:
        """
        what are potential moves if the piece is pinned in the given direction

        :param directionFromKingToPinner: direction from king to pinner!!!
        :return: list of potential moves
        """
        if directionFromKingToPinner not in self.get_sliding_directions():
            return [] # a piece is pinned in a direction in which it cannot move

        potentialMoves: List[Move] = []

        colIdx, rowIdx = self.square.colIdx, self.square.rowIdx
        while True:
            # can move towards the king but cannot capture
            colIdx, rowIdx = move_in_direction(colIdx, rowIdx, reverse_dir(directionFromKingToPinner))
            sqr = self.square.board.get_square_by_coords_opt(colIdx, rowIdx)
            assert sqr is not None, f"piece {self} is actually not pinned"

            if sqr.piece is not None:
                assert sqr.piece.color == self.color and sqr.piece.kind == PieceType.KING, f"piece {self} is actually not pinned"
                break
            potentialMoves.append(Move(self, sqr))

        colIdx, rowIdx = self.square.colIdx, self.square.rowIdx
        while True:
            # a piece can move in the direction of the pinner including its capture
            colIdx, rowIdx = move_in_direction(colIdx, rowIdx, directionFromKingToPinner)
            sqr = self.square.board.get_square_by_coords_opt(colIdx, rowIdx)
            assert sqr is not None, f"piece {self} is actually not pinned"

            potentialMoves.append(Move(self, sqr))
            if sqr.piece is not None:
                assert sqr.piece.color != self.color and sqr.piece.is_sliding(), f"piece {self} is actually not pinned"
                break

        return potentialMoves