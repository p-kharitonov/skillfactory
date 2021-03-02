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
        Client.__init__(self, name, balance)
        self.city = city
        self.status = status

    def get_city(self):
        return self.city

    def get_status(self):
        return self.status


db = [{'name': 'Иван Петров', 'balance': 50, 'city': 'Москва', 'status': 'Наставник'},
      {'name': 'Петр Иванов', 'balance': 10, 'city': 'Иваново', 'status': 'Студент'},
      {'name': 'Гвидо ван Россум', 'balance': 'Unknown', 'city': 'Белмонт', 'status': 'Случайный гость'}]

clients = [Guest(item['name'], item['balance'], item['city'], item['status']) for item in db]
for client in clients:
    print(f'«{client.get_name()}, г. {client.get_city()}, статус "{client.get_status()}"»')

