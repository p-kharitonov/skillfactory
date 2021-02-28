class Cat:

    def __init__(self, name='Unknown', gender='Unknown', age='Unknown'):
        self.name = str(name)
        self.gender = str(gender)
        self.age = str(age)

    def __str__(self):
        return f'Имя: {self.name}\nПол: {self.gender}\nВозраст: {self.age}'
