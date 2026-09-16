def ask(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer == "да":
            return True
        if answer == "нет":
            return False
        print("Ответьте 'да' или 'нет'.")


def main():
    print("Загадайте целое число и укажите интервал, в котором оно находится.")

    while True:
        try:
            low = int(input("Нижняя граница интервала: "))
            high = int(input("Верхняя граница интервала: "))
        except ValueError:
            print("Ошибка: введите целые числа.")
            continue

        if low > high:
            print("Ошибка: нижняя граница не должна быть больше верхней.")
            continue
        break

    attempts = 0
    while low <= high:
        mid = (low + high) // 2
        attempts += 1

        if ask(f"Число равно {mid}?\n"):
            print(f"\nВаше число: {mid}")
            print(f"Количество вопросов: {attempts}")
            return

        if ask(f"Число меньше {mid}?\n"):
            high = mid - 1
        else:
            low = mid + 1
        print("\n")

    print("В указанном интервале нет числа, "
          "которое удовлетворяло бы всем ответам")

if __name__ == "__main__":
    main()