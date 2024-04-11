import numpy as np
from copy import deepcopy

def minimax_a_b(board, depth, plays_as_black, ev_func):
    possible_moves = board.get_possible_moves(plays_as_black)
    if len(possible_moves) == 0:
        board.white_won = plays_as_black
        board.is_running = False
        return None

    alpha = -np.inf
    beta = np.inf
    moves_marks = []
    best_move = None
    for move in possible_moves:
        simulation_board = deepcopy(board)
        simulation_board.make_move(move)
        move_evaluation = minimax_a_b_recursive(simulation_board, depth - 1, not plays_as_black, alpha, beta, ev_func)

    print(best_move)
    if plays_as_black:
        print("Czarny: ", best_move[0])
    else:
        print("Biały: ", best_move[0])

    return best_move[1]


# recursive function, called from minimax_a_b
def minimax_a_b_recursive(board, depth, move_max, alpha, beta, ev_func):
    if depth == 0:
        return ev_func(board, move_max), board

    possible_moves = board.get_possible_moves(move_max)

    if move_max:
        best_move = None
        max_evaluation = -np.inf
        for possible_move in possible_moves:
            simulation_board = deepcopy(board)
            simulation_board.make_move(possible_move)
            simulated_move_evaluation = minimax_a_b_recursive(simulation_board, depth - 1, not move_max, alpha, beta, ev_func)[0]
            max_evaluation = max(max_evaluation, simulated_move_evaluation)
            alpha = max(alpha, simulated_move_evaluation)
            if max_evaluation == simulated_move_evaluation:
                best_move = possible_move
            if alpha >= beta:
                break
        return max_evaluation, best_move

    else:
        best_move = None
        min_evaluation = np.inf
        for possible_move in possible_moves:
            simulation_board = deepcopy(board)
            simulation_board.make_move(possible_move)
            simulated_move_evaluation = minimax_a_b_recursive(simulation_board, depth - 1, not move_max, alpha, beta, ev_func)[0]
            min_evaluation = min(min_evaluation, simulated_move_evaluation)
            beta = max(beta, simulated_move_evaluation)
            if min_evaluation == simulated_move_evaluation:
                best_move = possible_move
            if beta <= alpha:
                break
        return min_evaluation, best_move

    # ToDo
    # return b
