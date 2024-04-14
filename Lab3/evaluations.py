import constants


# count difference between the number of pieces, king+10


def basic_ev_func(board, is_black_turn):
    evaluation = 0
    for row in range(0, constants.BOARD_WIDTH):
        for column in range((row + 1) % 2, constants.BOARD_WIDTH, 2):
            if not board.board[row][column].is_empty():
                if board.board[row][column].is_white():
                    if board.board[row][column].is_king():
                        evaluation -= 10
                    else:
                        evaluation -= 1

                elif board.board[row][column].is_black():
                    if board.board[row][column].is_king():
                        evaluation += 10
                    else:
                        evaluation += 1

    return evaluation


# nagrody jak w wersji podstawowej + nagroda za stopien zwartosci grupy
def group_prize_ev_func(board, is_black_turn):
    evaluation = 0
    for row in range(0, constants.BOARD_WIDTH):
        for column in range((row + 1) % 2, constants.BOARD_WIDTH, 2):
            if not board.board[row][column].is_empty():
                if board.board[row][column].is_white():
                    if board.board[row][column].is_king():
                        evaluation -= 10
                    else:
                        evaluation -= 1
                    if is_piece_on_border(row, column):
                        evaluation -= 3
                    else:
                        if board.board[row - 1][column - 1].is_white():
                            evaluation -= add_points_for_grouping()
                        if board.board[row - 1][column + 1].is_white():
                            evaluation -= add_points_for_grouping()
                        if board.board[row - 1][column - 1].is_white():
                            evaluation -= add_points_for_grouping()
                        if board.board[row + 1][column + 1].is_white():
                            evaluation -= add_points_for_grouping()
                elif board.board[row][column].is_black():
                    if board.board[row][column].is_king():
                        evaluation += 10
                    else:
                        evaluation += 1
                    if is_piece_on_border(row, column):
                        evaluation += 3
                    else:
                        if board.board[row - 1][column - 1].is_black():
                            evaluation += add_points_for_grouping()
                        if board.board[row - 1][column + 1].is_black():
                            evaluation += add_points_for_grouping()
                        if board.board[row - 1][column - 1].is_black():
                            evaluation += add_points_for_grouping()
                        if board.board[row + 1][column + 1].is_black():
                            evaluation += add_points_for_grouping()

    return evaluation


def is_piece_on_border(row, column):
    return row == 0 or row == constants.BOARD_HEIGHT - 1 or column == 0 or column == constants.BOARD_WIDTH - 1


def add_points_for_grouping():
    return 1


# za kazdy pion na wlasnej polowie planszy otrzymuje sie 5 nagrody, na polowie przeciwnika 7, a za kazda damke 10.
def push_to_opp_half_ev_func(board, is_black_turn):
    evaluation = 0
    for row in range(0, constants.BOARD_WIDTH):
        for column in range((row + 1) % 2, constants.BOARD_WIDTH, 2):
            if not board.board[row][column].is_empty():
                if board.board[row][column].is_white():
                    if board.board[row][column].is_king():
                        evaluation -= 10
                    else:
                        if row >= 4:
                            evaluation -= 5
                        else:
                            evaluation -= 7
                elif board.board[row][column].is_black():
                    if board.board[row][column].is_king():
                        evaluation += 10
                    else:
                        if row >= 4:
                            evaluation += 7
                        else:
                            evaluation += 5

    return evaluation


# za kazdy nasz pion otrzymuje sie nagrode w wysokosci: (5 + numer wiersza, na ktołrym stoi pion) (im jest blizej wroga tym lepiej), a za kazda damke dodtakowe: 10.
def push_forward_ev_func(board, is_black_turn):
    evaluation = 0
    for row in range(0, constants.BOARD_WIDTH):
        for column in range((row + 1) % 2, constants.BOARD_WIDTH, 2):
            if not board.board[row][column].is_empty():
                if board.board[row][column].is_white():
                    evaluation = evaluation - 5 - (7 - row)
                    if board.board[row][column].is_king():
                        evaluation -= 10
                elif board.board[row][column].is_black():
                    evaluation = evaluation + 5 + row
                    if board.board[row][column].is_king():
                        evaluation += 10

    return evaluation
