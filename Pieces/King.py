from Pieces.Piece import Piece
from Pieces.Team import Team
from Pieces.Rook import Rook


class King(Piece):

    def __init__(self, team, row, col,  init_position=True):
        """
        King class that represents a king piece. Inherits from Piece class
        :param team: Team.WHITE or Team.BLACK
        :param row: current row the piece is in
        :param col: current column the piece is in
        :param init_position: True if the piece hasn't been moved, False otherwise
        """
        super().__init__(team, row, col)
        self.image_path = "Images/bK.png" if self.team == Team.BLACK else "Images/wK.png"
        self.move_options = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        self.init_position = init_position
        self.is_king = True

    def get_valid_moves(self, board, current_move=True):
        """
        Method used to get the valid move for the king
        :param board: current board object
        :param current_move: True to make sure king isn't moving into check, false otherwise
        :return: list of valid moves for current king
        """
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

        valid_moves = self.try_adding_castle(board, valid_moves)[0]
        valid_moves = self.harms_way(board, valid_moves)

        return valid_moves

    def try_adding_castle(self, board, valid_moves):
        """
        Method to add the castle move to the kings valid move list if the castle move is available
        :param board: current board object
        :param valid_moves: current list of valid moves
        :return: updated list of moves (may or may not contain the castle move)
        """
        can_castle = False

        # cannot castle in check or if king has already moved
        if self.in_check(board, (self.row, self.col)):
            return valid_moves, can_castle
        if not self.init_position:
            return valid_moves, can_castle

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
                        can_castle = True

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
                        can_castle = True

        return valid_moves, can_castle

    def in_check(self, board, location):
        """
        Method to determine if location[0], location[1] would cause the king to be in check
        :param board: the current board object
        :param location: (row, column) tuple where we want to determine check (usually just the location of king)
        :return: True if (row, column) would be check, otherwise False
        """
        change_team = Team.WHITE if self.team == Team.BLACK else Team.BLACK
        board.turn = change_team
        if (location[0], location[1]) in board.potential_next_moves():
            board.turn = self.team
            return True
        else:
            board.turn = self.team
            return False

    def move(self, row, col, board):
        """
        Updates the location details of current king piece (self.row and self.col)
        :param row: destination row
        :param col: destination column
        :return: True if the move was a castle, False otherwise
        """
        castle = False

        # if king is in original position and gets move coordinates below, then it was a castle move
        # move accordingly and update the castle boolean
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
        """
        :return: string representation of a king
        """
        return " K "

    def copy(self):
        """
        :return: copy of the current king piece
        """
        return King(self.team, self.row, self.col, self.init_position)

    def harms_way(self, board, valid_moves):
        """
        Used to remove moves from kings valid moves list that put him in check
        :param board: current board
        :param valid_moves: current set of valid moves
        :return: update list of valid moves
        """
        remove_from_valid = []
        # make sure the king isn't moving into harms way
        for move in valid_moves:
            move_dict = board.move_piece((self.row, self.col), move)
            if move in move_dict['board'].potential_next_moves():
                remove_from_valid.append(move)

        # remove the moves that would lead to being in check
        remove_from_valid = set(remove_from_valid)
        for move in remove_from_valid:
            if move in valid_moves:
                valid_moves.remove(move)

        return valid_moves

