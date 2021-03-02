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


db = {'Иван Петров': 50,
      'Петр Иванов': 10,
      'Гвидо ван Россум': 'Unknown'}
clients = [Client(key, value) for key, value in db.items()]
for client in clients:
    print(f'Клиент «{client.get_name()}». Баланс: {client.get_balance()} руб.')
