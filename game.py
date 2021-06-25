class cGame:
    def __init__(self):
        self.history = []
        self.displayer = display
        self.legal_moves = []
        self.board = cBoard()
        
    def place_piece(self, sqr, kind, color):
        self.board.place_piece(sqr, kind, color)
        self.displayer.draw_square(square, square.piece)
        
    def remove_piece(self, piece, display=False):
        self.board.remove_piece(piece)
        if display:
            self.displayer.draw_square(piece.square, None)
        
    def reset(self):
        self.board.loadFEN(FEN_INIT)
        
    def check_game_end(self):
        if len(self.legal_moves) == 0:
            if self.is_in_check(self.turn):
                if self.turn == WHITE:
                    self.displayer.inform(GAME_WON_BLACK)
                else:
                    self.displayer.inform(GAME_WON_WHITE)
            else:
                self.displayer.inform(GAME_DRAW_STALEMATE)

            return
        
        pieces = self.board.get_pieces()
        if len(pieces) == 2 or (len(pieces) == 3 and any(map(lambda p: p.is_light(), pieces))):
            self.displayer.inform(GAME_DRAW_MATERIAL)
            
        if self.board.half_moves == 100:
            self.displayer.inform(GAME_DRAW_50_MOVES)

    def perform_move(self, move):
        fromSqr, toSqr, movPiece = move.fromSqr, move.toSqr, move.piece
        
        if move.is_promotion():
            move.newPiece = self.displayer.get_promoted_piece_from_diaog()
            self.displayer.draw_square(toSqr, movPiece)

        self.displayer.draw_square(fromSqr, None)
        self.displayer.draw_square(toSqr, movPiece)
        
        if move.is_castling():
            self.displayer.draw_square(self.getSquare(rookFrom), None)
            self.displayer.draw_square(self.getSquare(rookTo), self.getSquare(rookTo).piece)
            
        self.history.append(move)
        self.legal_moves = self.get_all_moves()
        self.legal_moves = self.get_all_moves()
