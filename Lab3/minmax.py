import numpy as np
from copy import deepcopy


#TODO problem jest prawdopodobnie w głównej metodzie min max
def minimax_a_b(board, depth, plays_as_black, ev_func):
    possible_moves = board.get_possible_moves(plays_as_black)
    if len(possible_moves) == 0:
        board.white_won = plays_as_black
        board.is_running = False
        return None

    alpha = -np.inf
    beta = np.inf
    move_value_max = -np.inf
    move_value_min = np.inf

    best_move = None
    for move in possible_moves:
        simulation_board = deepcopy(board)
        simulation_board.make_move(move)
        move_evaluation = minimax_a_b_recursive(simulation_board, depth - 1, not plays_as_black, alpha, beta, ev_func)
        if plays_as_black:
            if move_evaluation > move_value_max:
                move_value_max = move_evaluation
                best_move = move
        else:
            if move_evaluation < move_value_min:
                move_value_min = move_evaluation
                best_move = move

    if plays_as_black:
        print("Czarny: ", best_move)
        print("Ocena: ", move_value_max)
    else:
        print("Biały: ", best_move)
        print("Ocena: ", move_value_min)

    return best_move


# recursive function, called from minimax_a_b
def minimax_a_b_recursive(board, depth, move_max, alpha, beta, ev_func):
    if depth == 0:
        return ev_func(board, move_max)

    possible_moves = board.get_possible_moves(move_max)

    if move_max:
        for move in possible_moves:
            simulation_board = deepcopy(board)
            simulation_board.make_move(move)
            alpha = max(alpha, minimax_a_b_recursive(simulation_board, depth - 1, not move_max, alpha, beta, ev_func))
            if alpha >= beta:
                return beta
        return alpha

    else:
        for move in possible_moves:
            simulation_board = deepcopy(board)
            simulation_board.make_move(move)
            beta = min(beta, minimax_a_b_recursive(simulation_board, depth - 1, not move_max, alpha, beta, ev_func))
            if alpha >= beta:
                return alpha
        return beta
