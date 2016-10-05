from functools import partial
from Tkinter import *


class Mark(object):
    unchecked = 0
    x = 1
    o = 2


class TTTButton(object):
    def __init__(self, root_window, callback, **kwargs):
        if 'id' not in kwargs:
            raise Exception(
                "{} id not provided".format(self.__class__.__name__))
        self.callback = callback
        self._id = kwargs['id']
        self.mark = Mark.unchecked
        self.root_window = root_window
        self.widget = Button(
            root_window,
            command=self.do_callback)

    def do_callback(self):
        self.callback(self._id)

    def get_mark(self):
        return self.mark

    def set_mark(self, mark):
        self.mark = mark
        txt = ''
        if mark == Mark.x:
            txt = 'x'
        elif mark == Mark.o:
            txt = 'o'
        self.widget.configure(text=txt)

    def is_mark(self, mark):
        return (self.mark == mark)


class TTTBoard(object):
    DEFAULT_SIZE = 3
    #
    buttons_marked = 0
    player = 0

    def __init__(self, root_window, winner_callback, **kwargs):
        self.root_window = root_window
        self.frame = Frame(root_window)
        # callback upon winner
        self.winner_callback = winner_callback
        # n X n board, where n = size
        self.size = self.DEFAULT_SIZE
        if 'size' in kwargs:
            try:
                self.size = max(int(kwargs['size']), self.DEFAULT_SIZE)
            except Exception:
                pass
        self.init_buttons()

    def get_button_id(self, row, col):
        return (row * self.size + col)

    def init_buttons(self):
        self.buttons = []
        for r in range(0, self.size):
            for c in range(0, self.size):
                '''button = Button(
                    self.root_window, text='',
                    command=lambda: partial(self.dumby, "{}{}".format(r, c)) ).grid(
                        row=r, column=c)'''
                '''
                button = Button(
                    self.root_window, text=("{}{}").format(r, c))
                button.grid(row=r, column=c)
                '''
                _id = self.get_button_id(r, c)
                button = TTTButton(
                    self.root_window,
                    self.ttt_button_clicked,
                    id=_id)
                #
                self.buttons.append(button)
                # Add to board
                button.widget.grid(row=r, column=c)

    def update_player(self):
        self.buttons_marked += 1
        self.player = (self.player + 1) % 2

    def get_player_mark(self):
        self.update_player()
        # Get previous player's mark
        return (
            Mark.x if bool(self.player) else Mark.o)

    def ttt_button_clicked(self, _id):
        # print(str(text))
        self.buttons[_id].set_mark(
            self.get_player_mark())
        #
        if self.check_winner():
            print("Won")

    def check_ids_for_winner(self, ids):
        mark = Mark.unchecked
        for _id in ids:
            # Unchecked doesn't allow a solution
            if self.buttons[_id].is_mark(Mark.unchecked):
                return False
            # Get first mark
            if mark == Mark.unchecked:
                mark = self.buttons[_id].get_mark()
            if not self.buttons[_id].is_mark(mark):
                return False
        return True

    def check_winner(self):
        # Needs to have minimum before attempt extensive lookup
        if self.buttons_marked < (self.size * 2 - 1):
            return False
        # Check rows
        found = True
        for r in range(0, self.size):
            '''
            mark = Mark.unchecked
            found = True
            for c in range(0, self.size):
                _id = self.get_button_id(r, c)
                # Unchecked doesn't allow a solution
                if self.buttons[_id].is_mark(Mark.unchecked):
                    found = False
                    print("0 0")
                    break
                # Get first mark
                if mark == Mark.unchecked:
                    mark = self.buttons[_id].get_mark()
                # Check
                if not self.buttons[_id].is_mark(mark):
                    found = False
                    print("0 1")
                    break
            if found:
                return True
            '''
            ids = []
            for c in range(0, self.size):
                ids.append(self.get_button_id(r, c))
            if self.check_ids_for_winner(ids):
                return True

        # Check cols
        for c in range(0, self.size):
            '''
            mark = Mark.unchecked
            found = True
            for r in range(0, self.size):
                _id = self.get_button_id(r, c)
                # Unchecked doesn't allow a solution
                if self.buttons[_id].is_mark(Mark.unchecked):
                    found = False
                    print("1 0")
                    break
                # Get first mark
                if mark == Mark.unchecked:
                    mark = self.buttons[_id].get_mark()
                # Check
                if not self.buttons[_id].is_mark(mark):
                    found = False
                    print("1 1")
                    break
            if found:
                return True
            '''
            ids = []
            for r in range(0, self.size):
                ids.append(self.get_button_id(r, c))
            if self.check_ids_for_winner(ids):
                return True
        # Check diagonals
        return False


def restart():
    print("Restart")


def winner(player_ID):
    print("Player {} Won".format(player_ID))


def create_menu(root_window):
    menu_bar = Menu(root_window)
    # create a pulldown menu, and add it to the menu bar
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Restart', command=restart)
    file_menu.add_separator()
    file_menu.add_command(label='Quit', command=root_window.quit)
    menu_bar.add_cascade(label='File', menu=file_menu)
    #
    root_window.config(menu=menu_bar)


root_window = Tk()
menu_bar = create_menu(root_window)
board = TTTBoard(root_window, winner)

# Code to add widgets will go here...
root_window.mainloop()
