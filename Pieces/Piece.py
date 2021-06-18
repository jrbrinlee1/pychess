from abc import ABC, abstractmethod
from Pieces.Team import Team


class Piece(ABC):
    """
    Abstract class for all the different pieces on the board.
    """

    def __init__(self, team, row, col):
        self.team = team
        self.row = row
        self.col = col

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_valid_moves(self, board, current_move=False):
        pass

    @abstractmethod
    def copy(self):
        pass

    def king_in_harms_way(self, board, valid_moves):
        """
        for king, use it's own harms way method
        :param board:
        :param valid_moves:
        :return:
        """

        king = board.white_king if self.team == Team.WHITE else board.black_king

        remove_from_valid = []
        # make sure the king isn't moving into harms way
        for move in valid_moves:
            test_board, fatal = board.move_piece((self.row, self.col), move)
            if (king.row, king.col) in test_board.potential_next_moves():
                remove_from_valid.append(move)

        remove_from_valid = set(remove_from_valid)
        for move in remove_from_valid:
            if move in valid_moves:
                valid_moves.remove(move)

        return valid_moves

    def move(self, row, col):
        self.row = row
        self.col = col

    def get_team(self):
        return self.team

    def get_location(self):
        return self.row, self.col

    def harms_way(self, board, current_valid_moves):
        pass
        '''
        for move in current_valid_moves:
            temp_board, fatal = board.move_piece(self.get_location(), move)
            for ret_move in temp_board.get_all_moves_and_next_to_king():
                king = temp_board.white_king if self.team == Team.WHITE else board.black_king
                if king.get_location() == ret_move:
                    current_valid_moves.remove(move)
        '''





