import pygame
from .constants import BLACK, ROWS, BLACK, SQUARE_SIZE, COLS, WHITE
from .pawn import Pawn

class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings_left = self.white_kings_left = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.black_left + (self.white_kings_left * 0.5 - self.black_kings_left * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for pawn in row:
                if pawn != 0 and pawn.color == color:
                    pieces.append(pawn)
        return pieces

    def move(self, pawn, row, col):
        self.board[pawn.row][pawn.col], self.board[row][col] = self.board[row][col], self.board[pawn.row][pawn.col]
        pawn.move(row, col)

        if row == ROWS - 1 or row == 0:
            pawn.make_king()
            if pawn.color == WHITE:
                self.white_kings_left += 1
            else:
                self.black_kings_left += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Pawn(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Pawn(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                pawn = self.board[row][col]
                if pawn != 0:
                    pawn.draw(win)

    def remove(self, pieces):
        for pawn in pieces:
            self.board[pawn.row][pawn.col] = 0
            if pawn != 0:
                if pawn.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        
        return None 
    
    def get_valid_moves(self, pawn):
        moves = {}
        left = pawn.col - 1
        right = pawn.col + 1
        row = pawn.row

        if pawn.color == BLACK or pawn.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, pawn.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, pawn.color, right))
        if pawn.color == WHITE or pawn.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, pawn.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, pawn.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves