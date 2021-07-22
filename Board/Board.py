from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.King import King
from Pieces.Team import Team


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
            self.white_king -
            self.black_king -
            self.is_black_in_check -
            self.is_white_in_check -
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
        """
        Method that sets self.board, self.white_pieces and self.black_pieces
         in their initial states. (i.e. no moves have been made)
        :return: None
        """

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
        """
        :param row: row on the board
        :param col: col on the board
        :return: True when board[row][col] has a piece on it. False otherwise.
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
                 there is no piece at that location.
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

    def move_piece(self, current_pos, next_pos, gui_move=False, ai=False):
        """
        Method that returns a copy of the current board with the piece on
        current_pos moved to next_pos. No error / valid move checking here.
        Valid move checking done a piece level.
        :param check_promotion:
        :param current_pos: position of piece you'd like to move
        :param next_pos: position you'd like to move th piece
        :param ai: is ai making this move
        :return: {'board': copy of new board, 'game_over': bool, 'draw': bool, 'winner': Team.WHITE or Team.BLACK}
        """

        # copy board and retrieve the piece being moved along with it's data
        new_board = self.copy_board_object()
        return_dictionary = {'board': new_board, 'game_over': False, 'draw': False, 'winner': None}
        piece = new_board.get_board()[current_pos[0]][current_pos[1]]
        data = piece.move(next_pos[0], next_pos[1])
        new_board.moves_since_taken += 1

        # check for and make castle move
        if isinstance(piece, King):
            if data:
                new_board.get_board()[current_pos[0]][current_pos[1]] = False
                if piece.get_team() == Team.WHITE:
                    row = 7
                else:
                    row = 0

                if next_pos[1] == 7:
                    new_board.get_board()[row][6] = piece
                    new_board.get_board()[row][5] = new_board.get_board()[row][7]
                    new_board.get_board()[row][5].move(row, 5)
                    new_board.get_board()[7][7] = False
                else:
                    new_board.get_board()[row][2] = piece
                    new_board.get_board()[row][3] = new_board.get_board()[row][0]
                    new_board.get_board()[row][3].move(row, 3)
                    new_board.get_board()[row][0] = False

                new_board.turn = Team.BLACK if piece.get_team() == Team.WHITE else Team.WHITE

                three_fold_bool = False
                if gui_move:
                    three_fold_bool = new_board.add_state_check_threefold()

                if three_fold_bool:
                    return_dictionary['game_over'] = True
                    return_dictionary['draw'] = True

                return return_dictionary

        # non-castle move, make the move on the board.board
        destination_piece = new_board.board[next_pos[0]][next_pos[1]]
        new_board.board[current_pos[0]][current_pos[1]] = False
        new_board.board[next_pos[0]][next_pos[1]] = piece

        # if a piece was taken, remove it from the set of pieces
        if piece.get_team() == Team.WHITE:
            moving_team_pieces = new_board.white_pieces
            opponents_pieces = new_board.black_pieces
            new_board.turn = Team.BLACK
        else:
            moving_team_pieces = new_board.black_pieces
            opponents_pieces = new_board.white_pieces
            new_board.turn = Team.WHITE

        if destination_piece:
            opponents_pieces.remove(destination_piece)
            new_board.moves_since_taken = 0

        # Check for en_passant and pawn promotion
        en_passant = False
        promotion = False
        if isinstance(piece, Pawn):
            if data is not None:
                en_passant = data[0]
                promotion = data[1]
        if en_passant:
            opponents_pieces.remove(new_board.board[next_pos[0] + 1][next_pos[1]])
            new_board.moves_since_taken = 0
            new_board.board[next_pos[0] + 1][next_pos[1]] = False

        # if we get to pawn that wasn't just moved, update en_passant_data
        for pc in moving_team_pieces:
            if isinstance(pc, Pawn) and pc is not piece:
                pc.en_passant_move = []
                pc.just_moved_two = False

        # was king taken, then game over with winner
        if isinstance(destination_piece, King):
            winner = "black team" if self.board.turn == Team.WHITE else "white team"
            return_dictionary['game_over'] = True
            return_dictionary['winner'] = winner
            return return_dictionary

        three_fold_bool = False
        if gui_move:
            three_fold_bool = new_board.add_state_check_threefold()

        # was there 50 moves made without a piece being taken, then game over draw
        if new_board.moves_since_taken >= 50 or three_fold_bool:
            return_dictionary['game_over'] = True
            return_dictionary['draw'] = True
            return return_dictionary

        if promotion and gui_move:
            new_board.execute_pawn_promotion(piece.get_team(), next_pos, ai)

        new_board.turn = Team.BLACK if piece.get_team() == Team.WHITE else Team.WHITE

        return return_dictionary

    def add_state_check_threefold(self):
        state = self.create_state_tuple()
        if state in self.prev_states.keys():
            count = self.prev_states[state]
            count = count + 1
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
        white = True if self.team_turn() is Team.WHITE else False
        best_move, _, _ = self.max_value(white, 4, float('-inf'), float('inf'))
        move = self.move_piece(best_move[0], best_move[1], True, ai=True)
        print(f"AI has returned the best move - {best_move[0]} to {best_move[1]}...")
        return move

    def get_successors(self, white):

        if white:
            piece_set = self.white_pieces
        else:
            piece_set = self.black_pieces

        for pc in piece_set:
            for move in pc.get_valid_moves(self):
                temp_board, game_over = self.move_piece(pc.get_location(), move)
                yield (pc.get_location(), move), temp_board

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
