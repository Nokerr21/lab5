def alt_minimax_a_b(board, depth):
    a = float('-inf') #najleoszy wybrór dla max
    b = float('inf') #najleoszy wybrór dla min
    move_value_max = float('-inf')
    move_value_min = float('inf')
    move_max = not board.white_turn #max domyślnie niebieski
    moves = list(set(board.get_possible_moves(move_max)))
    best_move = np.random.choice(moves)
    #best_move_value = 0
    for move in moves:
        board_copy = deepcopy(board)
        board_copy.make_ai_move(move)
        move_value = alt_minimax_a_b_recurr(board_copy, depth-1, not move_max, a, b)
        #if best_move is None:
        #    best_move = move
        #    best_move_value = move_value
        if move_max:
            if move_value > move_value_max:
                best_move = move
                move_value_max = move_value
        else:
            if move_value < move_value_min:
                best_move = move
                move_value_min = move_value
    return best_move

def alt_minimax_a_b_recurr(board, depth, move_max, a, b):
    if depth == 0 or board.end():
        return board.evaluate1(move_max)
    moves = board.get_possible_moves(move_max)
    if move_max:
        for move in moves:
            board_copy = deepcopy(board)
            board_copy.make_ai_move(move)
            a = max(a,alt_minimax_a_b_recurr(board_copy, depth-1, False, a, b))
            if a >= b:
                return b
        return a
    else:
        for move in moves:
            board_copy = deepcopy(board)
            board_copy.make_ai_move(move)
            b = min(b, alt_minimax_a_b_recurr(board_copy, depth - 1, True, a, b))
            if a >= b:
                return a
        return b
