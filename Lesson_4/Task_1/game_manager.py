from strategies import STRATEGY_FACTORY, create_strategy
from players import HumanPlayer, BotPlayer


class GameManager:
    def __init__(self):
        self.low = None
        self.high = None
        self.k_steps = None
        self.players = []
        self.rounds_log = []

    # ----------------------- НАСТРОЙКА -----------------------
    def configure(self):
        print("=" * 55 + "    Игра «Угадай число»    " + "=" * 55)
        self._configure_range()
        self._configure_steps()
        self._configure_players()

    def _configure_range(self):
        while True:
            try:
                self.low = int(input("Нижняя граница диапазона: "))
                self.high = int(input("Верхняя граница диапазона: "))
                if self.low < self.high:
                    return
                print("Нижняя граница должна быть меньше верхней.")
            except ValueError:
                print("Введите целые числа.")

    def _configure_steps(self):
        while True:
            try:
                self.k_steps = int(input("Число шагов K (сколько всего предположений за игру у каждого игрока): "))
                if self.k_steps > 0:
                    return
                print("K должно быть положительным.")
            except ValueError:
                print("Введите целое число.")

    def _configure_players(self):
        human = HumanPlayer("Пользователь")
        human.set_strategy()

        bot = BotPlayer("Бот")
        print("\nСтратегия угадывания для бота:")
        for key, (name, _) in STRATEGY_FACTORY.items():
            print(f"  {key} — {name}")
        while True:
            s = input("Выберите стратегию (1/2/3): ").strip()
            if s in STRATEGY_FACTORY:
                break
        bot.set_strategy(create_strategy(s, self.low, self.high))
        opponent = bot

        self.players = [human, opponent]



    # ----------------------- ИГРА -----------------------
    def run(self):
        print("\n" + "=" * 55 + "    Игра началась    " + "=" * 55)

        # каждый игрок загадывает число
        for p in self.players:
            p.set_secret(self.low, self.high)
        print("Все игроки загадали числа.\n")

        # Шаги
        step = 0
        winner = None
        while step < self.k_steps:
            p = self.players[step % 2]
            opponent = self.players[(step + 1) % 2]

            print(f"--- Шаг {step + 1}/{self.k_steps}: ход {p.name} ---")
            guess = p.make_guess()

            if guess is None:
                print(f"  {p.name} больше не может делать ход "
                      f"(стратегия исчерпана). Игра завершается.")
                break

            print(f"  {p.name} предполагает: {guess} "
                  f"(пытается угадать число {opponent.name})")

            if guess == opponent.secret_number:
                print(f"  Правильно! {p.name} угадал число!")
                p.receive_feedback(guess, "correct")
                winner = p
                step += 1
                break
            elif guess < opponent.secret_number:
                print(f"  Загаданное число БОЛЬШЕ {guess}.")
                p.receive_feedback(guess, "higher")
            else:
                print(f"  Загаданное число МЕНЬШЕ {guess}.")
                p.receive_feedback(guess, "lower")

            step += 1

        # ------------------ ИТОГ ------------------
        print("\n" + "=" * 55)
        if winner is not None:
            print(f"Победитель: {winner.name} (угадал число до K-го шага).")
        else:
            winner = self._resolve_by_distance()
            if winner is None:
                print("Ничья: никто не угадал, расстояния равны.")
            else:
                print(f"Шаги закончились. Победитель: {winner.name} — "
                      f"его последнее предположение оказалось ближе к "
                      f"загаданному противником числу.")

        self._print_reveal()

    def _resolve_by_distance(self):
        if len(self.players) < 2:
            return None
        p1, p2 = self.players

        d1 = (abs(p1.last_guess - p2.secret_number)
              if p1.last_guess is not None else None)
        d2 = (abs(p2.last_guess - p1.secret_number)
              if p2.last_guess is not None else None)

        print("Расстояния последних предположений:")
        print(f"  {p1.name}: последнее = {p1.last_guess}, "
              f"ошибка = {d1}")
        print(f"  {p2.name}: последнее = {p2.last_guess}, "
              f"ошибка = {d2}")

        if d1 is None and d2 is None:
            return None
        if d1 is None:
            return p2
        if d2 is None:
            return p1
        if d1 < d2:
            return p1
        if d2 < d1:
            return p2
        return None

    def _print_reveal(self):
        print("-" * 55)
        for p in self.players:
            print(f"Загаданное число игрока `{p.name}`: {p.secret_number}")