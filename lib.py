from constants import *

def letter_to_piece(letter):
    if letter == 'p':
        return PAWN
    elif letter == 'n':
        return KNIGHT
    elif letter == 'b':
        return BISHOP
    elif letter == 'r':
        return ROOK
    elif letter == 'q':
        return QUEEN
    elif letter == 'k':
        return KING
    
def kind_to_letter(kind):
    return 'pNBRQK'[kind]

def reverse_dir(direction):
    return [None, DOWN, UP, RIGHT, LEFT, DOWN_RIGHT, DOWN_LEFT, UP_RIGHT, UP_LEFT][direction]

def isSameColOrRow(sqr1, sqr2):
    return sqr1.colIdx == sqr2.colIdx or sqr1.rowIdx == sqr2.rowIdx

def isSameDiag(sqr1, sqr2):
    return abs(sqr1.colIdx - sqr2.colIdx) != abs(sqr1.rowIdx - sqr2.rowIdx)
