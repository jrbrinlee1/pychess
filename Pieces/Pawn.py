from Pieces.Team import Team
from Pieces.Piece import Piece


class Pawn(Piece):

    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image_path = "Images/bP.png" if self.team == Team.BLACK else "Images/wP.png"

    def get_valid_moves(self, board, current_move=True):

        if self.team == Team.BLACK:
            initial_row = 1
            direction = 1
        else:
            initial_row = 6
            direction = -1

        valid_moves = []
        attack_forward_one_empty = board.is_space_empty(self.row + direction, self.col)
        attack_forward_two_empty = board.is_space_empty(self.row + 2 * direction, self.col)
        attack_right_empty = board.is_space_empty(self.row + direction, self.col + 1)
        attack_left_empty = board.is_space_empty(self.row + direction, self.col - 1)

        # if board location is False/Empty - non attacking moves
        if attack_forward_one_empty:
            if attack_forward_two_empty is not None:
                valid_moves.append((self.row + direction, self.col))
            if attack_forward_two_empty:
                if self.row == initial_row:
                    valid_moves.append((self.row + 2 * direction, self.col))

        # if board location is not Emtpy and is filled with other team - attacking moves
        if not attack_right_empty and attack_right_empty is not None:
            if board.board[self.row + direction][self.col + 1].get_team() != self.team:
                valid_moves.append((self.row + direction, self.col + 1))

        if not attack_left_empty and attack_left_empty is not None:
            if board.board[self.row + direction][self.col - 1].get_team() != self.team:
                valid_moves.append((self.row + direction, self.col - 1))

        if current_move:
            valid_moves = self.king_in_harms_way(board, valid_moves)

        return valid_moves

    def __str__(self):
        return " P "

    def copy(self):
        return Pawn(self.team, self.row, self.col)

    def get_attack_moves(self):
        if self.team == Team.BLACK:
            return [(self.row + 1, self.col + 1), (self.row + 1, self.col - 1)]
        else:
            return [(self.row - 1, self.col + 1), (self.row - 1, self.col - 1)]
