import tkinter as tk
from tkinter.messagebox import showinfo
from Board.Board import Board
import sys
import PIL
from PIL import ImageTk, Image

WHITE_SPACE_COLOR = "white"
BLACK_SPACE_COLOR = "grey"
SELECTED_COLOR = "red"
VALID_MOVES_COLOR = "orange"
GUI_SPACE_WIDTH = 80
GUI_SPACE_HEIGHT = 80


class ClickTracker:
    def __init__(self):
        self.status = 0
        self.piece = None
        self.row = None
        self.col = None
        self.valid_moves = []

    def update(self, row, col, piece, valid_moves):
        self.status = 1 if self.status == 0 else 0
        self.piece = piece
        self.row = row
        self.col = col
        self.valid_moves = valid_moves

    def reset(self):
        self.status = 0
        self.piece = None
        self.row = None
        self.col = None
        self.valid_moves = []


class PyChess(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.blank_path = "Images/blank.png"
        self.master = master
        self.game_over = False
        self.draw = False
        self.winner = None
        self.click_tracker = ClickTracker()
        self.board = Board()
        self.board_map = []
        self.create_board_display()

        self.pack()

    def on_click(self, i, j):
        space_is_empty = self.board.is_space_empty(i, j)
        team_on_space = self.board.team_on(i, j) if not space_is_empty else None

        # no piece currently highlighted / clicked on
        if self.click_tracker.status == 0:
            if not space_is_empty:
                if self.board.team_turn() == team_on_space:
                    piece = self.board.get_board()[i][j]
                    self.board_map[i][j]['bg'] = SELECTED_COLOR
                    self.click_tracker.update(i, j, piece, piece.get_valid_moves(self.board))
                    self.highlight_valid_moves(self.click_tracker.valid_moves)
        # piece is currently highlighted / clicked on
        elif self.click_tracker.status == 1:
            # if player clicked on same piece that is highlighted, unhighlight it
            if self.click_tracker.row == i and self.click_tracker.col == j:
                self.reset_board_map_color()
                self.click_tracker.reset()
            # else, if they click on a valid move, make the move and update accordingly
            elif (i, j) in self.click_tracker.valid_moves:
                # move piece on the board object
                move_dict = self.board.move_piece((self.click_tracker.row, self.click_tracker.col), (i, j), True, False)
                self.board = move_dict['board']
                self.game_over = move_dict['game_over']
                self.draw = move_dict['draw']
                self.winner = move_dict['winner']
                # update the board_map data structure
                self.reset_board_map_color()
                self.reset_board_map_images()
                # finally, reset the click tracker
                self.click_tracker.reset()

            if self.game_over:
                if self.draw:
                    showinfo("tk", f"The game ends in a draw!")
                else:
                    showinfo("tk", f"The {self.winner} wins!")
                self.master.destroy()

    def let_AI_move(self):
        print("Letting AI move...")

        move_dict = self.board.let_AI_move()
        self.board = move_dict['board']
        self.game_over = move_dict['game_over']
        self.draw = move_dict['draw']
        self.winner = move_dict['winner']
        # update the board_map data structure
        self.reset_board_map_color()
        self.reset_board_map_images()
        # finally, reset the click tracker
        self.click_tracker.reset()

        if self.game_over:
            if self.draw:
                showinfo("tk", f"The game ends in a draw!")
            else:
                showinfo("tk", f"The {self.winner} wins!")
            self.master.destroy()

    def highlight_valid_moves(self, moves):
        for move in moves:
            self.board_map[move[0]][move[1]]['bg'] = VALID_MOVES_COLOR

    def reset_board_map_color(self):
        rows = len(self.board.get_board())
        cols = len(self.board.get_board()[0])

        for i in range(rows):
            for j in range(cols):
                color = BLACK_SPACE_COLOR if (i + j) % 2 == 1 else WHITE_SPACE_COLOR
                self.board_map[i][j]['bg'] = color

    def reset_board_map_images(self):
        rows = len(self.board.get_board())
        cols = len(self.board.get_board()[0])

        for i in range(rows):
            for j in range(cols):
                path = self.board.board[i][j].image_path if not self.board.is_space_empty(i, j) else self.blank_path
                image = PIL.Image.open(path)
                img = ImageTk.PhotoImage(image)
                self.board_map[i][j]['image'] = img
                self.board_map[i][j].image = img

    def create_board_display(self):
        rows = len(self.board.get_board())
        cols = len(self.board.get_board()[0])

        # create data structure to hold labels
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(None)
            self.board_map.append(row)

        # create labels and store in data structure
        for i in range(rows):
            for j in range(cols):
                color = BLACK_SPACE_COLOR if (i + j) % 2 == 1 else WHITE_SPACE_COLOR
                path = self.board.board[i][j].image_path if not self.board.is_space_empty(i, j) else self.blank_path
                image = PIL.Image.open(path)
                img = ImageTk.PhotoImage(image)
                label = tk.Label(self, image=img, bg=color, height=GUI_SPACE_HEIGHT, width=GUI_SPACE_WIDTH)
                label.image = img
                self.board_map[i][j] = label
                label.grid(row=i, column=j)
                label.bind('<Button-1>', lambda e, x=i, y=j: self.on_click(x, y))

        # bind enter to let AI move
        self.bind("<Return>", lambda event: self.let_AI_move())
        self.focus_set()


class FullGUI(tk.Frame):
    pass


def Run(ai=False):
    chess_root = tk.Tk()
    app = PyChess(master=chess_root)
    if ai:
        while True:
            #try:
            app.let_AI_move()
            #except AttributeError:
            #    print("having trouble with ai")
            #    inp = input()
            app.update_idletasks()
            app.update()
    else:
        app.mainloop()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        Run(True)
    else:
        Run()
