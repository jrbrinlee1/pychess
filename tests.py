import unittest
from Board.Board import Board
from Pieces.Pawn import Pawn
from Pieces.Queen import Queen


class TestPawn(unittest.TestCase):
    """
    Testing Pawn Class:
     - get_valid_moves(board)
       1 - check moves for left most, right most, and a middle pawn for black and white team with board in initial state
       2 - make sure black and white move in the right direction when not in the initial position
       3 - check black and white pawns cannot move forward with piece (opponent/same team) is in front of it
       4 - check black and white pawns can attack left, right, and both if opponents players are there
       5 - check white pawns cannot move if it leave king check and check white pawns can move if king
           is in check but pawn jump in the path of the threatening player
       6 -
    """

    def test_get_valid_moves_1(self):
        """
        Test to make sure we get valid moves on initial board
        for both teams (should be one and two spots forward for all pieces)
        :return: test results
        """
        board = Board()
        left_most_white_pawn = board.board[6][0]
        middle_white_pawn = board.board[6][3]
        right_most_white_pawn = board.board[6][7]

        left_most_black_pawn = board.board[1][0]
        middle_black_pawn = board.board[1][3]
        right_most_black_pawn = board.board[1][7]

        # first, make sure we have pawns
        self.assertIsInstance(left_most_white_pawn, Pawn)
        self.assertIsInstance(middle_white_pawn, Pawn)
        self.assertIsInstance(right_most_white_pawn, Pawn)

        self.assertIsInstance(left_most_black_pawn, Pawn)
        self.assertIsInstance(middle_black_pawn, Pawn)
        self.assertIsInstance(right_most_black_pawn, Pawn)

        # initial move so they should all be able to move to two unique places
        self.assertEqual(len(left_most_white_pawn.get_valid_moves(board)), 2)
        self.assertEqual(len(middle_white_pawn.get_valid_moves(board)), 2)
        self.assertEqual(len(right_most_white_pawn.get_valid_moves(board)), 2)

        self.assertEqual(len(left_most_black_pawn.get_valid_moves(board)), 2)
        self.assertEqual(len(middle_black_pawn.get_valid_moves(board)), 2)
        self.assertEqual(len(right_most_black_pawn.get_valid_moves(board)), 2)

        # those unique spaces should be as follows
        for move in left_most_white_pawn.get_valid_moves(board):
            actual = [(5, 0), (4, 0)]
            self.assertIn(move, actual)

        for move in middle_white_pawn.get_valid_moves(board):
            actual = [(5, 3), (4, 3)]
            self.assertIn(move, actual)

        for move in right_most_white_pawn.get_valid_moves(board):
            actual = [(5, 7), (4, 7)]
            self.assertIn(move, actual)

        for move in left_most_black_pawn.get_valid_moves(board):
            actual = [(2, 0), (3, 0)]
            self.assertIn(move, actual)

        for move in middle_black_pawn.get_valid_moves(board):
            actual = [(2, 3), (3, 3)]
            self.assertIn(move, actual)

        for move in right_most_black_pawn.get_valid_moves(board):
            actual = [(2, 7), (3, 7)]
            self.assertIn(move, actual)

    def test_get_valid_moves_2(self):
        """
        Test to make sure we get valid moves when off initial
        state and not by other pieces for both teams (should be just one move forward)
        :return:
        """
        board = Board()
        # move left most white pawn and a middle white pawn
        board = board.move_piece((6, 0), (4, 0))[0]
        board = board.move_piece((6, 2), (4, 2))[0]
        # move right most black pawn and a middle black pawn
        board = board.move_piece((1, 7), (3, 7))[0]
        board = board.move_piece((1, 5), (3, 5))[0]

        # get those pieces at new locations
        left_most_white_pawn = board.board[4][0]
        middle_white_pawn = board.board[4][2]

        middle_black_pawn = board.board[3][5]
        right_most_black_pawn = board.board[3][7]

        # make sure we've got the pawns
        self.assertIsInstance(left_most_white_pawn, Pawn)
        self.assertIsInstance(middle_white_pawn, Pawn)

        self.assertIsInstance(middle_black_pawn, Pawn)
        self.assertIsInstance(right_most_black_pawn, Pawn)

        # they should now only be able to move one space
        self.assertEqual(len(left_most_white_pawn.get_valid_moves(board)), 1)
        self.assertEqual(len(middle_white_pawn.get_valid_moves(board)), 1)

        self.assertEqual(len(middle_black_pawn.get_valid_moves(board)), 1)
        self.assertEqual(len(right_most_black_pawn.get_valid_moves(board)), 1)

        # those spaces should be as follows
        self.assertEqual(left_most_white_pawn.get_valid_moves(board)[0], (3, 0))
        self.assertEqual(middle_white_pawn.get_valid_moves(board)[0], (3, 2))

        self.assertEqual(middle_black_pawn.get_valid_moves(board)[0], (4, 5))
        self.assertEqual(right_most_black_pawn.get_valid_moves(board)[0], (4, 7))

    def test_get_valid_moves_3(self):
        """
        Test to make sure we get no moves when we have
        no moves to make (other opponent in the way of forward move, no attack moves and
        players own team in front with no attacking move)
        :return:
        """
        board = Board()
        # move white and black pawn in column 4 forward two spaces
        board = board.move_piece((6, 4), (4, 4))[0]
        board = board.move_piece((1, 4), (3, 4))[0]

        # get those pieces we just moved
        middle_white_pawn = board.board[4][4]
        middle_black_pawn = board.board[3][4]

        # make sure we've got the pawns
        self.assertIsInstance(middle_white_pawn, Pawn)
        self.assertIsInstance(middle_black_pawn, Pawn)

        # they should not be able to move
        self.assertEqual(len(middle_white_pawn.get_valid_moves(board)), 0)
        self.assertEqual(len(middle_black_pawn.get_valid_moves(board)), 0)

        # now check to make sure it cannot move into it's own team (one space in front and to in front on initial pos)
        board = Board()
        # move white pawns one and two places in front of other white pawns
        board = board.move_piece((6, 0), (5, 1))[0]
        board = board.move_piece((6, 2), (4, 3))[0]

        # get the pawns behind them
        white_pawn_1 = board.board[6][1]
        white_pawn_2 = board.board[6][3]

        # make sure we've got the pawns
        self.assertIsInstance(white_pawn_1, Pawn)
        self.assertIsInstance(white_pawn_2, Pawn)

        # 1 shouldn't be able to move, 2 should only be able to move 1 space
        self.assertEqual(len(white_pawn_1.get_valid_moves(board)), 0)
        self.assertEqual(len(white_pawn_2.get_valid_moves(board)), 1)

    def test_get_valid_moves_4(self):
        """
        first move like this:
                        black_pawn
            white_pawn
        check that both can move forward and attack

        then move like this:
            black_pawn              black_pawn
                        white_pawn
        check that white pawn has three moves

        then move like this:
                        black_pawn              black_pawn
            white_pawn              white_pawn
        check that black pawn has three moves
        :return:
        """
        board = Board()

        board = Board()
        # move white in column 5 and black pawn in column 5 forward two spaces
        board = board.move_piece((6, 4), (4, 4))[0]
        board = board.move_piece((1, 5), (3, 5))[0]

        # get those pieces we just moved
        middle_white_pawn = board.board[4][4]
        right_black_pawn = board.board[3][5]

        # make sure we've got the pawns
        self.assertIsInstance(middle_white_pawn, Pawn)
        self.assertIsInstance(right_black_pawn, Pawn)

        # they should be able to attack and move forward
        self.assertEqual(len(middle_white_pawn.get_valid_moves(board)), 2)
        self.assertEqual(len(right_black_pawn.get_valid_moves(board)), 2)

        for move in middle_white_pawn.get_valid_moves(board):
            actual = [(3, 4), (3, 5)]
            self.assertIn(move, actual)

        for move in right_black_pawn.get_valid_moves(board):
            actual = [(4, 4), (4, 5)]
            self.assertIn(move, actual)

        # now move other black pawn to the left of white pawn up two spaces
        board = board.move_piece((1, 3), (3, 3))[0]

        # get that pawn
        left_black_pawn = board.board[3][3]

        # verify it's a pawn
        self.assertIsInstance(left_black_pawn, Pawn)

        # white pawn should have 3 moves now
        self.assertEqual(len(middle_white_pawn.get_valid_moves(board)), 3)

        # the moves should be as follows
        for move in middle_white_pawn.get_valid_moves(board):
            actual = [(3, 3), (3, 4), (3, 5)]
            self.assertIn(move, actual)

        # now move other white pawn to the left of the black pawn we just move up two spaces
        board = board.move_piece((6, 2), (4, 2))[0]

        # get that pawn
        left_white_pawn = board.board[4][2]

        # verify it's a pawn
        self.assertIsInstance(left_white_pawn, Pawn)

        # black pawn should have 3 moves now (two attack and one forward)
        self.assertEqual(len(left_black_pawn.get_valid_moves(board)), 3)

        # the moves should be as follows
        for move in left_black_pawn.get_valid_moves(board):
            actual = [(4, 2), (4, 3), (4, 4)]
            self.assertIn(move, actual)

    def test_get_valid_moves_5(self):
        """
        Test to make sure pawn cannot move if it leaves king in position it can be
        taken

        :return:
        """

        board = Board()
        # white pawn in front of king up two, move black queen to check the king
        board = board.move_piece((6, 3), (4, 3))[0]
        board = board.move_piece((0, 3), (3, 0))[0]

        # get the queen and verify it's the queen
        black_queen = board.board[3][0]
        self.assertIsInstance(black_queen, Queen)

        # get white pawn on the far left in initial position, verify it is a pawn
        left_white_pawn = board.board[6][0]
        self.assertIsInstance(left_white_pawn, Pawn)
        # get moves, should be none since it would leave the king in check
        self.assertEqual(len(left_white_pawn.get_valid_moves(board)), 0)

        # get white pawn on top of bishop and verify it's a pawn
        left_white_pawn_1 = board.board[6][2]
        self.assertIsInstance(left_white_pawn_1, Pawn)
        # get moves, should be one hop in front to block the queen
        self.assertEqual(len(left_white_pawn_1.get_valid_moves(board)), 1)
        self.assertEqual(left_white_pawn_1.get_valid_moves(board)[0], (5, 2))

        # get white pawn on top of bishop and verify it's a pawn
        left_white_pawn_2 = board.board[6][1]
        self.assertIsInstance(left_white_pawn_2, Pawn)
        # get moves, should be one hop in front to block the queen
        self.assertEqual(len(left_white_pawn_2.get_valid_moves(board)), 1)
        self.assertEqual(left_white_pawn_2.get_valid_moves(board)[0], (4, 1))

    def test_get_valid_moves_6(self):
        pass

    def test_get_attack_moves(self):
        """
        get_attack_moves specific to pawns
        """
        pass


#class TestRook(unittest.TestCase):





if __name__ == '__main__':
    unittest.main()
