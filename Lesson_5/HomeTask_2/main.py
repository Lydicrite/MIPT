import random
from logger import LogManager, LogLevel

def main():
    logger = LogManager("Log.txt")
    logger.debug("Система успешно запущена", source="System", version="1.0.0")
    logger.info("Начало демонстрации случайных исключений", source="Main")

    error_pool = [
        (lambda: 1 / 0,             LogLevel.FATAL, "Критический сбой вычислений!"),
        (lambda: int("не число"),   LogLevel.ERROR, "Ошибка парсинга строки в число"),
        (lambda: "текст" + 5,       LogLevel.ERROR, "Конфликт типов данных"),
        (lambda: [1, 2, 3][10],     LogLevel.WARN,  "Обращение к несуществующему индексу списка"),
        (lambda: {}["missing_key"], LogLevel.WARN,  "Ключ не найден в словаре")
    ]

    for i in range(1, 6):
        crash_func, level, message = random.choice(error_pool)
        try:
            crash_func()
        except Exception as e:
            logger.log(level, message, source="RandomGen", exc=e, iteration=i)

    logger.info("Демонстрация завершена, файл логов сохранен", source="Main")


if __name__ == "__main__":
    main()