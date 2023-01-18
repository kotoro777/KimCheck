from constants.constants import SQUARE_SIZE, WHITE
from checkers.game import Game
from algorithms.minimax import minimax
import pygame


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def play():
    pygame.init()
    pygame.display.set_caption('CHECKERS')
    window = pygame.display.set_mode((600, 600))

    flag = True
    clock = pygame.time.Clock()
    game = Game(window)

    while flag:
        clock.tick(60)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)

        if game.winner() is not None:
            print(game.winner())
            flag = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()
