max_num = 0
while True:
    try:
        num = int(input("Введите число: "))
        
        if num > max_num:
            max_num = num
        elif num == 0:
            print(f"Максимальное из введённых чисел: {max_num}")
            break
        elif num < 0:
            raise ValueError
    except ValueError:
        print("Необходимо ввести целое число больше 0, или 0, чтобы закончить ввод чисел")
