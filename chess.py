#!/usr/bin/python3

from board import cBoard



board = cBoard()
#board.reset()
board.reset()
#board.placePiece('e3', ROOK, WHITE)
#board.placePiece('d1', QUEEN, WHITE)
#board.calcAttackingSquares()


while True:
    print(board)
    print('possible moves:')
    for piece, move in board.getAllMoves():
        print(piece, move.getCoord())
        
    mv = input("\nyour move: ")
    board.move(mv)

#for square in board.board:
    #if len(square.attackedBy) > 0:
        #print (square.getCoord(), ' - ', end='')
        #for p in square.attackedBy:
            #print (p.square.getCoord(), ' ', end='')
        #print()



#for piece in board.getSquare('e3').attackedBy:
    #print(piece.square.getCoord())

#for piece in board.whitePieces:
    #if piece.isAttackingSqr(3,1):
        #print(piece.square.getCoord())
#for move in board.getPotentialMoves():
    #print (move)
#for square in board.getSquare('d7').piece.getPotentialMoves():
    #print (square.getCoord())
