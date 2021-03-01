# Вывод поля
def show_field(field):
    print()
    print(*[' ', 0, 1, 2], '', sep=' | ')
    for i,row in enumerate(field):
        print([0, 1, 2][i], *row, '', sep=' | ')

# Проверка правильности введенных координат
def verification_input(data_input):
    if len(data_input) != 2:
        return False
    for n in data_input:
        if n not in ['0', '1', '2']:
            return False
    return True

# Получение координат хода
def get_coordinates(chair,field):
    while True:
        data_input = input(f'Ходят {chair}, ведите номер строки и столбца через пробел: ')
        data_input = data_input.split()
        if verification_input(data_input):
            data_input = list(map(int,data_input))
            if field[data_input[0]][data_input[1]] == ' ':
                return data_input
            else:
                print('Эта клетка уже занята!')
        else:
            print("Некорректный ввод! Введите два числа от 0 до 2 включительно через пробел")

# Проверка выигрышного хода
def check_win(field):
    new_field = [n for row in field for n in row]  # Получение игрового поля в виде одномерного массива
    win_coordinates = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)) # Выигрышные координаты
    for win_coordinate in win_coordinates:
        if new_field[win_coordinate[0]] == new_field[win_coordinate[1]] == new_field[win_coordinate[2]] != ' ':
            return True

def main():
    name_game = '--- Крестики-нолики ---'
    rules_game = 'Поле 3x3. Для хода каждому игроку предлагается ввести координаты клетки (строка и столбец).'
    print('\n'.join(["-"*len(name_game), name_game, "-"*len(name_game), rules_game]))  # Вывод описания игры
    chars = [['X', 'Крестики'], ['0', 'Нолики']]                         # Символы для игры
    while True:
        field = [[' ' for i in range(3)] for j in range(3)]             # Генерируем пустое поле
        show_field(field)                                               # Выводим пустое поле
        for step in range(9):                                           # 9 ходов
            player = step%2
            coordinates = get_coordinates(chars[player][1], field)    # Получаем координаты хода
            field[coordinates[0]][coordinates[1]] = chars[player][0]  # Заносим ход в поле
            show_field(field)                                           # Выводим получившееся поле
            if check_win(field):                                        # Проверяем может кто-то уже выиграл
                print(f'Победили {chars[player][1]}!\n')
                break
        else:                                                           # Если все ходы прошли без выигрыша, то ничья
            print("Ничья!\n")
        while True:                                                     # Предложение сыграть еще раз
            reload = input("Сыграем ещё? (да/нет): ")
            if 'нет' in reload.lower():
                return
            elif 'да' in reload.lower():
                break
            else:
                print('Введите либо "да", либо "нет".')


if __name__ == "__main__":
    main()
