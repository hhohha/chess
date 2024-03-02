import sys
sys.path.append('../c_engine')
from libboard import Board

b = Board()
b.load_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
for move in b.get_legal_moves().split():
    print(move)
b.make_move('e2e4')
print('---')
for move in b.get_legal_moves().split():
    print(move)

b.make_move('d2d4')
print('---')
for move in b.get_legal_moves().split():
    print(move)