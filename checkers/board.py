import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, LEFT_SIZE, BOT_SIZE
from .piece import Piece


def draw_squares(win):
    win.fill(BLACK)
    for row in range(COLS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(win, RED, (row * LEFT_SIZE, col * BOT_SIZE, BOT_SIZE, LEFT_SIZE))


def get_opposite_color(color):
    if color == RED:
        return WHITE
    elif color == WHITE:
        return RED


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 3:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        self.board[0][3].make_king()
        self.board[0][5].make_king()
        self.board[6][3].make_king()
        self.board[6][5].make_king()

    def draw(self, win):
        draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

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
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
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
            if right >= COLS:  # проверка на границы
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def get_mandatory_moves(self, piece):
        moves = self.get_all_moves(piece)
        # moves = self.get_moves(piece.row, piece.col, piece.color, 0)
        mandatory_moves = {}
        l = 1
        for item in moves.items():
            if len(item[1]) == l:
                mandatory_moves.update({item[0]: item[1]})
            if len(item[1]) > l:
                mandatory_moves = {item[0]: item[1]}
                l = len(item[1])

        return mandatory_moves

    def get_mandatory_pieces(self, color):

        mandatory_pieces = []
        l = 1
        for piece in self.get_all_pieces(color):
            moves = self.get_all_moves(piece)
            # moves = self.get_moves(piece.row, piece.col, piece.color, 0)
            for value in moves.values():
                if len(value) == l:
                    mandatory_pieces.append(piece)
                if len(value) > l:
                    l = len(value)
                    mandatory_pieces = [piece]

        return mandatory_pieces

    def get_all_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
        moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
        moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves


"""
   def get_moves(self, row, col, color, counter):
        moves = {}
        counter += 1
        # проверка на скиппед

        if row - 2 >= 0 and col - 2 >= 0:
            if self.board[row - 1][col - 1] != 0:
                piece = self.board[row - 1][col - 1]
                piece2 = self.board[row - 2][col - 2]
                if piece.color == get_opposite_color(color) and piece2 == 0:  # self.board[row - 2][col - 2] == 0:
                    l = [piece]
                    if (row, col) in moves.keys():
                        l = l + moves[(row, col)]
                        # moves.pop(row, col)
                    moves[(row - 2, col - 2)] = l
                    if counter < 12:
                        moves.update(self.get_moves(row - 2, col - 2, color, counter))

        # проверка на скиппед
        if row + 2 <= ROWS - 1 and col + 2 <= COLS - 1:
            if self.board[row + 1][col + 1] != 0:
                piece = self.board[row + 1][col + 1]
                piece2 = self.board[row + 2][col + 2]
                if piece.color == get_opposite_color(color) and piece2 == 0:
                    l = [piece]
                    if (row, col) in moves.keys():
                        l = l + moves[(row, col)]
                        # moves.pop(row, col)
                    moves[(row + 2, col + 2)] = l
                    if counter < 12:
                        moves.update(self.get_moves(row + 2, col + 2, color, counter))



        # проверка на скиппед
        if row - 2 >= 0 and col + 2 <= COLS - 1:
            if self.board[row - 1][col + 1] != 0:
                piece = self.board[row - 1][col + 1]
                piece2 = self.board[row - 2][col + 2]
                if piece.color == get_opposite_color(color) and piece2 == 0:  # self.board[row - 2][col + 2] == 0:
                    l = [piece]
                    if (row, col) in moves.keys():
                        l = l + moves[(row, col)]
                        # moves.pop(row, col)
                    moves[(row - 2, col + 2)] = l
                    if counter < 12:
                        moves.update(self.get_moves(row - 2, col + 2, color, counter))

        # проверка на скиппед
        if row + 2 <= ROWS - 1 and col - 2 >= 0:
            if self.board[row + 1][col - 1] != 0:
                piece = self.board[row + 1][col - 1]
                piece2 = self.board[row + 2][col - 2]
                if piece.color == get_opposite_color(color) and piece2 == 0:  # self.board[row + 2][col - 2] == 0:
                    l = [piece]
                    if (row, col) in moves.keys():
                        l = l + moves[(row, col)]
                        # moves.pop(row, col)
                    moves[(row + 2, col - 2)] = l
                    if counter < 12:
                        moves.update(self.get_moves(row + 2, col - 2, color, counter))
                    # moves.update(self.get_moves(row + 2, col - 2, color))

        return moves



"""

