# Реализовать функцию (или набор функций), которые выводят на экран таблицы 
# умножения, деления, вычитания, сложения для чисел 1..9. 
# Выбор таблицы осуществляется пользователем.

def multiplication_table():
    for a in range (1, 10):
        for b in range (1, 10):
             print(f"{a * b :>3}", end="")
        print()

def division_table():
    for a in range (1, 10):
        for b in range (1, 10):
             print(f"{a / b :>3}", end="")
        print()

def subtraction_table():
    for a in range (1, 10):
        for b in range (1, 10):
             print(f"{a - b :>3}", end="")
        print()

def addition_table():
    for a in range (1, 10):
        for b in range (1, 10):
             print(f"{a + b :>3}", end="")
        print()

def main():
    c = input("Введите символ таблицы: ")
    if c == '*':
        multiplication_table()
    elif c == '/':
        division_table()
    elif c == '-':
        subtraction_table()
    elif c == '+':
        addition_table()
    else:
        print("Неверный символ")
        return

if __name__ == "__main__":
    main()