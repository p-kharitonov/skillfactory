# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Игра 'Морской бой', в начале пользователю предлагается выбрать размер доски,        #
# выбрать режим игры (Человек Компьютер, Компьютер/Компьютер) и расположить корабли   #
# автоматически, далее стандартный сценарий, игроки поочереди пытаются потопить       #
# все корабли противника.                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


from random import randint, choice


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Корабль за пределами поля'


class BoardBusyException(BoardException):
    def __str__(self):
        return 'Координаты заняты'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'


class BoardWrongCoordException(BoardException):
    def __str__(self):
        return 'Введите 2 координаты в виде одной буквы и одной цифры (например {})!'


class BoardWrongShipException(BoardException):
    pass


class BoardWrongDotCoordinates(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Метод сравнивает координаты двух точек
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Метод возвращает количество клеток между двумя точками (размер корабля)
    def __sub__(self, other):
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)

    # Метод возвращает точку с суммой координат двух других (для получения точки рядом с кораблем)
    def __add__(self, other):
        return Dot(self.x+other.x, self.y+other.y)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x},{self.y})'


# Конструктор корабля. Входные параметры: крайние точки корабля
class Ship:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = self.start - self.end
        self.lives = self.length

    def __repr__(self):
        return f'{self.__class__.__name__}({self.start,self.end})'

    # Свойство возвращает список точек, принадлежащие кораблю
    @property
    def dots(self):
        dots = []
        trend_x = 1 if self.end.x - self.start.x > 0 else -1  # Получаем направление по осям
        trend_y = 1 if self.end.y - self.start.y > 0 else -1  # от начальной точки к конечной
        for x in range(self.start.x, self.end.x+trend_x, trend_x):
            for y in range(self.start.y, self.end.y+trend_y, trend_y):
                dots.append(Dot(x, y))
        return dots


# Конструктор поля
class Board:
    def __init__(self, hidden=False, size=6):
        self.size = size  # Размер поля
        self.hidden = hidden  # Запрет вывода не открытых клеток кораблей
        self.count = 0  # Количество потопленных кораблей
        self.field = [[' '] * size for _ in range(size)]  # Массив клеток поля
        self.busy = []  # Занятые клетки, 1 - куда нельзя ставить корабль, 2 - куда уже был выстрел
        self.ships = []  # Клетки кораблей

    def __str__(self):
        axis_x = ['A', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И']
        result = '\n  | '
        result += ' | '.join(axis_x[:self.size]) + ' |'
        for i, row in enumerate(self.field, 1):
            result += f'\n{i} | ' + ' | '.join(row) + ' |'
        if self.hidden:
            result = result.replace('o', ' ')
        return result

    # Метод добавляет корабль на поле, если добавить невозможно возвращает соответствующее исключение
    def add_ship(self, ship):
        for dot in ship.dots:
            if dot in self.busy:
                raise BoardBusyException()
            if self.out(dot):
                raise BoardOutException()
        for dot in ship.dots:
            self.busy.append(dot)
            self.field[dot.x][dot.y] = 'o'
        self.ships.append(ship)
        self.contour(ship)

    # Метод добавляет рядомстоящие с кораблем точки
    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dot in ship.dots:
            for x, y in near:
                contour_dot = dot + Dot(x, y)
                if (not self.out(contour_dot)) and (contour_dot not in self.busy):
                    self.busy.append(contour_dot)
                    if verb:
                        self.field[contour_dot.x][contour_dot.y] = '.'

    # Метод проверяет находится ли точка за пределами поля
    def out(self, dot):
        return dot.x >= self.size or dot.x < 0 or dot.y >= self.size or dot.y < 0

    # Метод стрельбы по полю, возвращает True, если корабль потоплен
    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()
        if dot in self.busy:
            raise BoardUsedException()
        self.busy.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.field[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True
        else:
            self.field[dot.x][dot.y] = '.'
            print('Мимо!')
            return False

    # Метод очищает список занятых клеток
    def begin(self):
        self.busy = []


# Родительских класс игроков
class Player:
    def __init__(self, name, own_board, opponent_board):
        self.name = name
        self.own_board = own_board
        self.opponent_board = opponent_board

    def __str__(self):
        return self.name

    # Загатовка для получение координат желаемого выстрела
    def ask(self, size):
        raise NotImplementedError()

    # Метод выстрела игрока по полю противника
    def hit(self, size):
        while True:
            try:
                coordinates = self.ask(size)
                hit = self.opponent_board.shot(coordinates)
                return hit
            except BoardException as e:
                print(e)


# Конструктор ИИ
class AI(Player):
    # Компьютер возвращает координаты выстрела
    def ask(self, size):
        dot = Dot(randint(0, size-1), randint(0, size-1))
        print(f'Ход {self.name}: {chr(dot.y+1072).upper()}{dot.x+1}')
        return dot


# Конструктор пользователя
class User(Player):
    # Спрашиваем у пользователя куда он желает выстрелить
    def ask(self, size):
        x = 0
        y = 0
        while True:
            coordinates = input('Ваш ход: ').lower()
            try:
                if len(coordinates) != 2:
                    raise BoardWrongCoordException
                if not ((coordinates[0].isdigit() or coordinates[1].isdigit()) and
                        (coordinates[0].isalpha() or coordinates[1].isalpha())):
                    raise BoardWrongCoordException
                for char in coordinates:
                    if char.isalpha():
                        y = ord(char) - 1072
                    elif char.isdigit():
                        x = int(char) - 1
                    else:
                        raise BoardWrongCoordException
                return Dot(x, y)
            except BoardWrongCoordException as e:
                random_coordinates = f'{chr(randint(1072, 6 + 1071)).upper()}{randint(1, 6)}'
                print(str(e).format(random_coordinates))


class Game:
    def __init__(self):
        self.size = 6
        self.level = 2
        self.game_mode = 1
        self.random = True
        self.len_ships = [3, 2, 2, 1, 1, 1, 1]
        self.player_1 = None
        self.player_2 = None

    @staticmethod
    def get_option(massage, start, end):
        while True:
            option = input(massage)
            if len(option) == 0:
                return None
            if option.isdigit() and (start <= int(option) <= end):
                return int(option)
            else:
                print('Неправильный ввод! ', end='')

    def select_size(self):
        massage = f'\nВведите размер доски от 6 до 9 [{self.size}]: '
        option = self.get_option(massage, 6, 9)
        if option is not None:
            self.size = option

    def select_game_mode(self):
        massage = f'\nЧеловек / Компьютер - 1\nКомпьютер / Компьютер - 2\nВведите режим игры [{self.game_mode}]: '
        option = self.get_option(massage, 1, 2)
        if option is not None:
            self.game_mode = option

    def is_random(self):
        while True:
            is_random = input('Расположить Ваши корабли автоматически? [да]: ')
            if len(is_random) == 0:
                return self.random
            if 'да' in is_random.lower():
                return True
            elif 'нет' in is_random.lower():
                return False
            else:
                print('Неправильный ввод! ', end='')

    def show_boards(self):
        board_1 = self.player_1.own_board.field
        board_2 = self.player_2.own_board.field
        axis_x = ['A', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И']
        header = '  | ' + ' | '.join(axis_x[:self.size]) + ' |'
        result = '\n' + f'{self.player_1}'.center(3+4*self.size) + ' '*5 + f'{self.player_2}'.center(3+4*self.size) + '\n'
        result += header + ' '*5 + header
        for n in range(0, self.size):
            result += f'\n{n + 1} | ' + ' | '.join(board_1[n]) + ' |'
            result += ' ' * 5
            result += f'{n + 1} | ' + ' | '.join(board_2[n]).replace('o', ' ') + ' |'
        print(result)

    def settings(self):
        self.select_size()  # Выбираем размер поля
        self.select_game_mode()  # Выбираем режим 'Человек vs Компьютер' или 'Компьютер vs Компьютер'
        player_2 = self.random_board()
        if self.game_mode == 1:  # Человек vs Компьютер
            self.random = self.is_random()
            if self.random:
                player_1 = self.random_board()
            else:
                player_1 = self.choice_board()
            self.player_1 = User('Игрок 1', player_1, player_2)
        else:  # Компьютер vs Компьютер
            player_1 = self.random_board()
            self.player_1 = AI('Игрок 1', player_1, player_2)
        self.player_2 = AI('Игрок 2', player_2, player_1)
        player_2.hidden = True

    @staticmethod
    def greet():
        print('-----------------------------------------------')
        print('------------------Морской бой------------------')
        print('-----------------------------------------------\n')
        print('Настройки'.upper())

    def loop(self):
        num = 0
        while True:
            self.show_boards()
            if num % 2 == 0:
                print('-' * (11 + 8*self.size))
                print(f'Ходит {self.player_1}!')
                repeat = self.player_1.hit(self.size)
            else:
                print('-' * (11 + 8*self.size))
                print(f'Ходит {self.player_2}!')
                repeat = self.player_2.hit(self.size)
            if repeat:
                num -= 1
            if self.player_2.own_board.count == 7:
                print('-' * (11 + 8*self.size))
                print(f'{self.player_1} выиграл!')
                break
            if self.player_1.own_board.count == 7:
                print('-' * (11 + 8*self.size))
                print(f'{self.player_2} выиграл!')
                break
            num += 1

    def start(self):
        self.greet()
        self.settings()
        self.loop()

    def choice_board(self):
        board = None
        while board is None:
            board = self.choice_place()
        return board

    def choice_place(self):
        board = Board(size=self.size)
        print(board)
        for len_ship in self.len_ships:
            while True:
                coordinates_ship = input(f'Введите координаты начала и конца коробля с длиной - {len_ship} (например A1 A{len_ship}): ').lower()
                coordinates_ship = coordinates_ship.replace(' ', '')
                coordinates = []
                if len(coordinates_ship) != 4:
                    print('Неправильный ввод! 1 ', end='')
                    continue
                    # raise BoardWrongDotCoordinates
                for coordinate in coordinates_ship:
                    if coordinate.isdigit():
                        coordinate = int(coordinate) - 1
                        coordinates.append(coordinate)
                        continue
                    if coordinate.isalpha():
                        coordinate = ord(coordinate) - 1072
                        coordinates.append(coordinate)
                start_dot = Dot(coordinates[1], coordinates[0])
                end_dot = Dot(coordinates[3], coordinates[2])
                ship = Ship(start_dot, end_dot)
                if ship.length != len_ship:
                    print('Неправильная длина')
                    continue
                try:
                    board.add_ship(ship)
                    print(board)
                    break
                except BoardException as e:
                    print(e)
                    continue
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        board = Board(size=self.size)
        attempts = 0
        for len_ship in self.len_ships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                start_dot = Dot(randint(0, self.size), randint(0, self.size))
                end_dot = start_dot + choice([Dot(0, len_ship-1), Dot(len_ship-1, 0), Dot(0, 1-len_ship), Dot(1-len_ship, 0)])
                ship = Ship(start_dot, end_dot)
                try:
                    board.add_ship(ship)
                    break
                except BoardException:
                    pass
        board.begin()
        return board


if __name__ == '__main__':
    g = Game()
    g.start()
