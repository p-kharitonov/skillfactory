class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Координаты за пределами поля"


class BoardBusyException(BoardException):
    def __str__(self):
        return 'Координаты заняты'


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x},{self.y})'


class Ship:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = self.start - self.end
        self.live = self.length

    @property
    def dots(self):
        dots = []
        trend_x = 1 if self.end.x - self.start.x > 0 else -1
        trend_y = 1 if self.end.y - self.start.y > 0 else -1
        for x in range(self.start.x, self.end.x+trend_x, trend_x):
            for y in range(self.start.y, self.end.y+trend_y, trend_y):
                dots.append(Dot(x, y))
        return dots


class Board:
    def __init__(self, hidden=False, size=6):
        self.size = size
        self.hidden = hidden
        self.field = [[' '] * size for _ in range(size)]
        self.ships_dots = []

    def __str__(self):
        result = ' |' + '|'.join([str(count) for count in range(self.size)]) + '|\n'
        for count, row in enumerate(self.field):
            result += str(count) + '|' + '|'.join(row) + '|\n'
        return result

    def add_ship(self, ship):
        for dot in ship.dots:
            if dot in self.ships_dots:
                raise BoardBusyException()
            if dot.x >= self.size or dot.y >= self.size:
                raise BoardOutException()
        for dot in ship.dots:
            self.ships_dots.append(dot)
            self.field[dot.x][dot.y] = '+'


s1 = Ship(Dot(2,0),Dot(2,1))
s2 = Ship(Dot(0,0),Dot(0,0))

board = Board()
board.add_ship(s1)
board.add_ship(s2)

print(board)