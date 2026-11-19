from math import isfinite


def count_levels(levels):
    counts = dict.fromkeys(range(256), 0)
    for level in levels:
        if not isinstance(level, int) or not 0 <= level <= 255:
            raise ValueError("Уровни должны быть целыми числами в интервале: [0, 255]")
        counts[level] += 1
    return counts


def validate_histogram(data):
    if not isinstance(data, dict):
        raise ValueError("Гистограмма должна быть словарем")
    result = dict.fromkeys(range(256), 0)
    for level, value in data.items():
        if not isinstance(level, int) or not 0 <= level <= 255:
            raise ValueError("Ключи гистограммы должны быть целыми числами в интервале: [0, 255]")
        if not isinstance(value, (int, float)) or not isfinite(value) or value < 0:
            raise ValueError("Значения гистограммы должны быть конечными и неотрицательными")
        result[level] = value
    return result


def normalize_histogram(data):
    data = validate_histogram(data)
    total = sum(data.values())
    if not isfinite(total) or total <= 0:
        raise ValueError("Нельзя нормализовать пустую гистограмму")
    return {level: value / total for level, value in data.items()}
