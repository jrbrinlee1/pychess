from Pieces.Team import Team
from Pieces.Piece import Piece


class Pawn(Piece):

    def __init__(self, team, row, col, init_position=True, just_moved_two=False, en_passant_move=[]):
        super().__init__(team, row, col)
        self.image_path = "Images/bP.png" if self.team == Team.BLACK else "Images/wP.png"
        self.init_position = init_position
        self.just_moved_two = just_moved_two
        self.direction = 1 if self.team == Team.BLACK else -1
        self.en_passant_move = en_passant_move

    def get_valid_moves(self, board, current_move=True):
        """
        Method used to get the valid move for the pawn
        :param board: current board object
        :param current_move: True to remove moves from list if king will be in check, false otherwise
        :return: list of valid moves for current pawn
        """

        valid_moves = []
        attack_forward_one_empty = board.is_space_empty(self.row + self.direction, self.col)
        attack_forward_two_empty = board.is_space_empty(self.row + 2 * self.direction, self.col)
        attack_right_empty = board.is_space_empty(self.row + self.direction, self.col + 1)
        attack_left_empty = board.is_space_empty(self.row + self.direction, self.col - 1)

        # if board location is False/Empty - non attacking moves
        if attack_forward_one_empty:
            valid_moves.append((self.row + self.direction, self.col))
            if attack_forward_two_empty:
                if self.init_position:
                    valid_moves.append((self.row + 2 * self.direction, self.col))

        # if board location is not Emtpy and is filled with other team - attacking moves
        if not attack_right_empty and attack_right_empty is not None:
            if board.board[self.row + self.direction][self.col + 1].get_team() != self.team:
                valid_moves.append((self.row + self.direction, self.col + 1))

        if not attack_left_empty and attack_left_empty is not None:
            if board.board[self.row + self.direction][self.col - 1].get_team() != self.team:
                valid_moves.append((self.row + self.direction, self.col - 1))

        self.en_passant(board)
        valid_moves = valid_moves + self.en_passant_move

        if current_move:
            valid_moves = self.king_in_harms_way(board, valid_moves)

        return valid_moves

    def __str__(self):
        """
        :return: string representation of a pawn
        """
        return " P "

    def copy(self):
        """
        :return: copy of the current pawn piece
        """
        return Pawn(self.team, self.row, self.col, self.init_position, self.just_moved_two, self.en_passant_move)

    def get_attack_moves(self):
        """
        :return: Returns forward diagonals of current pawns location [( , ), ( , )]
        """
        return [(self.row + self.direction, self.col + 1), (self.row + self.direction, self.col - 1)]

    def move(self, row, col, board):
        """
        Updates the location details of current pawn piece (self.row and self.col) and updates self.init_position to
        show that the pawn has been moved. Also keeps track of if the pawn was just moved two spaces (it could be
        captured en passant). Finally, checks and returns whether move was en passant or pawn promotion.
        :param row: destination row
        :param col: destination column
        :param board: board
        :return: (en passant move (True/False), pawn promotion (True/False)
        """
        # store information - pawn has been moved and if it was moved 2 spaces (could be captured en passant)
        self.init_position = False
        if abs(self.row - row) == 2:
            self.just_moved_two = True
        else:
            self.just_moved_two = False

        # was the move an en passant move
        ret = [False, False]
        self.en_passant(board)
        if (row, col) in self.en_passant_move:
            ret[0] = True

        # updates it's location
        self.row = row
        self.col = col

        # is the move a pawn promotion
        if self.team == Team.WHITE and row == 0:
            ret[1] = True
        elif self.team == Team.BLACK and row == 7:
            ret[1] = True

        return ret

    def en_passant(self, board):
        """
        Method check the current pawn on the board and returns valid en passant moves
        :param board: current board object
        :return: List[Tuples] which represent en passant moves
        """
        # spaces to the left and right of pawn
        left = (self.row, self.col - 1)
        right = (self.row, self.col + 1)
        # are those spaces empty
        is_piece_left = board.is_space_empty(left[0], left[1])
        is_piece_right = board.is_space_empty(right[0], right[1])

        attack_moves = []

        if not is_piece_left and is_piece_left is not None:
            pc = board.get_board()[left[0]][left[1]]
            if pc.team != self.team:
                if isinstance(pc, Pawn):
                    if pc.just_moved_two:
                        attack_moves.append((self.row + self.direction, self.col - 1))

        if not is_piece_right and is_piece_right is not None:
            pc = board.get_board()[right[0]][right[1]]
            if pc.team != self.team:
                if isinstance(pc, Pawn):
                    if pc.just_moved_two:
                        attack_moves.append((self.row + self.direction, self.col + 1))

        self.en_passant_move = attack_moves


