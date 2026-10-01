from abc import ABC, abstractmethod
import random

class GuessingStrategy(ABC):
    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high

    @abstractmethod
    def next_guess(self):
        """Следующее предположение (или None, если вариантов больше нет)."""
        ...

    @abstractmethod
    def update(self, guess: int, feedback: str) -> None:
        """
        Обновляет состояние стратегии по результату хода.
        feedback: 'correct' | 'higher' | 'lower'.
        """
        ...

    @property
    def exhausted(self) -> bool:
        return self.low > self.high


# Дихотомия
class DichotomyStrategy(GuessingStrategy):
    def next_guess(self):
        if self.exhausted:
            return None
        return (self.low + self.high) // 2

    def update(self, guess, feedback):
        if feedback == "higher":
            self.low = max(self.low, guess + 1)
        elif feedback == "lower":
            self.high = min(self.high, guess - 1)

# Рандомный выбор из непроверенных чисел
class RandomStrategy(GuessingStrategy):
    def __init__(self, low, high):
        super().__init__(low, high)
        self._used = set()

    def next_guess(self):
        candidates = [n for n in range(self.low, self.high + 1)
                      if n not in self._used]
        if not candidates:
            return None
        return random.choice(candidates)

    def update(self, guess, feedback):
        self._used.add(guess)
        if feedback == "higher":
            self.low = max(self.low, guess + 1)
        elif feedback == "lower":
            self.high = min(self.high, guess - 1)

# Последовательный перебор от low до high
class SequentialStrategy(GuessingStrategy):
    def __init__(self, low, high):
        super().__init__(low, high)
        self._current = low

    def next_guess(self):
        if self._current > self.high:
            return None
        guess = self._current
        self._current += 1
        return guess

    def update(self, guess, feedback):
        if feedback == "higher":
            self._current = max(self._current, guess + 1)
        elif feedback == "lower":
            self.high = min(self.high, guess - 1)



# Стратегия игрока с терминала
class TerminalStrategy(GuessingStrategy):
    def __init__(self, low: int = 0, high: int = 0):
        super().__init__(low, high)

    def next_guess(self):
        while True:
            try:
                return int(input("  Ваше предположение: "))
            except ValueError:
                print("  Введите целое число.")

    def update(self, guess, feedback):
        # человеку сообщения "больше/меньше" печатает менеджер
        pass

STRATEGY_FACTORY = {
    "1": ("Дихотомия",               DichotomyStrategy),
    "2": ("Случайный выбор",         RandomStrategy),
    "3": ("Последовательный выбор",  SequentialStrategy),
}

def create_strategy(choice: str, low: int, high: int) -> GuessingStrategy:
    return STRATEGY_FACTORY[choice][1](low, high)