from square import cSquare
from constants import *
from pawn import cPawn
from knight import cKnight
from bishop import cBishop
from rook import cRook
from queen import cQueen
from king import cKing
from square import cSquare
from icons import *
import re

class cBoard:
    def __init__(self, display):
        self.board = []
        for i in range(64):
            self.board.append(cSquare(i, self))
        self.turn = WHITE
        self.whitePieces = []
        self.blackPieces = []
        self.history = []
        self.castle_white_king = False
        self.castle_black_king = False
        self.castle_white_queen = False
        self.castle_black_queen = False
        self.en_passant = None
        self.half_moves = 0
        self.moves = 0
        self.display = display

    def loadFEN(self, fenstr):
        self.whitePieces.clear()
        self.blackPieces.clear()
        
        if not re.match(r'^([rnbqkpRNBQKP1-8]*/){7}[rnbqkpRNBQKP1-8]* [wb] (-|[KQkq]{1,4}) (-|[a-h][36]) [0-9]+ [0-9]+$', fenstr):
            raise ValueError('Invalid FEN position given')

        pieces, turn, castling, en_passant, halves, fulls = fenstr.split()

        i, j = 0, 7
        for c in pieces:
            if c.isnumeric():
                i += int(c)
                continue

            if c == '/':
                if i != 8:
                    raise ValueError('Invalid FEN position given')
                i, j = 0, j - 1
                continue

            if c.lower() == 'p':
                piece = PAWN
            elif c.lower() == 'n':
                piece = KNIGHT
            elif c.lower() == 'b':
                piece = BISHOP
            elif c.lower() == 'r':
                piece = ROOK
            elif c.lower() == 'q':
                piece = QUEEN
            elif c.lower() == 'k':
                piece = KING

            color = WHITE if c.isupper() else BLACK
            self.placePiece(i + 8*j, piece, color)    
            i += 1

        self.turn = WHITE if turn == 'w' else BLACK
        
        self.castle_white_king = 'K' in castling
        self.castle_white_queen = 'Q' in castling
        self.castle_black_king = 'k' in castling
        self.castle_black_queen = 'q' in castling
        
        self.en_passant = en_passant
        
        self.half_moves = int(halves)
        self.moves = int(fulls)
        
        self.calcAttackingSquares() # TODO - change to general init calculations

    def clear(self):
        self.loadFEN(FEN_CLEAN)
            
    def getSquare(self, col, row = None):
        # getSquare('a1') == getSquare(0) == getSquare(0, 0) == getSquare('a', 1) == getSquare('a', '1')
        # getSquare('h1') == getSquare(7) == getSquare(7, 0) == getSquare('a', 1) == getSquare('a', '1')
        # getSquare('a8') == getSquare(56) == getSquare(0, 7) == getSquare('a', 8) == getSquare('a', '8')
        # getSquare('h8') == getSquare(63) == getSquare(7, 7) == getSquare('h', 8) == getSquare('h', '8')

        if type(col) == int and type(row) == int:
            if col < 0 or col > 7 or row < 0 or row > 7:
                return None
            return self.board[col*8 + row]
        
        if type(col) == int and row == None:
            if col < 0 or col > 63:
                return None
            return self.board[col]
        
        if type(col) == str and row == None:
            row, col = int(col[1]), col[0]
        
        #row = int(row)
        if col < 'a' or col > 'h' or row < 1 or row > 8:
            return None
        return self.board[(ord(col) - 97) + (row - 1)*8]
        
        
    def placePiece(self, sqr, kind, color):
        if kind == PAWN: self.getSquare(sqr).piece = cPawn(color)
        elif kind == KNIGHT: self.getSquare(sqr).piece = cKnight(color)
        elif kind == BISHOP: self.getSquare(sqr).piece = cBishop(color)
        elif kind == ROOK: self.getSquare(sqr).piece = cRook(color)
        elif kind == QUEEN: self.getSquare(sqr).piece = cQueen(color)
        elif kind == KING: self.getSquare(sqr).piece = cKing(color)
        
        self.getSquare(sqr).piece.square = self.getSquare(sqr)
        
        if color == WHITE:
            self.whitePieces.append(self.getSquare(sqr).piece)
        else:
            self.blackPieces.append(self.getSquare(sqr).piece)

        col, row = self.getSquare(sqr).colIdx, self.getSquare(sqr).rowIdx
        self.displayPiece(col, row, kind, color)
        
    def removePiece(self, sqr):
        piece = self.getSquare(sqr).piece
        if not piece:
            raise ValueError
        
        if piece.color == WHITE:
            self.whitePieces.remove(piece)
        else:
            self.blackPieces.remove(piece)
            
        col, row = self.getSquare(sqr).colIdx, self.getSquare(sqr).rowIdx
        self.displayPiece(col, row, None, None)
        
        self.getSquare(sqr).piece = None
        
    def promotePiece(self, sqr, toKind):
        piece = self.getSquare(sqr).piece 
        if not piece:
            raise ValueError
        
        piece.kind = toKind
        
        col, row = self.getSquare(sqr).colIdx, self.getSquare(sqr).rowIdx
        self.displayPiece(col, row, piece.kind, piece.color)

    def displayPiece(self, col, row, kind, color):
        row = 7 - row
        if kind == None:
            icon = empty_icon
        elif color == WHITE:
            if kind == PAWN:
                icon = white_pawn_icon
            elif kind == KNIGHT:
                icon = white_knight_icon
            elif kind == BISHOP:
                icon = white_bishop_icon
            elif kind == ROOK:
                icon = white_rook_icon
            elif kind == QUEEN:
                icon = white_queen_icon
            else:
                icon = white_king_icon
        else:
            if kind == PAWN:
                icon = black_pawn_icon
            elif kind == KNIGHT:
                icon = black_knight_icon
            elif kind == BISHOP:
                icon = black_bishop_icon
            elif kind == ROOK:
                icon = black_rook_icon
            elif kind == QUEEN:
                icon = black_queen_icon
            else:
                icon = black_king_icon
            
        self.display[row][col].ImageData = icon
        self.display[row][col].Update(image_data=icon)
        
    def reset(self):
        self.loadFEN(FEN_INIT)
        
    def getKingIdxs(self, color):
        pieces = self.whitePieces if color == WHITE else self.blackPieces
        for piece in pieces:
            if piece.kind == KING:
                return piece.square.rowIdx, piece.square.colIdx
        return None, None
        
    def __str__(self):
        ret = ""
        for row in range(7, -1, -1):
            for col in range(8):
                ret +=  str(self.board[row * 8 + col]) + " " 
            ret += "\n"
        return ret
    
    def move(self, move, preview=False):
        if type(move) == str:
            if len(move) < 5:
                raise IndexError
            fromSqr = move[0:2]
            toSqr = move[3:5]
        elif type(move) == tuple:
            fromSqr, toSqr = move

        movPiece = self.getSquare(fromSqr).piece
        col, row = self.getSquare(toSqr).colIdx, self.getSquare(toSqr).rowIdx
        self.displayPiece(col, row, movPiece.kind, movPiece.color)

        col, row = self.getSquare(fromSqr).colIdx, self.getSquare(fromSqr).rowIdx            
        self.displayPiece(col, row, None, None)

        if self.getSquare(toSqr).piece is not None:
            if movPiece.color == WHITE:
                self.blackPieces.remove(self.getSquare(toSqr).piece)
            else:
                self.whitePieces.remove(self.getSquare(toSqr).piece)
        
        self.getSquare(toSqr).piece = movPiece
        self.getSquare(fromSqr).piece = None
        movPiece.square = self.getSquare(toSqr)
        movPiece.movesCnt += 1
        
        self.turn = WHITE if self.turn == BLACK else BLACK
        
        for piece in self.getSquare(fromSqr).attackedBy + self.getSquare(toSqr).attackedBy:
            piece.calcAttackingSquares()
            
        movPiece.calcAttackingSquares()
        
        if not preview:
            self.history.append(move)
        
    def getPossibleMoves(self, color=None):
        retLst = []
        if color == None:
            color = self.turn
        pieces = self.whitePieces if color == WHITE else self.blackPieces
        
        for piece in pieces:
            for dest in piece.getPotentialMoves():
                retLst.append(piece.square.getCoord() + "-" + dest.getCoord())
        return retLst
        
    def calcAttackingSquares(self):
        for piece in self.whitePieces + self.blackPieces:
            piece.calcAttackingSquares()
            
    def checkDirection(colIdx, rowIdx, direction):
        if direction == UP:
            colDiff, rowDiff = 0, 1
        elif direction == DOWN:
            colDiff, rowDiff = 0, -1
        elif direction == LEFT:
            colDiff, rowDiff = -1, 0
        elif direction == RIGHT:
            colDiff, rowDiff = 1, 0
        elif direction == UP_LEFT:
            colDiff, rowDiff = -1, 1
        elif direction == UP_RIGHT:
            colDiff, rowDiff = 1, 1
        elif direction == DOWN_LEFT:
            colDiff, rowDiff = -1, -1
        else: # DOWN_RIGHT
            colDiff, rowDiff = 1, -1
            
        colIdx, rowIdx = colIdx + colDiff, rowIdx + rowDiff
        while True:
            sqr = self.square.board.getSquare(colIdx, rowIdx)
            if sqr is None or not sqr.isFree():
                return sqr
            
    def isShortCastlePossible(self, color):
        if color == WHITE and not self.castle_white_king or color == BLACK and not self.castle_black_king:
            return False
        
        row = 1 if color == WHITE else 8
        
        piece = self.getSquare('e', row).piece
        if piece is None or piece.kind != KING or piece.color != color or piece.movesCnt != 0:
            return False
        
        piece = self.getSquare('h', row).piece
        if piece is None or piece.kind != ROOK or piece.color != color or piece.movesCnt != 0:
            return False
        
        if self.getSquare('f', row).piece is not None or self.getSquare('g', row).piece is not None:
            return False
        
        for square in [self.getSquare('e', row), self.getSquare('f', row), self.getSquare('g', row)]:
            for piece in square.attackedBy:
                if piece.color != color:
                    return False
            
        return True
    
    
    def isLongCastlePossible(self, color):
        if color == WHITE and not self.castle_white_queen or color == BLACK and not self.castle_black_queen:
            return False

        row = 1 if color == WHITE else 8
        
        piece = self.getSquare('e', row).piece
        if piece is None or piece.kind != KING or piece.color != color or piece.movesCnt != 0:
            return False
        
        piece = self.getSquare('a', row).piece
        if piece is None or piece.kind != ROOK or piece.color != color or piece.movesCnt != 0:
            return False
        
        if self.getSquare('d', row).piece is not None or self.getSquare('c', row).piece is not None or self.getSquare('b', row).piece is not None:
            return False
        
        for square in [self.getSquare('e', row), self.getSquare('d', row), self.getSquare('c', row)]:
            for piece in square.attackedBy:
                if piece.color != color:
                    return False
            
        return True
    
    def getAllMoves(self, color=None):
        if color == None:
            color = self.turn
        pieces = self.whitePieces if color == WHITE else self.blackPieces
        
        retLst = []
        for piece in pieces:
            for move in piece.getPotentialMoves():
                mvStr = piece.square.getCoord() + '-' + move.getCoord()
                if not self.inCheck(color, mvStr):
                    retLst.append((piece, move))
            
        return retLst
            
    def inCheck(self, color, move=None):
        if move:
            self.move(move)
            
        retVal = False
        col, row = self.getKingIdxs(color)
        for piece in self.getSquare(col, row).attackedBy:
            if piece.color != color:
                retVal = True
                break
        if move:
            self.move(move[3:5] + '-' + move[0:2])    
        return retVal
        
