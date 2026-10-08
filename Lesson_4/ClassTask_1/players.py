from abc import ABC, abstractmethod
import random

from strategies import GuessingStrategy, TerminalStrategy

# Игрок (или бот, или чел)
class Player(ABC):
    def __init__(self, name: str):
        self.name = name
        self.secret_number = None
        self.strategy: GuessingStrategy = None
        self.last_guess = None
        self.history = []

    def set_secret(self, low: int, high: int) -> None:
        self.secret_number = self._choose_secret(low, high)

    def set_strategy(self, strategy: GuessingStrategy) -> None:
        self.strategy = strategy

    @abstractmethod
    def _choose_secret(self, low: int, high: int) -> int:
        ...

    def make_guess(self):
        guess = self.strategy.next_guess()
        self.last_guess = guess
        return guess

    def receive_feedback(self, guess: int, feedback: str) -> None:
        self.history.append((guess, feedback))
        self.strategy.update(guess, feedback)

    def __str__(self):
        return self.name

# Игрок-человек
class HumanPlayer(Player):
    def _choose_secret(self, low, high):
        while True:
            try:
                n = int(input(f"{self.name}, введите ваше секретное число "
                              f"в диапазоне [{low}; {high}]: "))
                if low <= n <= high:
                    return n
                print("Число вне диапазона. Повторите ввод.")
            except ValueError:
                print("Введите целое число.")

    def set_strategy(self, strategy=None):
        self.strategy = TerminalStrategy()

# Игрок-бот
class BotPlayer(Player):
    def _choose_secret(self, low, high):
        print(f"{self.name} загадал своё секретное число.")
        return random.randint(low, high)