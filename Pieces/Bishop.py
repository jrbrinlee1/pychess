from Pieces.Team import Team
from Pieces.Piece import Piece


class Bishop(Piece):

    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image_path = "Images/bB.png" if self.team == Team.BLACK else "Images/wB.png"

    def get_valid_moves(self, board, current_move=True):
        """
        Method used to get the valid move for the bishop
        :param board: current board object
        :param current_move: True to remove moves from list if king will be in check, false otherwise
        :return: list of valid moves for current bishop
        """
        valid_moves = []
        options = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

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
        :return: string representation of a Bishop
        """
        return " B "

    def copy(self):
        """
        :return: copy of the current bishop piece
        """
        return Bishop(self.team, self.row, self.col)
