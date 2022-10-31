from abc import *
from random import randint
from itertools import repeat


class Move:
    def __init__(self, counter, x, y):
        self.x = x
        self.y = y
        self.counter = counter


class Player(metaclass=ABCMeta):

    def __init__(self, board):
        self.board = board
        self._counter = None

    @abstractmethod
    def get_move(self):
        pass

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = value

    def __str__(self):
        return self.__class__.__name__ + "[" + self._counter + "]"


def dependent_func(a, b, c):
    if b != " ":
        if b == c:
            return "C"
        else:
            return "H"
    else:
        return a


class ComputerPlayer(Player):
    def __init__(self, board):
        super().__init__(board)
        self.row_data = [1, 1, 1, 1, 1, 1, 1, 1]
        self.shell_count = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

    def get_move(self):
        self.shell_count = list(map(lambda x, y: list(map(dependent_func, x, y, repeat(self.counter, 3))), self.shell_count, self.board.shell_cell))
        self.make_it_think()
        self.mark_it()
        large_value = self.best_move()
        row = large_value[0]
        col = large_value[1]
        if not self.board.check_cell_is_empty(row, col):
            print("Error\nSomething wrong has happened")
        self.board.move(Move(self.counter, row, col))

    def best_move(self):
        large_value = [0, 0, 0]
        ii=0
        for i in self.shell_count:
            jj = 0
            for j in i:
                if type(j) == int and j > large_value[0]:
                    large_value[0] = j
                    large_value[1] = ii
                    large_value[2] = jj
                jj += 1
            ii += 1
        return large_value[1:]

    def mark_it(self):
        j = 0
        for i in self.row_data:
            if i > 0:
                self.search_and_mark(j)
            j += 1

    def make_it_think(self):
        j = 0
        for i in self.row_data:
            if i > 0:
                self.make_it_search(j)
            j += 1

    def make_it_search(self, index_of_row):
        if index_of_row < 3:
            sam_list = self.shell_count[index_of_row]
        elif index_of_row < 6:
            sam_list = [self.shell_count[0][index_of_row-3], self.shell_count[1][index_of_row-3], self.shell_count[2][index_of_row-3]]
        elif index_of_row==6:
            sam_list = [self.shell_count[0][0], self.shell_count[1][1], self.shell_count[2][2]]
        else:
            sam_list = [self.shell_count[0][2], self.shell_count[1][1], self.shell_count[2][0]]
        if "C" in sam_list and "H" in sam_list:
            self.row_data[index_of_row] -= 1
        elif "C" in sam_list or "H" in sam_list:
            if sam_list.count('C') > 1:
                self.row_data[index_of_row] += 5
            elif sam_list.count('H') > 1:
                self.row_data[index_of_row] += 4
            else:
                self.row_data[index_of_row] += 1

    def search_and_mark(self, index_of_row):
        if index_of_row < 3:
            if type(self.shell_count[index_of_row][0]) == int:
                self.shell_count[index_of_row][0] += self.row_data[index_of_row]
            if type(self.shell_count[index_of_row][1]) == int:
                self.shell_count[index_of_row][1] += self.row_data[index_of_row]
            if type(self.shell_count[index_of_row][2]) == int:
                self.shell_count[index_of_row][2] += self.row_data[index_of_row]
        elif index_of_row < 6:
            if type(self.shell_count[0][index_of_row-3])==int:
                self.shell_count[0][index_of_row-3] += self.row_data[index_of_row]
            if type(self.shell_count[1][index_of_row-3])==int:
                self.shell_count[1][index_of_row-3] += self.row_data[index_of_row]
            if type(self.shell_count[2][index_of_row-3])==int:
                self.shell_count[2][index_of_row-3] += self.row_data[index_of_row]
        elif index_of_row == 6:
            if type(self.shell_count[0][0])==int:
                self.shell_count[0][0] += self.row_data[index_of_row]
            if type(self.shell_count[1][1])==int:
                self.shell_count[1][1] += self.row_data[index_of_row]
            if type(self.shell_count[2][2])==int:
                self.shell_count[2][2] += self.row_data[index_of_row]
        else:
            if type(self.shell_count[0][2])==int:
                self.shell_count[0][2] += self.row_data[index_of_row]
            if type(self.shell_count[1][1])==int:
                self.shell_count[1][1] += self.row_data[index_of_row]
            if type(self.shell_count[2][0])==int:
                self.shell_count[2][0] += self.row_data[index_of_row]


def get_user_input(string_val):
    val = input(string_val)
    valid = True
    while valid:
        if not val.isdigit():
            val = input("Invalid input\n" + string_val)
        elif val not in ['1', '2', '3']:
            val = input("Number out of range\n" + string_val)
        else:
            valid = False
    return int(val)


class HumanPlayer(Player):
    def __init__(self, board):
        super().__init__(board)

    def get_move(self):
        row = get_user_input("Enter the row: ")
        col = get_user_input("Enter the column: ")
        while not self.board.check_cell_is_empty(row-1, col-1):
            print("Shell is not free\nTry again!!")
            row = get_user_input("Enter the row: ")
            col = get_user_input("Enter the column: ")
        self.board.move(Move(self.counter, row-1, col-1))


class Counter:
    def __init__(self, string):
        self.label = string

    def __str__(self):
        return self.label


class Board:
    def __init__(self):
        self.shell_cell = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.separator = "\n" + ("-" * 13) + "\n"

    def __str__(self):
        row1 = "| " + str(self.shell_cell[0][0]) + " | " + str(self.shell_cell[0][1]) + " | " + str(
            self.shell_cell[0][2]) + " |"
        row2 = "| " + str(self.shell_cell[1][0]) + " | " + str(self.shell_cell[1][1]) + " | " + str(
            self.shell_cell[1][2]) + " |"
        row3 = "| " + str(self.shell_cell[2][0]) + " | " + str(self.shell_cell[2][1]) + " | " + str(
            self.shell_cell[2][2]) + " |"
        return "\n" + row1 + self.separator + row2 + self.separator + row3

    def move(self, move):
        self.shell_cell[move.x][move.y] = move.counter


    def check_shell_is_full(self):
        for i in self.shell_cell:
            for j in i:
                if j == " ":
                    return False
        return True

    def check_win(self, player):
        label = player._counter
        for i in self.shell_cell:
            if i[0] == label and i[1] == label and i[2] == label:
                return True
        for (i, j, k) in zip(self.shell_cell[0], self.shell_cell[1], self.shell_cell[2]):
            if i == label and j == label and k == label:
                return True
        if self.shell_cell[1][1] == label:
            if self.shell_cell[0][0]==label and self.shell_cell[2][2]==label:
                return True
            elif self.shell_cell[0][2]==label and self.shell_cell[2][0]==label:
                return True
        return False

    def check_cell_is_empty(self, x, y):
        if self.shell_cell[x][y] == " ":
            return True
        return False


X = Counter('X')
Y = Counter('O')


class Game:
    def __init__(self):
        self.board = Board()
        self.computer_player = ComputerPlayer(self.board)
        self.human_player = HumanPlayer(self.board)
        self.winner = None
        self.next_player = None

    def __str__(self):
        return "<Object of tic tac toe game>"

    def select_counter(self):
        counter = input("Select your placeholder[X/O]:")
        while counter not in ["X", "O", "o", "x"]:
            counter = input("Invalid input\nSelect your placeholder[X/O]:")
        if counter in ["X", "x"]:
            self.human_player.counter = "X"
            self.computer_player.counter = "O"
        else:
            self.human_player.counter = "O"
            self.computer_player.counter = "X"

    def play(self):
        print("-"*50, "          Welcome to the Tic Tac Toe game          ", "-"*50, sep="\n")
        self.select_counter()
        print("Tossing a coin......")
        #remember 0 is human and 1 is computer
        players_list = [self.human_player, self.computer_player]
        current_player = randint(0, 1)
        if current_player == 0:
            print("Oops!! you won the toss")
            self.next_player = 1
        else:
            print("U lost the toss")
            self.next_player = 0
        print(self.board)
        while True:
            if self.board.check_win(players_list[self.next_player]):
                if self.next_player==0:
                    print("OOOOh!!\nYou did it!!\nYou won!!")
                    return 0
                else:
                    print("Computer won it!!\nTry again later")
                    return 0
            if self.board.check_shell_is_full():
                print("Its a draw!!")
                return 0
            if current_player == 0:
                print("It's your turn")
            else:
                print("Its computers turn")
            players_list[current_player].get_move()
            print(self.board)
            val = current_player
            current_player = self.next_player
            self.next_player = val


if __name__ == '__main__':
    game = Game()
    game.play()


