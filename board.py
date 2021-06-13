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
from lib import *
import re

class cDisplayer:
    def __init__(self, display):
        self.display = display
        self.lighted_squares = []
    
    def clear(self):
        for i in range(8):
            for j in range(8):
                if self.display[i][j].ImageData != empty_icon:
                    self.display[i][j].Update(image_data=empty_icon)
                    self.display[i][j].ImageData=empty_icon

    def draw_square(self, sqr, piece):
        icon = self._get_icon(piece)
        self.display[7-sqr.rowIdx][sqr.colIdx].Update(image_data=icon)
        self.display[7-sqr.rowIdx][sqr.colIdx].ImageData = icon
    
    def light_squares(self, squares, intensity=1):
        self.lighted_squares += squares
        for sqr in squares:
            color = self._get_color(sqr, intensity)
            self.display[7-sqr.rowIdx][sqr.colIdx].Update(button_color=color)
            
    def unlight_squares(self):
        self.light_squares(self.lighted_squares, 0)
        self.lighted_squares = []
    
    def _get_icon(self, piece):
        if piece == None:
            return empty_icon
        elif piece.color == WHITE:
            if piece.kind == PAWN:
                return white_pawn_icon
            elif piece.kind == KNIGHT:
                return white_knight_icon
            elif piece.kind == BISHOP:
                return white_bishop_icon
            elif piece.kind == ROOK:
                return white_rook_icon
            elif piece.kind == QUEEN:
                return white_queen_icon
            else:
                return white_king_icon
        else:
            if piece.kind == PAWN:
                return black_pawn_icon
            elif piece.kind == KNIGHT:
                return black_knight_icon
            elif piece.kind == BISHOP:
                return black_bishop_icon
            elif piece.kind == ROOK:
                return black_rook_icon
            elif piece.kind == QUEEN:
                return black_queen_icon
            else:
                return black_king_icon
    
    def _get_color(self, sqr, intensity):
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

class cBoard:
    def __init__(self, display):
        self.board = []
        for i in range(64):
            self.board.append(cSquare(i, self))
        self.turn = WHITE
        self.white_pieces = []
        self.black_pieces = []
        self.white_sliding_pieces = []
        self.black_sliding_pieces = []
        self.history = []
        self.castle_white_king = False
        self.castle_black_king = False
        self.castle_white_queen = False
        self.castle_black_queen = False
        self.en_passant = None
        self.half_moves = 0
        self.moves = 0
        self.displayer = cDisplayer(display)
        self.white_king_sqr = None
        self.black_king_sqr = None

    def loadFEN(self, fenstr):
        self.clear()
        
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

            piece = letter_to_piece(c.lower())

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
        
        self.calcAttackingSquares()
        print (self)

    def clear(self):
        for sqr in self.board:
            sqr.piece = None
            
        self.white_pieces = []
        self.black_pieces = []
        self.white_sliding_pieces = []
        self.black_sliding_pieces = []
        self.history = []
        self.half_moves = 0
        self.moves = 0
        
        self.displayer.clear()
            
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
        square = self.getSquare(sqr)
        
        if kind == PAWN: square.piece = cPawn(color)
        elif kind == KNIGHT: square.piece = cKnight(color)
        elif kind == BISHOP: square.piece = cBishop(color)
        elif kind == ROOK: square.piece = cRook(color)
        elif kind == QUEEN: square.piece = cQueen(color)
        elif kind == KING: square.piece = cKing(color)
        
        square.piece.square = square
        
        self.get_pieces(color).append(square.piece)
            
        if kind == KING:
            if color == WHITE:
                self.white_king_sqr = square
            else:
                self.black_king_sqr = square

        self.displayer.draw_square(square, square.piece)
        
    def reset(self):
        self.loadFEN(FEN_INIT)
        
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
            fr = move[0:2]
            to = move[3:5]
        elif type(move) == tuple:
            fr, to = move

        fromSqr = self.getSquare(fr)
        toSqr = self.getSquare(to)
        movPiece = fromSqr.piece
        
        self.displayer.draw_square(fromSqr, None)
        self.displayer.draw_square(toSqr, movPiece)

        # TODO get rid of WHITE/BLACK, remove from sliding if needed
        if toSqr.piece is not None:
            if movPiece.color == WHITE:
                self.black_pieces.remove(toSqr.piece)
                for sqr in toSqr.piece.attackingSquares:
                    sqr.attacked_by_blacks.remove(toSqr.piece)
            else:
                self.white_pieces.remove(toSqr.piece)
                for sqr in toSqr.piece.attackingSquares:
                    sqr.attacked_by_whites.remove(toSqr.piece)
        
        toSqr.piece = movPiece
        fromSqr.piece = None
        movPiece.square = toSqr
        movPiece.movesCnt += 1
        
        self.turn = WHITE if self.turn == BLACK else BLACK
        
        if movPiece.kind == KING:
            if movPiece.color == WHITE:
                self.white_king_sqr = toSqr
            else:
                self.black_king_sqr = toSqr
        
        for piece in fromSqr.attacked_by_whites + fromSqr.attacked_by_blacks + toSqr.attacked_by_whites + toSqr.attacked_by_blacks:
            if piece.is_sliding:
                piece.calcAttackingSquares()
            
        movPiece.calcAttackingSquares()
        
        if not preview:
            self.history.append(move)
        
    def calcAttackingSquares(self):
        for piece in self.white_pieces + self.black_pieces:
            piece.calcAttackingSquares()

    def get_pinned_pieces(self, color):
        for piece self.get_pieces(not color, sliding=True):
            pass
        # TODO - continue

    def get_all_moves(self, color):
        
        pieces = self.get_pieces(color)
        
        pinned_pieces = self.get_pinned_pieces(color)
        
        moves = []
        
        if not self.is_in_check(color):
            for piece in pieces:
                pinned = piece.is_pinned()
                if not pinned:
                    moves += piece.getPotentialMoves()
                else:
                    moves += piece.get_potential_moves_pinned(pinned)
        
        
        # TODO - continue        
        
            
        
    def check_direction(rowIdx, colIdx, direction, includePath=False):
        ds = [(0, 0), (0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]
        colDiff, rowDiff = ds[direction]
        colIdx, rowIdx = colIdx + colDiff, rowIdx + rowDiff
        path = []

        while True:
            sqr = self.square.board.getSquare(colIdx, rowIdx)
            if sqr is None or not sqr.is_free():
                return path + [sqr] if includePath else sqr
            elif includePath:
                path.append(sqr)
            
    def get_king_sqr(self, color):
        if color == WHITE:
            return self.white_king_sqr
        return self.black_king_sqr
    
    def is_in_check(self, color):
        kingSqr = self.get_king_sqr(color)
        if not kingSqr:
            return False
        
        return kingSqr.is_attacked_by(not color)
