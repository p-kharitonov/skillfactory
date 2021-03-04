class Client:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def get_name(self):
        return self.name

    def get_balance(self):
        return self.balance

    def change_balance(self, cost):
        self.balance -= cost
        return self.balance


class Guest(Client):
    def __init__(self, name, balance, city, status):
        super().__init__(name, balance)
        self.city = city
        self.status = status

    def __str__(self):
        return f'«{self.name}, г. {self.city}, статус "{self.status}"»'


if __name__ == '__main__':
    db = [{'name': 'Иван Петров', 'balance': 50, 'city': 'Москва', 'status': 'Наставник'},
          {'name': 'Петр Иванов', 'balance': 10, 'city': 'Иваново', 'status': 'Студент'},
          {'name': 'Гвидо ван Россум', 'balance': 'Unknown', 'city': 'Белмонт', 'status': 'Случайный гость'}]

    clients = [Guest(**item) for item in db]
    for client in clients:
        print(client)

