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
