from pets import Cat

if __name__ == '__main__':
    cats = [Cat(name='Барон', gender='мальчик', age='2 года'),
            Cat(name='Сэм', gender='мальчик', age='2 года')]

    for cat in cats:
        print(cat)
