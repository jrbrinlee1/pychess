from Pieces import Piece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.King import King
from Pieces.Team import Team

ROW = 8
COL = 8
ROWS = range(0, ROW)
COLS = range(0, COL)


class Board:

    def __init__(self, board=None, white_pieces=[], black_pieces=[], moves_since_taken=0, prev_states={}):
        """
        Board object which represents the state of the chess board/game. If no
        arguments are provided to constructor, then a chess board with an initial
        state is built. Arguments can be provided when a copy of a current board
        is needed. Instance variables:
            self.board - (List[List] type representing the actual board)
            self.white_pieces - List
            self.black_pieces - List
            self.turn -
        :param board: List[List] type which contains row/columns of Piece objects
                      or False when there is no piece in that position.
        :param white_pieces: List of pieces that belong to the white team
        :param black_pieces: List of pieces that belong to the black team
        """
        self.board = board
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.moves_since_taken = moves_since_taken
        self.prev_states = prev_states
        if self.board is None:
            self.set_board_to_init_state()
        self.turn = Team.WHITE

    def set_board_to_init_state(self):
        """
        Method that sets self.board, self.white_pieces and self.black_pieces
         in their initial states. (i.e. no moves have been made)
        :return: None
        """
        black_back_row = [Rook(Team.BLACK, 0, 0), Knight(Team.BLACK, 0, 1), Bishop(Team.BLACK, 0, 2),
                          Queen(Team.BLACK, 0, 3), King(Team.BLACK, 0, 4), Bishop(Team.BLACK, 0, 5),
                          Knight(Team.BLACK, 0, 6), Rook(Team.BLACK, 0, 7)]
        white_back_row = [Rook(Team.WHITE, 7, 0), Knight(Team.WHITE, 7, 1), Bishop(Team.WHITE, 7, 2),
                          Queen(Team.WHITE, 7, 3), King(Team.WHITE, 7, 4), Bishop(Team.WHITE, 7, 5),
                          Knight(Team.WHITE, 7, 6), Rook(Team.WHITE, 7, 7)]

        board = [black_back_row]
        black_pawns = [Pawn(Team.BLACK, 1, i) for i in range(8)]
        board.append(black_pawns)
        for i in range(4):
            row = [False for j in range(8)]
            board.append(row)
        white_pawns = [Pawn(Team.WHITE, 6, i) for i in range(8)]
        board.append(white_pawns)
        board.append(white_back_row)

        self.board = board
        self.white_pieces = white_pawns[:] + white_back_row[:]
        self.black_pieces = black_pawns[:] + black_back_row[:]

    def move_piece(self, current_pos, next_pos, gui_move=False, ai=False):
        """
        Method that returns a copy of the current board with the piece on
        current_pos moved to next_pos. No error / valid move checking here.
        Valid move checking done a piece level.
        :param current_pos: position of piece you'd like to move
        :param next_pos: position you'd like to move th piece
        :param gui_move: True if move is being made on gui, False if it's being made in game logic
        :param ai: is ai making this move
        :return: {'board': copy of new board, 'game_over': bool, 'draw': bool, 'winner': Team.WHITE or Team.BLACK}
        """

        # copy board and retrieve the piece being moved along with it's data
        new_board = self.copy_board_object()
        return_dictionary = {'board': new_board, 'game_over': False, 'draw': False, 'winner': None}
        piece = new_board.get_board()[current_pos[0]][current_pos[1]]
        """
        if gui_move:
            print(f"Board:")
            new_board.print_board()
            print(f"Piece: {piece}")
            print(f"current position: {current_pos[0], current_pos[1]}")
            print(f"destination position: {next_pos[0], next_pos[1]}")
        if not gui_move:
            print("SOME NONE GUI ACTION......")
            print()
            print(f"Board:")
            new_board.print_board()
            print(f"Piece: {piece}")
            print(f"current position: {current_pos[0], current_pos[1]}")
            print(f"destination position: {next_pos[0], next_pos[1]}")
        """
        data = piece.move(next_pos[0], next_pos[1], new_board)
        new_board.moves_since_taken += 1
        castle = False

        # check for and make castle move
        if isinstance(piece, King) and data and gui_move:
            # update board
            castle = True
            row = 7 if piece.get_team() == Team.WHITE else 0
            king_col = 6 if next_pos[1] == 7 else 2
            rook_col = 5 if next_pos[1] == 7 else 3
            rook = new_board.get_board()[row][next_pos[1]]
            rook.move(row, rook_col, new_board)
            new_board.get_board()[row][king_col] = piece
            new_board.get_board()[row][rook_col] = rook
            new_board.get_board()[current_pos[0]][current_pos[1]] = False
            new_board.get_board()[next_pos[0]][next_pos[1]] = False

        if not castle:
            # non-castle move, make the move on the board.board
            destination_piece = new_board.board[next_pos[0]][next_pos[1]]
            new_board.board[current_pos[0]][current_pos[1]] = False
            new_board.board[next_pos[0]][next_pos[1]] = piece

            if destination_piece:
                new_board.update_teams_pieces()
                new_board.moves_since_taken = 0

            # Check for en_passant and pawn promotion
            if isinstance(piece, Pawn):
                if data[0]:  # if en passant
                    new_board.moves_since_taken = 0
                    new_board.board[next_pos[0] - piece.direction][next_pos[1]] = False
                if data[1] and gui_move:  # check if pawn promotion and gui move
                    new_board.execute_pawn_promotion(piece.get_team(), next_pos, ai)
        # endif not castle

        moving_team_pieces = new_board.white_pieces if piece.get_team() == Team.WHITE else new_board.black_pieces
        for pc in moving_team_pieces:
            if isinstance(pc, Pawn) and pc is not piece:
                pc.en_passant_move = []
                pc.just_moved_two = False

        # check for threefold rule
        three_fold_bool = False
        if gui_move:
            three_fold_bool = new_board.add_state_check_threefold()

        # was there 50 moves made without a piece being taken or third instance of game board, then game over and draw
        if new_board.moves_since_taken >= 50 or three_fold_bool:
            return_dictionary['game_over'] = True
            return_dictionary['draw'] = True

        # change turns
        new_board.turn = Team.BLACK if piece.get_team() == Team.WHITE else Team.WHITE

        # update teams pcs
        new_board.update_teams_pieces()

        """
        # check mate or draw?
        if gui_move:
            pcs = self.white_pieces if new_board.turn == Team.WHITE else self.black_pieces
            moves = []
            check = False
            for pc in pcs:
                moves = moves + pc.get_valid_moves(new_board, False)
                moves = pc.king_in_harms_way(new_board, moves)
                if isinstance(pc, King):
                    if pc.in_check(new_board, (pc.row, pc.col)):
                        check = True
            if len(moves) == 0:
                return_dictionary['game_over'] = True
                if check:
                    return_dictionary['draw'] = False
                    return_dictionary['winner'] = 'white team' if new_board.turn == Team.BLACK else 'black team'
                else:
                    return_dictionary['draw'] = True
        """

        return return_dictionary

    def update_teams_pieces(self):
        self.white_pieces = []
        self.black_pieces = []
        # if we get to pawn that wasn't just moved, update en_passant_data
        for row in ROWS:
            for col in COLS:
                pc = self.board[row][col]
                if pc:
                    # pc.move(row, col)
                    if pc.get_team() == Team.WHITE:
                        self.white_pieces.append(pc)
                    else:
                        self.black_pieces.append(pc)

    def add_state_check_threefold(self):
        # get state of the board as string tuple
        state = self.create_state_tuple()
        # if we've seen the state before, increment count
        if state in self.prev_states.keys():
            count = self.prev_states[state]
            count = count + 1
            # if we've seen this state three times, then threefold rule says draw
            if count == 3:
                return True
            else:
                self.prev_states[state] = count
        else:
            self.prev_states[state] = 1

        return False

    def execute_pawn_promotion(self, team, next_pos, ai):
        if not ai:
            print(f"1 - Queen\n2 - Bishop\n3 - Rook\n4 - Knight\n5 - Pawn\nWhat promotion would you like to make: ")
            inp = input()

            new_pc = Pawn(team, next_pos[0], next_pos[1])
            if inp == "1":
                new_pc = Queen(team, next_pos[0], next_pos[1])
            elif inp == "2":
                new_pc = Bishop(team, next_pos[0], next_pos[1])
            elif inp == "3":
                new_pc = Rook(team, next_pos[0], next_pos[1])
            elif inp == "4":
                new_pc = Knight(team, next_pos[0], next_pos[1])

        else:
            new_pc = Queen(team, next_pos[0], next_pos[1])

        old_pc = self.get_board()[next_pos[0]][next_pos[1]]
        self.get_board()[next_pos[0]][next_pos[1]] = new_pc

        if team == Team.WHITE:
            self.white_pieces.remove(old_pc)
            self.white_pieces.append(new_pc)
        else:
            self.black_pieces.remove(old_pc)
            self.black_pieces.append(new_pc)

    def copy_board_object(self):
        """
        :return: deep copy of a board object (self)
        """
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

        return Board(new_board, new_white_pieces, new_black_pieces, self.moves_since_taken, self.prev_states)

    def let_AI_move(self):
        white = True if self.team_turn() == Team.WHITE else False
        best_move, _, _ = self.max_value(white, 4, float('-inf'), float('inf'))
        move = self.move_piece(best_move[0], best_move[1], True, True)
        print(f"AI has returned the best move for white:{white} - {best_move[0]} to {best_move[1]}...")
        return move

    def get_successors(self, white):
        piece_set = self.white_pieces if white else self.black_pieces
        for pc in piece_set:
            for move in pc.get_valid_moves(self):
                move_dict = self.move_piece(pc.get_location(), move, False, True)
                yield (pc.get_location(), move), move_dict['board']

    def get_utility(self, white):
        utility = 0
        max_pieces = self.white_pieces if white else self.black_pieces
        min_pieces = self.black_pieces if white else self.white_pieces
        for pc in max_pieces:
            utility += self.score(pc)
        for pc in min_pieces:
            utility -= self.score(pc)
        return utility

    def max_value(self, white, limit, alpha, beta):
        utility = self.get_utility(white)
        v = float('-inf')
        count = 0
        leaf = 0

        if limit == 0:
            return None, utility, 1

        for successor in self.get_successors(white):
            min_child_node = successor[1].min_value(white, limit - 1, alpha, beta)
            v2 = min_child_node[1]
            leaf += min_child_node[2]
            if v2 > v:
                v = v2
                best_move = successor[0]
            if v >= beta:
                return best_move, v, leaf
            if v > alpha:
                alpha = v
            count += 1

        if count == 0:
            return None, utility, 1
        else:
            return best_move, v, leaf

    def min_value(self, white, limit, alpha, beta):
        utility = self.get_utility(white)
        v = float('inf')
        count = 0
        leaf = 0

        if limit == 0:
            return None, utility, 1

        for successor in self.get_successors(not white):
            min_child_node = successor[1].max_value(white, limit - 1, alpha, beta)
            v2 = min_child_node[1]
            leaf += min_child_node[2]
            if v2 < v:
                v = v2
                best_move = successor[0]
            if v <= alpha:
                return best_move, v, leaf
            if v < beta:
                beta = v
            count += 1

        if count == 0:
            return None, utility, 1
        else:
            return best_move, v, leaf

    def get_team_pieces(self, team):
        if team == Team.WHITE:
            return self.white_pieces, self.black_pieces
        else:
            return self.black_pieces, self.white_pieces

    def score(self, pc):
        _ = self
        if isinstance(pc, King):
            return 100
        if isinstance(pc, Queen):
            return 20
        if isinstance(pc, Rook):
            return 8
        if isinstance(pc, Bishop):
            return 6
        if isinstance(pc, Knight):
            return 6
        if isinstance(pc, Pawn):
            return 1

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

    def create_state_tuple(self):
        state = []
        for i in range(len(self.board)):
            state_row = []
            for j in range(len(self.board[0])):
                piece = self.board[i][j]
                if not piece:
                    state_row.append('x')
                else:
                    string = ''
                    if isinstance(piece, King):
                        _, can_castle = piece.try_adding_castle(self, [])
                        if can_castle:
                            string = string + 'c'
                    if isinstance(piece, Pawn):
                        try:
                            piece.en_passant(self)
                            if len(piece.en_passant_move) != 0:
                                string = string + 'e'
                        except TypeError:
                            pass

                    string = string + 'W' if piece.get_team() == Team.WHITE else string + 'B'

                    string = string + str(piece)
                    state_row.append(string)
            state.append(state_row)

        tuple_representation = []
        for i in range(len(state)):
            row_as_tuple = tuple(state[i])
            tuple_representation.append(row_as_tuple)

        return tuple(tuple_representation)

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
        """
        :param row: row on the board
        :param col: col on the board
        :return: True when board[row][col] has piece on it. False when it doesn't. None when it's not a valid location.
        """
        if row < 0 or col < 0:
            return None
        try:
            return True if not self.board[row][col] else False
        except IndexError:
            return None

    def team_on(self, row, col):
        """
        :param row: row on the board
        :param col: col on the board
        :return: White when board[row][col] has a white piece on it, Black
                 when board[row][col] has a black piece on it, and None if
                 it's not a valid location.
        """
        try:
            ret = self.board[row][col].get_team()
        except IndexError:
            return None
        return ret

    def get_board(self):
        return self.board

    def team_turn(self):
        return self.turn

