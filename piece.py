from constants import Color, PieceType

class Piece:
    def __init__(self, kind: PieceType, color: Color):
        self.kind = kind
        self.color = color

    def __str__(self) -> str:
        if self.kind == PieceType.PAWN: return 'P' if self.color == Color.WHITE else 'p'
        elif self.kind == PieceType.KNIGHT: return 'N' if self.color == Color.WHITE else 'n'
        elif self.kind == PieceType.BISHOP: return 'B' if self.color == Color.WHITE else 'b'
        elif self.kind == PieceType.ROOK: return 'R' if self.color == Color.WHITE else 'r'
        elif self.kind == PieceType.QUEEN: return 'Q' if self.color == Color.WHITE else 'q'
        else: return 'K' if self.color == Color.WHITE else 'k'

    def __repr__(self) -> str:
        return f'Piece({self.kind}, {self.color})'