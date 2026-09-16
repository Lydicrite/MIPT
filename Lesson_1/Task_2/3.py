import random
while True:
    try:
        N = int(input("Введите размерность векторов: "))
        if N <= 0:
            raise ValueError("Размерность вектора должна быть положительной!")

        a = [random.randint(-100, 100) for _ in range(N)]
        b = [random.randint(-100, 100) for _ in range(N)]

        print(a)
        print(b)
        print(f"Сумма: {[a[i] + b[i] for i in range(N)]}")
        print(f"Умножение: {[a[i] * b[i] for i in range(N)]}")
        print(f"Скалярное произведение: {sum(a[i] * b[i] for i in range(N))}")
        print(f"Вектор с большей нормой: {a if sum(a) > sum(b) else b}")

        s = int(input("Введите скаляр: "))
        print(f"Результат умножения: {[a[i] * s if sum(a) > sum(b) else b[i] * s for i in range(N)]}")

        break
    except ValueError as e:
        print(e)