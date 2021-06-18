from Pieces.Piece import Piece
from Pieces.Team import Team


class King(Piece):

    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image_path = "Images/bK.png" if self.team == Team.BLACK else "Images/wK.png"
        self.move_options = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_valid_moves(self, board):
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

        valid_moves = self.harms_way(board, valid_moves)

        return valid_moves

    def __str__(self):
        return " K "

    def copy(self):
        return King(self.team, self.row, self.col)

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
