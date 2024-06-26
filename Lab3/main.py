"""
Nalezy napisac funkcje "minimax_a_b_recurr", "minimax_a_b" (ktora wola funkcje rekurencyjna) i funkcje "*ev_func", ktora oceniaja stan gry
"""


import pygame
import constants
import board as board_class
import game as game_class
import minmax
import evaluations
from Lab3 import board


def main():
    board = board_class.Board()
    window = pygame.display.set_mode((constants.WIN_WIDTH, constants.WIN_HEIGHT))
    is_running = True
    clock = pygame.time.Clock()
    game = game_class.Game(window, board)

    while is_running:
        clock.tick(constants.FPS)

        if not game.board.white_turn:
            move = minmax.minimax_a_b(game.board, constants.MINIMAX_DEPTH, True, evaluations.basic_ev_func)
            # move = minmax.minimax_a_b( game.board, constants.MINIMAX_DEPTH, True, evaluations.push_forward_ev_func)
            # move = minmax.minimax_a_b( game.board, constants.MINIMAX_DEPTH, True, evaluations.push_to_opp_half_ev_func)
            # move = minmax.minimax_a_b( game.board, constants.MINIMAX_DEPTH, True, evaluations.group_prize_ev_func)

            if move is not None:
                game.board.make_move(move)
            else:
                is_running = False
        if game.board.end():
            is_running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.clicked_at(pos)

        game.update()

    pygame.quit()

def ai_vs_ai():
    board = board_class.Board()
    is_running = True

    while is_running:
        if board.white_turn:
            move = minmax.minimax_a_b(board, 5, not board.white_turn, evaluations.basic_ev_func)
            # move = minmax.minimax_a_b(board, 5, not board.white_turn, evaluations.group_prize_ev_func)
            # move = minmax.minimax_a_b(board, 5, not board.white_turn, evaluations.push_to_opp_half_ev_func)
        else:
            move = minmax.minimax_a_b(board, 5, not board.white_turn, evaluations.basic_ev_func)
            # move = minmax.minimax_a_b(board, 5, not board.white_turn, evaluations.push_forward_ev_func)
            # move = minmax.minimax_a_b(board, 5, not board.white_turn, evaluations.push_to_opp_half_ev_func)
            # move = minmax.minimax_a_b(board, 5, not board.white_turn, evaluations.group_prize_ev_func)

        if move is not None:
            board.register_move(move)
            board.make_move(move)
        else:
            if board.white_turn:
                board.black_won = True
            else:
                board.white_won = True
            is_running = False
        if board.end():
            is_running = False

        if board.black_won and board.white_won:
            print("Remis")
        elif board.black_won:
            print("Czarne wygrały")
        elif board.white_won:
            print("Białe wygrały")


# main()
for i in range(0, 10):
    ai_vs_ai()


