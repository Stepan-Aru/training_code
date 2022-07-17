from random import randint


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * self._length

    def get_copy(self):
        return self.__class__(self._length, self._tp, self._x, self._y)

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def get_nose(self):
        if self._tp == 1:
            return self._x + (self._length - 1), self._y
        if self._tp == 2:
            return self._x, self._y + (self._length - 1)

    def move(self, go):
        if self._is_move:
            if self._tp == 1:
                self._x += go
            if self._tp == 2:
                self._y += go

    def get_aura(self):
        back_x, back_y = self.get_start_coords()
        nose_x, nose_y = self.get_nose()
        if self._tp == 1:
            return (back_x - 1, back_y - 1), (nose_x + 1, nose_y + 1)
        if self._tp == 2:
            return (back_x - 1, back_y - 1), (nose_x + 1, nose_y + 1)

    def is_collide(self, other):
        if None in other.get_start_coords():
            return False
        s_X1, s_Y1 = self.get_aura()[0]
        s_X2, s_Y2 = self.get_aura()[1]
        o_X1, o_Y1 = other.get_aura()[0]
        o_X2, o_Y2 = other.get_aura()[1]
        v_1 = s_X1 < o_X2
        v_2 = s_X2 > o_X1
        v_3 = s_Y1 < o_Y2
        v_4 = s_Y2 > o_Y1
        return all((v_1, v_2, v_3, v_4))

    def is_out_pole(self, size):
        for coord in (*self.get_start_coords(),*self.get_nose()):
            if not 0 <= coord <= size - 1:
                return True
        return False

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value

    def __repr__(self):
        return f'Корабль: {self._length}-палубный'


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = []

    def init(self):
        for i in range(1, 5):
            for _ in range(i):
                self._ships.append(Ship(5 - i, randint(1, 2)))

        for ship in self._ships:
            while True:
                new_ship = ship.get_copy()
                new_x = randint(0, self._size - 1)
                new_y = randint(0, self._size - 1)
                new_ship.set_start_coords(new_x, new_y)
                if not self.coord_validator(new_ship, ship, self._ships):
                    ship.set_start_coords(new_x, new_y)
                    break

    def get_ships(self):
        return self._ships

    def coord_validator(self, new_ship, old_ship, ships):
        valid_1 = new_ship.is_out_pole(self._size)
        valid_2 = False
        for other_ship in ships:
            if other_ship != old_ship:
                valid_2 = new_ship.is_collide(other_ship)
                if valid_2:
                    break
                        
        return any((valid_1, valid_2))

    def move_ships(self):
        for ship in self._ships:
            new_ship = ship.get_copy()
            new_ship.move(1)
            if not self.coord_validator(new_ship, ship, self._ships):
                ship.move(1)
            else:
                new_ship = ship.get_copy()
                new_ship.move(-1)
                if not self.coord_validator(new_ship, ship, self._ships):
                    ship.move(-1)
                

    def get_pole(self):
        pole = [[0 for _ in range(self._size)] for _ in range(self._size)]
        for ship in self._ships:
            if None not in ship.get_start_coords():
                for i in range(ship._length):
                    if ship._tp == 1:
                        pole[ship._y][ship._x + i] = ship._cells[i]
                    if ship._tp == 2:
                        pole[ship._y + i][ship._x] = ship._cells[i]

        return tuple(tuple(row) for row in pole)

    def show(self):
        res = [' '.join(map(str, row)) for row in self.get_pole()]
        print(*res, sep='\n')


gp = GamePole(10)
gp.init()
gp.show()
gp.move_ships()
print()
gp.show()
