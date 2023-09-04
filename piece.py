from typing import List, Optional
from square import Square
from utils import *
from abc import ABC, abstractmethod
from move import Move

# TODO - refactor

class Piece(ABC):
    def __init__(self, kind: PieceType, color: Color, square: Square):
        self.kind = kind
        self.color = color
        self.movesCnt = 0
        self.square = square
        # self.attacked_squares = [[]]
        # self.id = square.idx
        # self.is_active = True

    @abstractmethod
    def calc_potential_moves(self):
        pass

    @abstractmethod
    def calc_potential_moves_pinned(self, direction: Direction):
        pass

    def isSliding(self) -> bool:
        return False

    #def get_attacked_squares(self):
    #    return self.attacked_squares[-1]

    #@abstractmethod
    #def add_new_calculation(self):
    #    self.attacked_squares.append([])

    #@abstractmethod
    #def remove_last_calculation(self):
    #    self.attacked_squares.pop()

    #@abstractmethod
    #def update_attacked_squares(self):
    #    pass

    #def calc_attacked_squares(self):
    #   return list(map(lambda mv: mv.toSqr, self.calc_potential_moves(ownPieces=True)))

    def get_legal_moves(self):
        if self.square.board.turn != self.color:
            return []
        return list(filter(lambda move: move.fromSqr == self.square, self.square.board.legal_moves[-1]))

    #def __eq__(self, other):
    #    return self.id == other.id
    
    def __hash__(self):
        return id(self)

class SlidingPiece(Piece, ABC):
    def isSliding(self) -> bool:
        return True

    @abstractmethod
    def get_sliding_directions(self) -> List[Direction]:
        pass

    def calc_potential_moves(self, ownPieces: bool=False) -> List[Move]:
        """
        potential moves are all possible moves without considering checks and pins,
        e.i. potential moves can be impossible if the king is in check or the piece is pinned
        with ownPieces=True, the potential moves are all possible moves including captures of own pieces - to see if a piece is covered

        :param ownPieces: should include own pieces in the potential moves
        :return: list of potential moves
        """
        potentialMoves: List[Move] = []
        for direction in self.get_sliding_directions():
            i, j = 0, 0
            while True:
                i, j = move_in_direction(i, j, direction)
                square: Optional[Square] = self.square.board.get_square_by_coords(self.square.rowIdx + i, self.square.colIdx + j)

                if square is None:
                    break  # reached the edge of the board

                if square.piece is None:
                    potentialMoves.append(Move(self, square))  # free square
                elif square.piece.color != self.color:
                    potentialMoves.append(Move(self, square))  # capture - can move here but no further
                    break
                else:
                    if ownPieces:  # if own pieces are included, can move here but no further
                        potentialMoves.append(Move(self, square))
                    break
        return potentialMoves

    def calc_potential_moves_pinned(self, directionFrom: Direction) -> List[Move]:
        """
        what are potential moves if the piece is pinned in the given direction

        :param directionFrom: direction from pinner to king
        :return: list of potential moves
        """
        if directionFrom not in self.get_sliding_directions():
            return [] # a piece is pinned in a direction in which it cannot move

        potentialMoves: List[Move] = []

        while True:
            # a piece can move in the direction of the pinner including its capture
            colIdx, rowIdx = move_in_direction(self.square.colIdx, self.square.rowIdx, directionFrom)
            sqr = self.square.board.get_square_by_coords(rowIdx, colIdx)
            assert sqr is not None, f"piece {self} is actually not pinned"

            potentialMoves.append(Move(self, sqr))
            if not sqr.is_free():
                break

        while True:
            # can move towards the king but cannot capture
            colIdx, rowIdx = move_in_direction(self.square.colIdx, self.square.rowIdx, reverse_dir(directionFrom))
            sqr = self.square.board.get_square_by_coords(rowIdx, colIdx)
            assert sqr is not None, f"piece {self} is actually not pinned"

            if not sqr.is_free():
                break
            potentialMoves.append(Move(self, sqr))

        return potentialMoves

# class PieceWithPotenialSquares(Piece):
#     def __init__(self, kind: PieceType, color: Color, square: Square):
#         super().__init__(kind, color, square)
#         self.potential_squares = [[]]
#         self.has_PT = True
#
#     def get_potential_squares(self):
#         return self.potential_squares[-1]
#
#     def add_new_calculation(self):
#         for sqr in self.get_attacked_squares():
#             sqr.get_attacked_by(self.color).remove(self)
#         self.attacked_squares.append([])
#         self.potential_squares.append([])
#
#     def remove_last_calculation(self):
#         for sqr in self.get_attacked_squares():
#            sqr.get_attacked_by(self.color).remove(self)
#         self.attacked_squares.pop()
#         for sqr in self.get_attacked_squares():
#             if self not in sqr.get_attacked_by(self.color):
#                 sqr.get_attacked_by(self.color).append(self)
#         self.potential_squares.pop()
#
#     def update_attacked_squares(self):
#         self.get_potential_squares().clear()
#         if not self.is_active:
#             for sqr in self.get_attacked_squares():
#                 sqr.get_attacked_by(self.color).remove(self)
#             self.get_attacked_squares().clear()
#             return
#
#         self.get_attacked_squares().clear()
#
#         for sqr in self.calc_attacked_squares():
#             self.get_attacked_squares().append(sqr)
#             if sqr.piece is None or sqr.piece.color != self.color:
#                 self.get_potential_squares().append(sqr)
#
#             sqr.get_attacked_by(self.color).append(self)
#
#
# class cPieceWithoutPS(Piece):
#     def __init__(self, kind, color, square):
#         super().__init__(kind, color, square)
#         self.has_PT = False
#
#     def add_new_calculation(self):
#         for sqr in self.get_attacked_squares():
#             sqr.get_attacked_by(self.color).remove(self)
#         self.attacked_squares.append([])
#
#     def remove_last_calculation(self):
#         for sqr in self.get_attacked_squares():
#            sqr.get_attacked_by(self.color).remove(self)
#         self.attacked_squares.pop()
#         for sqr in self.get_attacked_squares():
#             if self not in sqr.get_attacked_by(self.color):
#                 sqr.get_attacked_by(self.color).append(self)
#
#     def update_attacked_squares(self):
#         if not self.is_active:
#             for sqr in self.get_attacked_squares():
#                 sqr.get_attacked_by(self.color).remove(self)
#             self.get_attacked_squares().clear()
#             return
#
#         for sqr in self.calc_attacked_squares():
#             self.get_attacked_squares().append(sqr)
#             sqr.get_attacked_by(self.color).append(self)
