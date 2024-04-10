import numpy as np
from copy import deepcopy


def minimax_a_b(board, depth, plays_as_black, ev_func):
    #Format: [sourceRow, sourceCol, destRow, destCol, pieceId]
    possible_moves = board.get_possible_moves(plays_as_black)
    #TODO do usuniecia
    ev_func(board, 5)
    if len(possible_moves) == 0:
        board.white_won = plays_as_black
        board.is_running = False
        return None

    a = -np.inf
    b = np.inf
    moves_marks = []
    for possible_move in possible_moves:
        temp_board = deepcopy(board)
        temp_board.make_move(possible_move)
        minimax_a_b_recursive(temp_board, depth, plays_as_black, a, b, ev_func)
    # ToDo
        print(possible_move)

    # return possible_moves[best_index]


# recursive function, called from minimax_a_b
def minimax_a_b_recursive(board, depth, move_max, a, b, ev_func):
    if depth == 0:
        return ev_func(board, move_max)
    possible_moves = board.get_possible_moves(move_max)
    if move_max:
        best_move = None

    # ToDo
    return b