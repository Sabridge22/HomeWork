from random import randint
from typing import Optional, Tuple, List

class Ship:

    def __init__(
        self, length: int, tp: int = 1, x: Optional[int] = None, y: Optional[int] = None
    ):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * length

    def set_start_coords(self, x:int, y:int) -> None:
        self._x = x
        self._y = y

    def get_start_coords(self) -> Tuple[int, int]:
        return (self._x, self._y)

    def move(self, go:int) -> None: # движение корабля по полю
        if self._is_move:
            if self._tp == 1:  # горизонтальная ориентация
                new_x = self._x + go
                if new_x >= 0:
                    self._x = new_x
                else:
                    self._x = 0
            elif self._tp == 2:  # вертикальная ориентация
                new_y = self._y + go
                if new_y >= 0:
                    self._y = new_y
                else:
                    self._y = 0

    def is_collide(self, other: 'Ship') -> bool:# проверка на пересечение кораблей

        x1, y1 = self._x, self._y
        len1, len2 = self._length, other._length

        # генерация всех клеток корабля self
        coords1 = set()
        if self._tp == 1:  # горизонтальная ориентация
            coords1.update((x1 + i, y1) for i in range(len1))
            coords1.update(
                (x1 + i, y1 + dy) for i in range(len1) for dy in range(-1, 2)
            )
        else:  # вертикальная ориентация
            coords1.update((x1, y1 + i) for i in range(len1))
            coords1.update(
                (x1 + dx, y1 + i) for i in range(len1) for dx in range(-1, 2)
            )

        # то же самое для other
        coords2 = set()
        if other._tp == 1:  # горизонтальная ориентация
            coords2.update((other._x + i, other._y) for i in range(len2))
            coords2.update(
                (other._x + i, other._y + dy)
                for i in range(len2)
                for dy in range(-1, 2)
            )
        else:  # вертикальная ориентация
            coords2.update((other._x, other._y + i) for i in range(len2))
            coords2.update(
                (other._x + dx, other._y + i)
                for i in range(len2)
                for dx in range(-1, 2)
            )

        # проверка пересечения
        return bool(coords1.intersection(coords2))

    def is_out_pole(self, size: int) -> bool:# выходит ли корабль за поле
        if self._x is None or self._y is None:
            return False

        if self._tp == 1:  # горизонтальная ориентация
            return self._x + self._length > size
        elif self._tp == 2:  # вертикальная ориентация
            return self._y + self._length > size

    def __getitem__(self, indx: int) -> int:
        return self._cells[indx]

    def __setitem__(self, indx:int, value:int)-> None:
        self._cells[indx] = value


class GamePole:
    def __init__(self, size: int)-> None:
        self._size = size
        self._ships = []

    def init(self) -> None:
        ships_to_create = [(4, 1), (3, 2), (2, 3), (1, 4)]
        # размещение кораблей
        for length, count in ships_to_create:
            for _ in range(count):
                tp = randint(1, 2)
                ship = Ship(length, tp)
                placed = False
                while not placed:
                    x = randint(0, self._size - 1)
                    y = randint(0, self._size - 1)
                    ship.set_start_coords(x, y)
                    if not ship.is_out_pole(self._size) and not any(
                        ship.is_collide(other) for other in self._ships
                    ):
                        self._ships.append(ship)
                        placed = True

    def get_ships(self) -> List[Ship]:
        return self._ships

    def move_ships(self)-> None: # перемещение кораблей случ. образом
        for ship in self._ships:
            go = randint(-1, 1)
            ship.move(go)
            if any(
                ship.is_collide(other) for other in self._ships if ship != other
            ) or ship.is_out_pole(self._size):
                ship.move(-go)  # отменить движение

    def show(self)-> None: # вывод поля в консоль
        pole = self.get_pole()
        for row in pole:
            print(" ".join(map(str, row)))

    def get_pole(self)-> Tuple[Tuple[int, ...], ...]:# текущее состояние поля
        pole = [[0] * self._size for _ in range(self._size)]
        for ship in self._ships:
            x, y = ship.get_start_coords()
            for i in range(ship._length):
                if ship._tp == 1:
                    pole[y][x + i] = ship[i]
                else:
                    pole[y + i][x] = ship[i]
        return tuple(tuple(row) for row in pole)


# Tests
ship = Ship(2)
ship = Ship(2, 1)
ship = Ship(3, 2, 0, 0)
assert (
    ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0
), "неверные значения атрибутов объекта класса Ship"
assert ship._cells == [1, 1, 1], "неверный список _cells"
assert ship._is_move, "неверное значение атрибута _is_move"
ship.set_start_coords(1, 2)
assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"
ship.move(1)
s1 = Ship(4, 1, 0, 0)
s2 = Ship(3, 2, 0, 0)
s3 = Ship(3, 2, 0, 2)
assert s1.is_collide(
    s2
), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
assert (
    s1.is_collide(s3) == False
), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"
s2 = Ship(3, 2, 1, 1)
assert s1.is_collide(
    s2
), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"
s2 = Ship(3, 1, 8, 1)
assert s2.is_out_pole(
    10
), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"
s2 = Ship(3, 2, 1, 5)
assert (
    s2.is_out_pole(10) == False
), "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"
s2[0] = 2
assert s2[0] == 2, "неверно работает обращение ship[indx]"
p = GamePole(10)
p.init()
for nn in range(5):
    for s in p._ships:
        assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"
        for ship in p.get_ships():
            if s != ship:
                assert (
                    s.is_collide(ship) == False
                ), "корабли на игровом поле соприкасаются"
    p.move_ships()

gp = p.get_pole()
assert (
    type(gp) == tuple and type(gp[0]) == tuple
), "метод get_pole должен возвращать двумерный кортеж"
assert (
    len(gp) == 10 and len(gp[0]) == 10
), "неверные размеры игрового поля, которое вернул метод get_pole"
pole_size_8 = GamePole(8)
pole_size_8.init()
print("\n Passed")
