from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Toplevel
import numpy as np

BOARDS = ['debug', 'n00b', 'l33t', 'error']  # Available sudoku boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def __init__(self, parent, game):
        self.game = game
        # A frame is a “rectangular region on the screen”.
        Frame.__init__(self, parent)
        self.parent = parent

        # Initialization of row and col, which will take in the future the value of the mouse pointer
        self.row, self.col = -1, -1

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self,
                              text="Clear answers",
                              command=self.__clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        # <Button-1> is a mouse click
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        # <Key> will be the number pressed
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"
            # vertical lines
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            # horizontal lines
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    # Method that fill in the canvas with the predefined numbers. It is called every time the user inputs a number
    def __draw_puzzle(self):
        # First, we clear out any previous number
        self.canvas.delete("numbers")

        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j][0]
                status = self.game.puzzle[i][j][1]

                if answer != 0:
                    # coordinates of where we will place the number
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2

                    original = self.game.start_puzzle[i][j][0]

                    color = "black" if answer == original and status == "blocked_cell" else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __draw_cursor(self):  # highlights the particular cell that the user has clicked on
        self.canvas.delete("cursor")  # to clear out the previously highlighted cell.

        # We create a rectangle around the selected cell
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    def __cell_clicked(self, event):
        # if the flag game over is set to True, we don't do anything
        if self.game.game_over:
            return

        # Here, we have x and y (that are the coordinates of the event) that define row and col
        # self.row and self.col are the row and col of the sudoku game
        x, y = event.x, event.y
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
            # We need to take the lower bound integer (row and col are float)
            row, col = int(np.floor(row)), int(np.floor(col))

            # if cell was selected already (the value of self.row and self.col are already the same) - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col][0] >= 0 and self.game.puzzle[row][col][
                1] == "modifiable_cell":  # In the .sudoky files, the empty cells are filled in with 0
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):

        # If the game is over, no need to allow to enter an element
        if self.game.game_over:
            return

        if event.char == "":
            return

        if self.row >= 0 and self.col >= 0 and event.char in "1234567890" and self.game.puzzle[self.row][self.col][
            1] == "modifiable_cell":  # event.char is "2" if 2 is pressed

            self.game.puzzle[self.row][self.col][0] = int(event.char)

            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    def __clear_answers(self):
        # resets the game to its original state

        self.game.start()
        # delete the victory tag if the user solved the grid

        self.canvas.delete("victory")

        self.__draw_puzzle()


class SudokuBoard(object):
    """
    Sudoku Board representation
    """

    def __init__(self, board_file):
        self.board = self.__create_board(board_file)

    # Private function
    def __create_board(self, board_file):
        """Function that creates a matrix representing the sudoku board"""
        board = []

        for line in board_file:

            line = line.strip()  # strop erases any unnecessary character
            if len(line) != 9:
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )
            board.append([])

            for c in line:

                if not c.isdigit():
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9"
                    )

                if c != '0':
                    board[-1].append([int(c), "blocked_cell"])
                else:
                    board[-1].append([int(c), "modifiable_cell"])

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")

        return board


class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    Class so that we maintain the state of the game
    """

    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board

    def start(self):
        # Flag that turns True when the game is done
        self.game_over = False
        # Creation of a copy of the puzzle : self.puzzle = self.start_puzzle would keep update both states
        self.puzzle = []

        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def __check_block(self, block):
        # We check that what we call a block (will be row, columns or squares) contains 1->9.

        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        # The input row is an integer
        # Using check_block, we check if each row has 1->9
        row_values = [value[0] for value in self.puzzle[row]]
        return self.__check_block(row_values)

    def __check_column(self, column):
        # Using check_block, we check if each columnn has 1->9
        col_values = [value[0] for value in [self.puzzle[row][column] for row in range(9)]]
        return self.__check_block(col_values)

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c][0]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )
