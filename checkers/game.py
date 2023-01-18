import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, BOT_SIZE, LEFT_SIZE
from checkers.board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)

        mandatory_pieces = []
        if piece != 0 and piece.color == self.turn:
            mandatory_pieces = self.board.get_mandatory_pieces(piece.color)
        # all OK

        if piece != 0 and piece.color == self.turn:
            if len(mandatory_pieces) > 0:
                # mandatory_pieces = self.board.get_mandatory_pieces(piece.color)
                if piece in mandatory_pieces:
                    self.selected = piece
                    self.valid_moves = self.board.get_mandatory_moves(piece)

                    return True
            else:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)

                return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            print(self.valid_moves)
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * BOT_SIZE + BOT_SIZE // 2, row * LEFT_SIZE + LEFT_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
