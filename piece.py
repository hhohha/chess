from lib import *
from abc import ABC, abstractmethod

class cPiece(ABC):
    def __init__(self, kind, color, square):
        self.id = square.idx
        self.kind = kind
        self.color = color
        self.movesCnt = 0
        self.attacked_squares = [[]]
        self.square = square
        self.is_active = True

    def get_attacked_squares(self):
        return self.attacked_squares[-1]

    @abstractmethod
    def calc_potential_moves(self):
        pass

    @abstractmethod
    def calc_potential_moves_pinned(self):
        pass

    @abstractmethod
    def add_new_calculation(self):
        self.attacked_squares.append([])

    @abstractmethod
    def remove_last_calculation(self):
        self.attacked_squares.pop()

    @abstractmethod
    def update_attacked_squares(self):
        pass

    def calc_attacked_squares(self):
        return list(map(lambda mv: mv.toSqr, self.calc_potential_moves(ownPieces=True)))

    def get_legal_moves(self):
        if self.square.board.turn != self.color:
            return []
        return list(filter(lambda move: move.fromSqr == self.square, self.square.board.legal_moves[-1]))

    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return self.id

class cPieceWithPS(cPiece):
    def __init__(self, kind, color, square):
        super().__init__(kind, color, square)
        self.potential_squares = [[]]
        self.has_PT = True

    def get_potential_squares(self):
        return self.potential_squares[-1]

    def add_new_calculation(self):
        for sqr in self.get_attacked_squares():
            sqr.get_attacked_by(self.color).remove(self)
        self.attacked_squares.append([])
        self.potential_squares.append([])

    def remove_last_calculation(self):
        for sqr in self.get_attacked_squares():
           sqr.get_attacked_by(self.color).remove(self)
        self.attacked_squares.pop()
        for sqr in self.get_attacked_squares():
            if self not in sqr.get_attacked_by(self.color):
                sqr.get_attacked_by(self.color).append(self)
        self.potential_squares.pop()

    def update_attacked_squares(self):
        self.get_potential_squares().clear()
        if not self.is_active:
            for sqr in self.get_attacked_squares():
                sqr.get_attacked_by(self.color).remove(self)
            self.get_attacked_squares().clear()
            return

        self.get_attacked_squares().clear()

        for sqr in self.calc_attacked_squares():
            self.get_attacked_squares().append(sqr)
            if sqr.piece is None or sqr.piece.color != self.color:
                self.get_potential_squares().append(sqr)

            sqr.get_attacked_by(self.color).append(self)


class cPieceWithoutPS(cPiece):
    def __init__(self, kind, color, square):
        super().__init__(kind, color, square)
        self.has_PT = False

    def add_new_calculation(self):
        for sqr in self.get_attacked_squares():
            sqr.get_attacked_by(self.color).remove(self)
        self.attacked_squares.append([])

    def remove_last_calculation(self):
        for sqr in self.get_attacked_squares():
           sqr.get_attacked_by(self.color).remove(self)
        self.attacked_squares.pop()
        for sqr in self.get_attacked_squares():
            if self not in sqr.get_attacked_by(self.color):
                sqr.get_attacked_by(self.color).append(self)

    def update_attacked_squares(self):
        if not self.is_active:
            for sqr in self.get_attacked_squares():
                sqr.get_attacked_by(self.color).remove(self)
            self.get_attacked_squares().clear()
            return

        for sqr in self.calc_attacked_squares():
            self.get_attacked_squares().append(sqr)
            sqr.get_attacked_by(self.color).append(self)
