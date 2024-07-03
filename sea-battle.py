import time

import random


class BoardOutException(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def out(self):
        if 1 <= self.x <= 6 and 1 <= self.y <= 6:
            return False
        else:
            return True

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

    def __str__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:
    def __init__(self, length, front_coords, direction):
        self.length = length
        self.health = length
        self.front_coords = front_coords
        self.direction = direction
        self.front_coords_x, self.front_coords_y = self.front_coords.x, self.front_coords.y
        self.dots = [front_coords]
        if self.direction == 'горизонтально':
            for i in range(1, length):
                self.dots.append(Dot(self.front_coords_x - i, self.front_coords_y))

        elif self.direction == 'вертикально':
            for i in range(1, length):
                self.dots.append(Dot(self.front_coords_x, self.front_coords_y + i))


class Board:
    def __init__(self):
        self.matrix = [['O'] * 6 for _ in range(6)]
        self.ships = []
        self.ship_counter = 0
        self.not_shoted_dots = set()
        self.occupied_dots = set()
        self.ships_dots = set()
        self.free_dots = set()
        for i in range(1, 7):
            for j in range(1, 7):
                self.free_dots.add(Dot(i, j))
                self.not_shoted_dots.add(Dot(i, j))
        self.shoted_dots = set()

    def add_ship(self, other):
        if all((coords in self.free_dots) and (coords not in self.occupied_dots) for coords in other.dots):
            self.ships.append(other)
            for coords in other.dots:
                self.ships_dots.add(coords)
                self.occupied_dots.add(coords)
                self.free_dots.discard(coords)
                x, y = coords.x, coords.y
                for step_x in [-1, 0, 1]:
                    for step_y in [-1, 0, 1]:
                        if 1 <= step_x + x <= 6 and 1 <= step_y + y <= 6:
                            self.occupied_dots.add(Dot(step_x + x, step_y + y))

            for coords in self.ships_dots:
                self.matrix[coords.y - 1][coords.x - 1] = '□'
        else:
            raise BoardOutException("корабль сюда поставить нельзя")

    def shot(self, other):
        x, y = other.x, other.y
        if other in self.free_dots:
            print('мимо!')
            self.matrix[y - 1][x - 1] = 'T'
        else:
            for i in range(len(self.ships)):
                if other in self.ships[i].dots:
                    self.ships[i].health = self.ships[i].health - 1
                    if self.ships[i].health == 0:
                        print('убил!')
                        for dot in self.ships[i].dots:
                            x, y = dot.x, dot.y
                            for step_x in [-1, 0, 1]:
                                for step_y in [-1, 0, 1]:
                                    if 1 <= x + step_x <= 6 and 1 <= y + step_y <= 6 and self.matrix[y + step_y - 1][
                                        x + step_x - 1] == 'O':
                                        self.matrix[y + step_y - 1][x + step_x - 1] = 'T'
                                        self.shoted_dots.add(Dot(x + step_x, y + step_y))
                                        self.not_shoted_dots.discard(Dot(x + step_x, y + step_y))

                    else:
                        print('ранил!')
            self.matrix[y - 1][x - 1] = '⛝'
        self.shoted_dots.add(other)
        self.not_shoted_dots.discard(other)

    def clear(self):
        self.matrix = [['O'] * 6 for _ in range(6)]
        self.ships = []
        self.ship_counter = 0
        self.not_shoted_dots = set()
        self.occupied_dots = set()
        self.ships_dots = set()
        self.free_dots = set()
        for i in range(1, 7):
            for j in range(1, 7):
                self.free_dots.add(Dot(i, j))
                self.not_shoted_dots.add(Dot(i, j))
        self.shoted_dots = set()

    def random_create(self, needed_ships):
        big_flag = True
        while big_flag:
            for length in needed_ships:
                flag_added = False
                step_counter = 0
                flag = True
                while flag:
                    try:
                        direction = random.choice(['вертикально', 'горизонтально'])
                        front = random.choice(list(self.free_dots))
                        self.add_ship(Ship(length, front, direction))

                    except BoardOutException:
                        pass

                    else:
                        flag = False
                        flag_added = True
                        step_counter = 0

                    finally:
                        step_counter += 1

                    if step_counter > 1000:
                        self.clear()
                        break
                if flag_added is False:
                    break

                if len(self.ships) == 7:
                    big_flag = False

    def ships_in_game(self):
        counter = 0
        for ship in self.ships:
            if ship.health > 0:
                counter += 1

        return counter

    def print_player(self):
        print('@ | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i in range(len(self.matrix)):
            print(str(i + 1) + " |", " | ".join(self.matrix[i]), '|')

    def print_ai(self):
        print('@ | 1 | 2 | 3 | 4 | 5 | 6 |')
        new_matrix = []
        for i in range(6):
            new_matrix.append([])
            for j in range(6):
                if self.matrix[i][j] == '⛝':
                    new_matrix[i].append('⛝')
                elif self.matrix[i][j] == 'T':
                    new_matrix[i].append('T')
                else:
                    new_matrix[i].append('O')
        for i in range(len(new_matrix)):
            print(str(i + 1) + " |", " | ".join(new_matrix[i]), '|')


needed_ships = [3, 2, 2, 1, 1, 1, 1]

player = Board()
ai = Board()
ai.random_create(needed_ships)

print('инструкция:')
print('1. Корабли помечаются символом □, раненные символом - ⛝, выстрелы мимо - Т')
print('2. Не вводите ничего в консоль, пока программа не спросит вас что-либо')
print('3. Чтобы выстрелить нужно ввести в консоль ряд и стобец клетки. Например: 3 3')
print('4. Чтобы поставить корабль нужно указать ряд и столбец его носа, затем направление (если вертикально, то нос смотрит вверх, если горизонтально, то нос смотрит вправо). Например: 1 1 вертикально')
print('5. В игре один корабль на 3 клетки, два корабля на 2 клетки и четыре корабля на 1 клетку')
print('6. Клетки вокруг убитого корабля автоматически помечаются символом Т, то есть мимо')
print('7. Приятной игры!')
while True:
    how_to_create = input('как вы хотите расставить корабли? (рандомно/самостоятельно) ')
    if how_to_create.lower() in ['рандомно', 'самостоятельно']:
        break
    else:
        print('вы ввели что-то не то')

if how_to_create != 'рандомно':
    for length in needed_ships:
        print('')
        flag = True
        while flag:
            try:
                player.print_player()
                inputted_data = input(f'куда вы хотите поставить корабль длиной {length}? ').split()
                if len(inputted_data) == 3:
                    x, y, direction = tuple(inputted_data)

                    x, y = int(x), int(y)
                    if 1 <= x <= 6 and 1 <= y <= 6:
                        pass
                    else:
                        print('Вы ввели что-то не то')
                        continue
                else:
                    print('Вы ввели что-то не то')
                    continue
            except ValueError:
                print('Вы ввели что-то не то')

            try:
                player.add_ship(Ship(length, Dot(y,x), direction))


            except BoardOutException:
                print('Сюда нельзя поставить корабль, давайте ещё раз')


            else:
                flag = False
else:
    player.random_create(needed_ships)

shooting_now = 'player'
while player.ships_in_game() and ai.ships_in_game():
    time.sleep(3)
    print('---------------')
    print(f'ваше поле, живых кораблей: {player.ships_in_game()}:')
    player.print_player()
    print('---------------')
    print(f'поле противника, живых кораблей: {ai.ships_in_game()}:')
    ai.print_ai()
    if shooting_now == 'player':
        print('вы делаете ход')
        try:
            inputted = list(map(int, input('куда хотите выстрелить? ').split()))
            if len(inputted) != 2:
                print('вы ввели что-то не то, давайте ещё раз')
                continue

        except ValueError:
            print('вы ввели что-то не то, давайте ещё раз')
            continue
        x, y = tuple(inputted)
        target = Dot(y, x)
        if target.out():
            print('эта клетка вне поля, давайте ещё раз')
            continue
        if target in ai.shoted_dots:
            print('вы уже стреляли сюда, выберите другую клетку')
            continue

        else:
            ai.shot(target)
            if target not in ai.ships_dots:
                shooting_now = 'ai'


    else:
        print('ИИ делает ход')
        target = random.choice(list(player.not_shoted_dots))
        player.shot(target)
        if target not in player.ships_dots:
            shooting_now = 'player'

    if player.ships_in_game() == 0:
        print('вы проиграли')
        exit(0)

    if ai.ships_in_game() == 0:
        print('вы выиграли')
        exit(0)
