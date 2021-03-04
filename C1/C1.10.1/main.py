class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def __str__(self):
        return f'x: {self.x}\ny: {self.y}\nwidth: {self.width}\nheight: {self.height}'


if __name__ == '__main__':
    figure = Rectangle(5, 10, 50, 100)
    print(figure)
