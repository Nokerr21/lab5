import numpy as np
from copy import deepcopy


# TODO problem jest prawdopodobnie w głównej metodzie min max
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
    best_moves = []
    # best_move = None
    for move in possible_moves:
        simulation_board = deepcopy(board)
        simulation_board.make_move(move)
        move_evaluation = minimax_a_b_recursive(simulation_board, depth - 1, not plays_as_black, alpha, beta, ev_func)
        # if plays_as_black:
        #     print("Czarny: ", move_evaluation)
        # else:
        #     print("Biały: ", move_evaluation)
        if plays_as_black:
            if move_evaluation > move_value_max:
                move_value_max = move_evaluation
                best_moves.clear()
                best_moves.append(move)
            elif move_evaluation == move_value_max:
                best_moves.append(move)

        else:
            if move_evaluation < move_value_min:
                move_value_min = move_evaluation
                best_moves.clear()
                best_moves.append(move)
            elif move_evaluation == move_value_min:
                best_moves.append(move)

    # if plays_as_black:
    #     print("Czarny: ", best_moves)
    #     print("Ocena: ", move_value_max)
    # else:
    #     print("Biały: ", best_moves)
    #     print("Ocena: ", move_value_min)

    return np.random.choice(best_moves)


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










#FROM TEMP

# def minimax_a_b(board, depth, plays_as_black, ev_func):
#     a = float('-inf')  # najleoszy wybrór dla max
#     b = float('inf')  # najleoszy wybrór dla min
#     move_value_max = float('-inf')
#     move_value_min = float('inf')
#     move_max = plays_as_black  # max domyślnie niebieski
#     moves = board.get_possible_moves(move_max)
#     best_move = np.random.choice(moves)
#     for move in moves:
#         board_copy = deepcopy(board)
#         board_copy.make_move(move)
#         move_value = minimax_a_b_recursive(board_copy, depth - 1, not move_max, a, b, ev_func)
#         if move_max:
#             if move_value > move_value_max:
#                 best_move = move
#                 move_value_max = move_value
#         else:
#             if move_value < move_value_min:
#                 best_move = move
#                 move_value_min = move_value
#     return best_move


# def minimax_a_b_recursive(board, depth, move_max, alpha, beta, ev_func):
#     if depth == 0 or board.end():
#         return ev_func(board, move_max)
#     moves = board.get_possible_moves(move_max)
#     if move_max:
#         for move in moves:
#             board_copy = deepcopy(board)
#             board_copy.make_move(move)
#             alpha = max(alpha, minimax_a_b_recursive(board_copy, depth - 1, False, alpha, beta, ev_func))
#             if alpha >= beta:
#                 return beta
#         return alpha
#     else:
#         for move in moves:
#             board_copy = deepcopy(board)
#             board_copy.make_move(move)
#             beta = min(beta, minimax_a_b_recursive(board_copy, depth - 1, True, alpha, beta, ev_func))
#             if alpha >= beta:
#                 return alpha
#         return beta