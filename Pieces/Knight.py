from Pieces.Team import Team
from Pieces.Piece import Piece


class Knight(Piece):

    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image_path = "Images/bN.png" if self.team == Team.BLACK else "Images/wN.png"

    def get_valid_moves(self, board, current_move=True):
        """
        Method used to get the valid move for the knight
        :param board: current board object
        :param current_move: True to remove moves from list if king will be in check, false otherwise
        :return: list of valid moves for current knight
        """
        valid_moves = []
        options = [(1, 2), (2, 1), (1, -2), (-2, 1), (-1, 2), (2, -1), (-1, -2), (-2, -1)]

        for op in options:
            i = self.row + op[0]
            j = self.col + op[1]

            if i < 0 or j < 0:
                continue

            if board.is_space_empty(i, j) is not None:
                if board.is_space_empty(i, j):
                    valid_moves.append((i, j))
                elif board.team_on(i, j) != self.team:
                    valid_moves.append((i, j))
            else:
                continue

        if current_move:
            valid_moves = self.king_in_harms_way(board, valid_moves)

        return valid_moves

    def __str__(self):
        """
        :return: string representation of a knight
        """
        return " K "

    def copy(self):
        """
        :return: copy of the current knight piece
        """
        return Knight(self.team, self.row, self.col)


