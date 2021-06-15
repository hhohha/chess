from lib import *

class cPiece:
    def __init__(self, kind, color):
        self.kind = kind
        self.color = color
        self.movesCnt = 0
        self.attackingSquares = []
        
    def get_potential_moves(self, ownPieces=False):
        return []
        
    def calcAttackingSquares(self):
        for sqr in self.attackingSquares:
            sqr.get_attacked_by(self.color).remove(self)
            
        self.attackingSquares = self.getAttackedSquares()
        
        for sqr in self.attackingSquares:
            sqr.get_attacked_by(self.color).append(self)
            
    def getAttackedSquares(self):
        return map(lambda move: move.toSqr, self.get_potential_moves(ownPieces=True))
    
    def is_pinned(self):
        kingSqr = self.square.board.get_king_sqr(self.color)
        if not kingSqr:
            return False
            
        kingColIdx, kingRowIdx = kingSqr.colIdx, kingSqr.rowIdx

        if self.square.colIdx == kingColIdx and self.square.rowIdx == kingRowIdx:
            return False
        
        if self.square.colIdx != kingColIdx and self.square.rowIdx != kingRowIdx and abs(kingColIdx - self.square.colIdx) != abs(kingRowIdx - self.square.rowIdx):
            return False

        if self.square.colIdx == kingColIdx and self.square.rowIdx > kingRowIdx:
            kingDir, otherDir, attPiece = DOWN, UP, ROOK
        elif self.square.colIdx == kingColIdx and self.square.rowIdx < kingRowIdx:
            kingDir, otherDir, attPiece = UP, DOWN, ROOK
        elif self.square.colIdx > kingColIdx and self.square.rowIdx == kingRowIdx:
            kingDir, otherDir, attPiece = LEFT, RIGHT, ROOK
        elif self.square.colIdx < kingColIdx and self.square.rowIdx == kingRowIdx:
            kingDir, otherDir, attPiece = RIGHT, LEFT, ROOK
        elif self.square.colIdx > kingColIdx and self.square.rowIdx > kingRowIdx:
            kingDir, otherDir, attPiece = DOWN_LEFT, UP_RIGHT, BISHOP
        elif self.square.colIdx < kingColIdx and self.square.rowIdx < kingRowIdx:
            kingDir, otherDir, attPiece = UP_RIGHT, DOWN_LEFT, BISHOP
        elif self.square.colIdx > kingColIdx and self.square.rowIdx < kingRowIdx:
            kingDir, otherDir, attPiece = UP_LEFT, DOWN_RIGHT, BISHOP
        else: #self.square.colIdx < kingColIdx and self.square.rowIdx > kingRowIdx
            kingDir, otherDir, attPiece = DOWN_RIGHT, UP_LEFT, BISHOP

        # check towards the king
        sqr = self.square.board.find_first_piece_in_dir(self.square, kingDir)
        if sqr is None or sqr.piece.kind != KING or sqr.piece.color != self.color:
            return False
            
        # check the other direction            
        sqr = self.square.board.find_first_piece_in_dir(self.square, otherDir)
        if sqr is None or sqr.piece.color == self.color:
            return False
        
        if sqr.piece.kind == QUEEN or sqr.piece.kind == attPiece:
            return otherDir
        return False

    def pprint(self):
        return kind_to_letter(self.kind) + self.square.getCoord()

    def get_legal_moves(self):
        if self.square.board.turn != self.color:
            return []
        return filter(lambda move: move.piece == self, self.square.board.legal_moves)
