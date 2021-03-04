class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_square(self):
        return self.height * self.width


if __name__ == '__main__':
    figure = Rectangle (5, 10, 50, 100)
    print(f'width: {figure.get_width()}\nheight: {figure.get_height()}\nsquare: {figure.get_square()}')
