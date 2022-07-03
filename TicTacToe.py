from random import choice


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

    def __str__(self):
        d = {0: ' ', 1: 'x', 2: 'o'}
        return d[self.value]


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.init()

    def __getitem__(self, key):
        return self.pole[key[0]][key[1]].value

    def __setitem__(self, key, value):
        i, j = key
        if type(i) != int or i < 0 or i > 2 or type(j) != int or j < 0 or j > 2:
            raise IndexError('некорректно указанные индексы')

        if self.pole[i][j]:
            self.pole[i][j].value = value

        self.__is_human_win = self.__is_win(self.HUMAN_X)
        self.__is_computer_win = self.__is_win(self.COMPUTER_O)
        self.__is_draw = self.__is_no_winner()

    def init(self):
        self.pole = tuple(tuple(Cell() for _ in range(3)) for _ in range(3))
        self.__is_human_win = False
        self.__is_computer_win = False
        self.__is_draw = False

    def show(self):
        for i, row in enumerate(self.pole):
            print(*row, sep=' | ')
            if i != len(self.pole) - 1:
                print('--|---|--')
        print()

    def human_go(self):
        i, j = list(map(int, input('Введите координаты ячейки через пробел: ').split()))
        self[i, j] = self.HUMAN_X

    def computer_go(self):
        free_cells = [c for row in self.pole for c in row if c.value == 0]
        choice(free_cells).value = self.COMPUTER_O

    def __is_win(self, w):
        rows = any(map(lambda row: all(map(lambda x: x.value == w, row)), self.pole))
        cols = any(map(lambda row: all(map(lambda x: x.value == w, row)), zip(*self.pole)))
        cross1 = all(map(lambda x: x.value == w, [self.pole[i][i] for i in range(3)]))
        cross2 = all(map(lambda x: x.value == w, [self.pole[i][-(i + 1)] for i in range(3)]))
        return any([rows, cols, cross1, cross2])

    def __is_no_winner(self):
        no_free_cells = not any(map(lambda row: any(map(lambda x: bool(x), row)), self.pole))
        no_winner = not any([self.is_human_win, self.is_human_win])
        return all([no_free_cells, no_winner])

    @property
    def is_human_win(self):
        return self.__is_human_win

    @property
    def is_computer_win(self):
        return self.__is_computer_win

    @property
    def is_draw(self):
        return self.__is_draw

    def __bool__(self):
        return not any([self.is_human_win, self.is_computer_win, self.is_draw])


game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")
