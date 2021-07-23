from Pieces.Team import Team
from Pieces.Piece import Piece


class Rook(Piece):

    def __init__(self, team, row, col, init_position=True):
        super().__init__(team, row, col)
        self.image_path = "Images/bR.png" if self.team == Team.BLACK else "Images/wR.png"
        self.init_position = init_position

    def get_valid_moves(self, board, current_move=True):
        """
        Method used to get the valid move for the rook
        :param board: current board object
        :param current_move: True to remove moves from list if king will be in check, false otherwise
        :return: list of valid moves for current rook
        """
        valid_moves = []
        options = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for op in options:
            for i in range(1, 9):
                row = self.row + op[0] * i
                col = self.col + op[1] * i
                if row < 0 or col < 0:
                    break
                if board.is_space_empty(row, col) is not None:
                    if board.is_space_empty(row, col):
                        valid_moves.append((row, col))
                    else:
                        if board.team_on(row, col) != self.team:
                            valid_moves.append((row, col))
                        break
                else:
                    break

        if current_move:
            valid_moves = self.king_in_harms_way(board, valid_moves)

        return valid_moves

    def __str__(self):
        """
        :return: string representation of a rook
        """
        return " R "

    def copy(self):
        """
        :return: copy of the current rook piece
        """
        return Rook(self.team, self.row, self.col, self.init_position)

    def move(self, row, col):
        """
        Updates the location details of current rook piece (self.row and self.col) and it stores that it's been moved
        :param row: destination row
        :param col: destination column
        """
        self.row = row
        self.col = col
        self.init_position = False
