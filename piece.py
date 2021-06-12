from lib import *

class cPiece:
    def __init__(self, kind, color):
        self.kind = kind
        self.color = color
        self.movesCnt = 0
        self.attackingSquares = []
        
    def getPotentialMoves(self, ownPieces=False):
        return []
        
    def calcAttackingSquares(self):
        for sqr in self.attackingSquares:
            if self.color == WHITE:
                sqr.attacked_by_whites.remove(self)
            else:
                sqr.attacked_by_blacks.remove(self)
            
        self.attackingSquares = self.getAttackedSquares()
        
        for sqr in self.attackingSquares:
            if self.color == WHITE:
                sqr.attacked_by_whites.append(self)
            else:
                sqr.attacked_by_blacks.append(self)
                
            
    def getAttackedSquares(self):
        return self.getPotentialMoves(ownPieces=True)
    
    def isPinned(self):
        kingColIdx, kingRowIdx = self.square.board.getKingIdxs(self.color)
        if kingColIdx is None or self.square.colIdx == kingColIdx and self.square.rowIdx == kingRowIdx:
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
        sqr = self.square.board.checkDirection(self.square.rowIdx, self.square.colIdx, kingDir)
        if sqr is None or sqr.piece.kind != KING or sqr.piece.color != self.color:
            return False
            
        # check the other direction            
        sqr = self.square.board.checkDirection(self.square.rowIdx, self.square.colIdx, otherDir)
        if sqr is None or sqr.piece.color == self.color:
            return False
        
        return sqr.piece.kind == QUEEN or sqr.piece.kind == attPiece

    def pprint(self):
        return kind_to_letter(self.kind) + self.square.getCoord()
