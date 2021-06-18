from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.King import King
from Pieces.Team import Team


class Board:

    def __init__(self, board=None, white_pieces=[], black_pieces=[]):
        self.board = board
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        if self.board is None:
            self.set_board_to_init_state()
        self.turn = Team.WHITE
        self.white_king = None
        self.black_king = None
        for pc in self.white_pieces:
            if isinstance(pc, King):
                self.white_king = pc
        for pc in self.black_pieces:
            if isinstance(pc, King):
                self.black_king = pc

        self.is_black_in_check = False
        self.is_white_in_check = False

    def set_board_to_init_state(self):

        black_back_row = [Rook(Team.BLACK, 0, 0), Knight(Team.BLACK, 0, 1), Bishop(Team.BLACK, 0, 2),
                          Queen(Team.BLACK, 0, 3), King(Team.BLACK, 0, 4), Bishop(Team.BLACK, 0, 5),
                          Knight(Team.BLACK, 0, 6), Rook(Team.BLACK, 0, 7)]
        board = [black_back_row]

        black_pawns = []
        for i in range(8):
            black_pawns.append(Pawn(Team.BLACK, 1, i))
        board.append(black_pawns)

        for i in range(4):
            row = []
            for j in range(8):
                row.append(False)
            board.append(row)
        white_pawns = []
        for i in range(8):
            white_pawns.append(Pawn(Team.WHITE, 6, i))
        board.append(white_pawns)

        white_back_pieces = [Rook(Team.WHITE, 7, 0), Knight(Team.WHITE, 7, 1), Bishop(Team.WHITE, 7, 2),
                             Queen(Team.WHITE, 7, 3), King(Team.WHITE, 7, 4), Bishop(Team.WHITE, 7, 5),
                             Knight(Team.WHITE, 7, 6), Rook(Team.WHITE, 7, 7)]
        board.append(white_back_pieces)

        self.board = board

        self.white_pieces = white_pawns[:]
        for pc in white_back_pieces:
            self.white_pieces.append(pc)
        self.black_pieces = black_back_row[:]
        for pc in black_pawns:
            self.black_pieces.append(pc)

    def print_board(self):
        for i in range(8):
            for j in range(8):
                print(" ", end="")
                if not self.board[i][j]:
                    print("[ ]", end="")
                else:
                    print(self.board[i][j], end="")
                if j == 7:
                    print()

    def is_space_empty(self, row, col):
        if row < 0 or col < 0:
            return None

        try:
            return True if not self.board[row][col] else False
        except IndexError:
            return None

    def team_on(self, row, col):
        try:
            ret = self.board[row][col].get_team()
        except IndexError:
            return None
        return ret

    def get_board(self):
        return self.board

    def team_turn(self):
        return self.turn

    def move_piece(self, current, next):
        """
        Method that returns a copy of the current board with the piece on
        current moved to next.
        :param current: position of piece you'd like to move
        :param next: position you'd like to move th piece
        :return: Copy of the current board with specified move made
        """
        fatal = False
        new_board = self.copy_board_object()
        piece = new_board.get_board()[current[0]][current[1]]
        destination_piece = new_board.board[next[0]][next[1]]
        new_board.board[current[0]][current[1]] = False
        new_board.board[next[0]][next[1]] = piece
        piece.move(next[0], next[1])
        if piece.get_team() == Team.WHITE:
            if destination_piece:
                new_board.black_pieces.remove(destination_piece)
            new_board.turn = Team.BLACK
        else:
            if destination_piece:
                new_board.white_pieces.remove(destination_piece)
            new_board.turn = Team.WHITE

        if isinstance(destination_piece, King):
            fatal = True

        return new_board, fatal

    def copy_board_object(self):
        new_board = []
        new_white_pieces = []
        new_black_pieces = []
        for i in range(len(self.board)):
            row = []
            for j in range(len(self.board[0])):
                if self.board[i][j]:
                    copy = self.board[i][j].copy()
                    row.append(copy)
                    if copy.get_team() == Team.WHITE:
                        new_white_pieces.append(copy)
                    else:
                        new_black_pieces.append(copy)
                else:
                    row.append(False)
            new_board.append(row)

        return Board(new_board, new_white_pieces, new_black_pieces)

    def potential_next_moves(self):
        moves = []
        if self.turn == Team.WHITE:
            piece_set = self.white_pieces
        else:
            piece_set = self.black_pieces

        for pc in piece_set:
            if isinstance(pc, King):
                for move in pc.move_options:
                    moves.append((pc.row + move[0], pc.col + move[1]))
            elif isinstance(pc, Pawn):
                moves = moves + pc.get_attack_moves()
            else:
                moves = moves + pc.get_valid_moves(self, False)

        return moves
