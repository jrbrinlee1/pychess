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
        self.is_king = False

    @abstractmethod
    def __str__(self):
        """
        :return: what should be printed
        """
        pass

    @abstractmethod
    def get_valid_moves(self, board, current_move=False):
        """
        :param board: Type Board which is the current state of the board
        :param current_move: actually making move
        :return:
        """
        pass

    @abstractmethod
    def copy(self):
        """
        :return: copy of the current piece
        """
        pass

    def king_in_harms_way(self, board, valid_moves):
        """
        default king_in_harms_way method (only king overrides this version)
        :param board: current board object
        :param valid_moves: list of current valid moves
        :return: updated valid_moves list (List(Tuple)) with moves removed that would leave the king in check
        """
        copy = board.copy_board_object()

        pieces = copy.white_pieces if self.team == Team.WHITE else copy.black_pieces
        for pc in pieces:
            if pc.is_king:
                king = pc

        remove_from_valid = []
        # make sure the king isn't moving into harms way
        for move in valid_moves:
            move_dict = copy.move_piece((self.row, self.col), move, False)
            if (king.row, king.col) in move_dict['board'].potential_next_moves():
                remove_from_valid.append(move)

        # remove those moves that would put king in check
        remove_from_valid = set(remove_from_valid)
        for move in remove_from_valid:
            if move in valid_moves:
                valid_moves.remove(move)

        return valid_moves

    def move(self, row, col, board):
        self.row = row
        self.col = col

    def get_team(self):
        return self.team

    def get_location(self):
        return self.row, self.col







