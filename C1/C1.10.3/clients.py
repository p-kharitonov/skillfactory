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


db = [{'name': 'Иван Петров', 'balance': 50},
      {'name': 'Петр Иванов', 'balance': 10},
      {'name': 'Гвидо ван Россум', 'balance': 'Unknown'}]

clients = [Client(item['name'], item['balance']) for item in db]
for client in clients:
    print(f'Клиент «{client.get_name()}». Баланс: {client.get_balance()} руб.')
