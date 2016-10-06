# -*- coding: utf-8 -*-
from functools import partial
from Tkinter import *
import tkMessageBox as Alert


class TTTGame(object):
    GAME = "Tic Tac Toe"
    # Set to size of board; board is n X n where n = DEFAULT_SIZE
    DEFAULT_SIZE = 3
    # "Enum" Marks
    UNCHECKED = 0
    X = 1
    O = 2

    # This is the game board, which sets up the buttons (to be marked) and also
    # handles game logic
    class TTTBoard(object):
        # This encapsulates the Button widget along with keeping track of its
        # current state and making a callback when clicked
        class TTTButton(object):
            def __init__(self, root_window, callback, **kwargs):
                if 'id' not in kwargs:
                    raise Exception(
                        "{} id not provided".format(self.__class__.__name__))
                self.callback = callback
                self._id = kwargs['id']
                self.mark = TTTGame.UNCHECKED
                self.root_window = root_window
                self.widget = Button(
                    root_window,
                    command=self.do_callback)

            def reset(self):
                self.mark = TTTGame.UNCHECKED
                self.set_mark(self.mark)

            def do_callback(self):
                self.callback(self._id)

            def get_mark(self):
                return self.mark

            def set_mark(self, mark):
                # Do not update if already marked
                if self.mark != TTTGame.UNCHECKED:
                    return False
                self.mark = mark
                txt = ''
                if mark == TTTGame.X:
                    txt = 'x'
                elif mark == TTTGame.O:
                    txt = 'o'
                self.widget.configure(text=txt)
                return True

            def is_mark(self, mark):
                return (self.mark == mark)

        # TTTBoard constructor and functions
        def __init__(self, root_window, winner_callback, **kwargs):
            self.buttons_marked = 0
            self.root_window = root_window
            self.frame = Frame(root_window)
            self.player = 0
            self.starting_player = 0
            self.won = False
            # callback upon winner
            self.winner_callback = winner_callback
            # n X n board, where n = size
            self.size = TTTGame.DEFAULT_SIZE
            if 'size' in kwargs:
                try:
                    self.size = max(int(kwargs['size']), TTTGame.DEFAULT_SIZE)
                except Exception:
                    pass
            self.init_buttons()

        def init_buttons(self):
            self.buttons = []
            for r in range(0, self.size):
                for c in range(0, self.size):
                    _id = self.get_button_id(r, c)
                    button = self.TTTButton(
                        self.frame,
                        self.ttt_button_clicked,
                        id=_id)
                    #
                    self.buttons.append(button)
                    # Add to board
                    button.widget.grid(row=r, column=c)

        # Compute button id by given row and column
        def get_button_id(self, row, col):
            return (row * self.size + col)

        def reset(self, restart):
            # Reset buttons
            for r in range(0, self.size):
                for c in range(0, self.size):
                    _id = self.get_button_id(r, c)
                    self.buttons[_id].reset()
            # Reset winnder
            self.won = False
            # Update who starts
            if restart:
                self.player = 0
                self.starting_player = 0
            else:
                self.player = self.update_starting_player()
            #
            self.buttons_marked = 0

        # Ensures starting player alternates
        def update_starting_player(self):
            self.starting_player = (self.starting_player + 1) % 2
            return self.starting_player

        def update_player(self):
            self.player = (self.player + 1) % 2

        def get_player_mark(self):
            # Get previous player's mark
            return (
                TTTGame.O if bool(self.player) else TTTGame.X)

        def ttt_button_clicked(self, _id):
            # If button did not update, do not attempt board updates
            if self.won or not self.buttons[_id].set_mark(self.get_player_mark()):
                return
            # Button updated
            self.buttons_marked += 1
            self.won = self.check_winner()
            if self.won:
                self.winner_callback(self.player)
            else:
                self.update_player()
                # No winner
                if self.buttons_marked == (pow(self.size, 2)):
                    self.winner_callback(-1)

        # Check if list of ids are similarly marked
        def check_ids_for_winner(self, ids):
            mark = TTTGame.UNCHECKED
            for _id in ids:
                # Unchecked doesn't allow a solution
                if self.buttons[_id].is_mark(TTTGame.UNCHECKED):
                    return False
                # Get first mark
                if mark == TTTGame.UNCHECKED:
                    mark = self.buttons[_id].get_mark()
                if not self.buttons[_id].is_mark(mark):
                    return False
            return True

        # Iterate through buttons to find if a winning combination exists
        def check_winner(self):
            # Needs to have minimum before attempt extensive lookup
            if self.buttons_marked < (self.size * 2 - 1):
                return False
            # Check rows
            for r in range(0, self.size):
                ids = []
                for c in range(0, self.size):
                    ids.append(self.get_button_id(r, c))
                if self.check_ids_for_winner(ids):
                    return True
            # Check cols
            for c in range(0, self.size):
                ids = []
                for r in range(0, self.size):
                    ids.append(self.get_button_id(r, c))
                if self.check_ids_for_winner(ids):
                    return True
            # Check diagonals
            ids = []
            for i in range(0, self.size):
                ids.append(i * self.size + i)
            if self.check_ids_for_winner(ids):
                return True
            ids = []
            for i in range(0, self.size):
                ids.append(i * self.size + (self.size - i - 1))
            if self.check_ids_for_winner(ids):
                return True
            return False


    class TTTScoreBoard(object):
        class TTTScoreLabel(object):
            def __init__(self, root_window, player_id):
                self.points = 0
                self.player_id = player_id
                self.widget = Label(root_window, text="")
                self.update()

            def update(self):
                self.widget.configure(text=
                    ("Player {}\n{}").format(self.player_id, self.points))

            def increment(self):
                self.points += 1
                self.update()

            def reset(self):
                self.points = 0
                self.update()

        # TTTScoreBoard constructor and functions
        def __init__(self, root_window):
            self.frame = Frame(root_window)
            self.score_labels = []
            for i in range(0, 2):
                self.score_labels.append(self.TTTScoreLabel(self.frame, i))
                # Position vertically stacked
                self.score_labels[i].widget.grid(row=i, column=0)

        def increment(self, player_id):
            self.score_labels[player_id].increment()

        def reset(self):
            for i in range(0, 2):
                self.score_labels[i].reset()

    # TTTGame constructor and functions
    def __init__(self, **kwargs):
        self.root_window = Tk()
        self.root_window.wm_title(self.GAME)
        self.menu_bar = self.create_menu(self.root_window)
        #
        self.left_frame = Frame(self.root_window).grid(row=0, column=0)
        self.right_frame = Frame(self.root_window).grid(row=0, column=1)
        # Add score board
        Frame(self.right_frame, width=100, height=25).grid(row=0, column=1)
        Frame(self.right_frame, width=100, height=25).grid(row=2, column=1)
        Frame(self.right_frame, width=25, height=100).grid(row=1, column=2)
        self.score_board = self.TTTScoreBoard(self.left_frame)
        self.score_board.frame.grid(row=1, column=0)
        # n X n board, where n = size
        self.size = TTTGame.DEFAULT_SIZE
        if 'size' in kwargs:
            try:
                self.size = max(int(kwargs['size']), TTTGame.DEFAULT_SIZE)
            except Exception:
                pass
        # Add game board
        self.board = self.TTTBoard(
            self.right_frame, self.winner, size=self.size)
        self.board.frame.grid(row=1, column=1)

    # Setup board and start game
    def start(self):
        self.root_window.mainloop()

    # Prompt to clear board and reset to initial player
    def restart(self):
        result = Alert.askquestion(
            "Restart",
            "Restarting will clear score board and reset to Player 0. Continue?")
        if result == 'yes':
            print("Restart")
            self.board.reset(True)
            self.score_board.reset()

    # Winner callback
    def winner(self, player_id):
        if player_id >= 0:
            print("Player {} Won".format(player_id))
            self.score_board.increment(player_id)
        self.board.reset(False)

    def create_menu(self, root_window):
        self.menu_bar = Menu(root_window)
        # create a pulldown menu, and add it to the menu bar
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Restart', command=self.restart)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=self.root_window.quit)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        #
        self.root_window.config(menu=self.menu_bar)


# Setup and start game if main program
if __name__ == "__main__":
    # Initialize board with 3 X 3 tiles
    game = TTTGame(size=3)
    game.start()
