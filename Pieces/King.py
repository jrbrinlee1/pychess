from Pieces.Piece import Piece
from Pieces.Team import Team
from Pieces.Rook import Rook


class King(Piece):

    def __init__(self, team, row, col,  init_position=True):
        super().__init__(team, row, col)
        self.image_path = "Images/bK.png" if self.team == Team.BLACK else "Images/wK.png"
        self.move_options = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        self.init_position = init_position

    def get_valid_moves(self, board, current_move=True):
        valid_moves = []
        # check normal moves
        for op in self.move_options:
            row = self.row + op[0]
            col = self.col + op[1]
            if row < 0 or col < 0:
                continue
            if board.is_space_empty(row, col) is not None:
                if board.is_space_empty(row, col):
                    valid_moves.append((row, col))
                else:
                    if board.team_on(row, col) != self.team:
                        valid_moves.append((row, col))

        valid_moves = self.try_adding_castle(board, valid_moves)
        valid_moves = self.harms_way(board, valid_moves)

        return valid_moves

    def try_adding_castle(self, board, valid_moves):
        # cannot castle in check or if king has already moved
        if self.in_check(board, (self.row, self.col)):
            return valid_moves
        if not self.init_position:
            return valid_moves

        col = 4
        row = 7 if self.team == Team.WHITE else 0

        king_side_rook = board.get_board()[row][col + 3]
        queen_side_rook = board.get_board()[row][col - 4]

        if king_side_rook:
            if isinstance(king_side_rook, Rook):
                if king_side_rook.init_position:
                    # piece in rook position is rook and hasn't moved
                    if not self.in_check(board, (row, col + 1)) and \
                       not self.in_check(board, (row, col + 2)) and \
                       board.is_space_empty(row, col + 1) and \
                       board.is_space_empty(row, col + 2):
                        # king isn't moving to/through check and there are no pieces between king and king side rook
                        valid_moves.append((row, col + 3))

        if queen_side_rook:
            if isinstance(queen_side_rook, Rook):
                if queen_side_rook.init_position:
                    # piece in rook position is rook and hasn't moved
                    if not self.in_check(board, (row, col - 1)) and \
                       not self.in_check(board, (row, col - 2)) and \
                       board.is_space_empty(row, col - 1) and \
                       board.is_space_empty(row, col - 2) and \
                       board.is_space_empty(row, col - 3):
                        # # king isn't moving to/through check and there are no pieces between king and queen side rook
                        valid_moves.append((row, col - 4))

        return valid_moves

    def in_check(self, board, location):
        change_team = Team.WHITE if self.team == Team.BLACK else Team.BLACK
        board.turn = change_team
        if (location[0], location[1]) in board.potential_next_moves():
            board.turn = self.team
            return True
        else:
            board.turn = self.team
            return False

    def move(self, row, col):
        castle = False
        if self.init_position:
            if self.team == Team.WHITE and row == 7 and col == 7:
                castle = True
                self.row = 7
                self.col = 6
            elif self.team == Team.WHITE and row == 7 and col == 0:
                castle = True
                self.row = 7
                self.col = 2
            elif self.team == Team.BLACK and row == 0 and col == 7:
                castle = True
                self.row = 0
                self.col = 6
            elif self.team == Team.BLACK and row == 0 and col == 0:
                castle = True
                self.row = 0
                self.col = 2
            else:
                self.row = row
                self.col = col
        else:
            self.row = row
            self.col = col

        self.init_position = False
        return castle

    def __str__(self):
        return " K "

    def copy(self):
        return King(self.team, self.row, self.col, self.init_position)

    def harms_way(self, board, valid_moves):
        remove_from_valid = []
        # make sure the king isn't moving into harms way
        for move in valid_moves:
            test_board, fatal = board.move_piece((self.row, self.col), move)
            if move in test_board.potential_next_moves():
                remove_from_valid.append(move)

        remove_from_valid = set(remove_from_valid)
        for move in remove_from_valid:
            if move in valid_moves:
                valid_moves.remove(move)

        return valid_moves
