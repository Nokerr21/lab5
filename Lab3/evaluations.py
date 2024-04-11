import constants
# count difference between the number of pieces, king+10


def basic_ev_func(board, is_black_turn):
    white_pieces = 0
    white_kings = 0
    black_pieces = 0
    black_kings = 0
    evaluation = 0
    # in range((row + 1) % 2, constants.BOARD_WIDTH, 2)
    for row in range(0, constants.BOARD_WIDTH):
        for column in range((row + 1) % 2, constants.BOARD_WIDTH, 2):
            if board.board[row][column].is_white():
                if board.board[row][column].is_king():
                    white_kings += 1
                else:
                    white_pieces += 1
            elif board.board[row][column].is_black():
                if board.board[row][column].is_king():
                    black_kings += 1
                else:
                    black_pieces += 1



    # ToDo funkcja liczy i zwraca ocene aktualnego stanu planszy
    evaluation = (black_pieces + 10 * black_kings) + (-white_pieces - 10 * white_kings)


    # self.board[row][col].is_blue() - sprawdza czy to niebieski kolor figury
    # self.board[row][col].is_white()- sprawdza czy to biały kolor figury
    # self.board[row][col].is_king()- sprawdza czy to damka
    # self.board[row][col].row - wiersz na ktorym stoi figura
    # self.board[row][col].col - kolumna na ktorej stoi figura
    # wspolrzedne zaczynaja (0,0) sie od lewej od gory
    return evaluation


# nagrody jak w wersji podstawowej + nagroda za stopien zwartosci grupy
def group_prize_ev_func(board, is_black_turn):
    h = 0
    # ToDo
    return h


# za kazdy pion na wlasnej polowie planszy otrzymuje sie 5 nagrody, na polowie przeciwnika 7, a za kazda damke 10.
def push_to_opp_half_ev_func(board, is_black_turn):
    h = 0
    # ToDo
    return h


# za kazdy nasz pion otrzymuje sie nagrode w wysokosci: (5 + numer wiersza, na ktołrym stoi pion) (im jest blizej wroga tym lepiej), a za kazda damke dodtakowe: 10.
def push_forward_ev_func(board, is_black_turn):
    h = 0
    # ToDo
    return h


# f. called from main