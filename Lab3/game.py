import constants
import pygame


class Game:
    def __init__(self, window, board):
        self.window = window
        self.board = board
        self.something_is_marked = False
        self.marked_col = None
        self.marked_row = None
        self.pos_moves = {}

    def __draw(self):
        self.window.fill(constants.BRIGHT_BOARD_COL)
        # draw board
        for row in range(constants.BOARD_HEIGHT):
            for col in range((row + 1) % 2, constants.BOARD_WIDTH, 2):
                y = row * constants.FIELD_SIZE
                x = col * constants.FIELD_SIZE
                pygame.draw.rect(self.window, constants.DARK_BOARD_COL, (x, y, constants.FIELD_SIZE, constants.FIELD_SIZE))

        # draw pieces
        for row in range(constants.BOARD_HEIGHT):
            for col in range((row + 1) % 2, constants.BOARD_WIDTH, 2):
                cur_col = None
                if self.board.board[row][col].is_white():
                    cur_col = constants.WHITE_PIECES_COL
                elif self.board.board[row][col].is_black():
                    cur_col = constants.BLACK_PIECES_COL
                if cur_col is not None:
                    x = col * constants.FIELD_SIZE
                    y = row * constants.FIELD_SIZE
                    pygame.draw.circle(self.window, cur_col, (x + constants.FIELD_SIZE / 2, y + constants.FIELD_SIZE / 2), constants.PIECE_SIZE)
                    if self.board.board[row][col].is_king():
                        pygame.draw.circle(self.window, constants.KING_MARK_COL, (x + constants.FIELD_SIZE / 2, y + constants.FIELD_SIZE / 2),
                                           constants.PIECE_SIZE / 2)

        # if piece is marked by user, mark it and possible moves
        if self.something_is_marked:
            x = self.marked_col * constants.FIELD_SIZE
            y = self.marked_row * constants.FIELD_SIZE
            pygame.draw.circle(self.window, constants.POSS_MOVE_MARK_COL, (x + constants.FIELD_SIZE / 2, y + constants.FIELD_SIZE / 2),
                               constants.PIECE_SIZE + constants.MARK_THICK, constants.MARK_THICK)
            pos_moves = self.board.get_piece_moves(self.board.board[self.marked_row][self.marked_col])
            for pos_move in pos_moves:
                self.pos_moves[(pos_move.dest_row, pos_move.dest_col)] = pos_move
                x = pos_move.dest_col * constants.FIELD_SIZE
                y = pos_move.dest_row * constants.FIELD_SIZE
                pygame.draw.circle(self.window, constants.POSS_MOVE_MARK_COL, (x + constants.FIELD_SIZE / 2, y + constants.FIELD_SIZE / 2),
                                   constants.POS_MOVE_MARK_SIZE)

    def update(self):
        self.__draw()
        pygame.display.update()

    def mouse_to_indexes(self, pos):
        return (int(pos[0] // constants.FIELD_SIZE), int(pos[1] // constants.FIELD_SIZE))

    def clicked_at(self, pos):
        (col, row) = self.mouse_to_indexes(pos)
        field = self.board.board[row][col]
        if self.something_is_marked:
            if (row, col) in self.pos_moves:
                self.board.make_move(self.pos_moves[(row, col)])
                self.something_is_marked = False
                self.pos_moves = {}

        if field.is_white():
            if self.something_is_marked:
                self.something_is_marked = False
                self.pos_moves = {}
            else:
                self.something_is_marked = True
                self.marked_col = col
                self.marked_row = row
