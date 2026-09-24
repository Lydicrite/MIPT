# Векторные операции    
from math import isfinite



def scalar_product(left, right):
    if len(left) != len(right):
        raise ValueError("Векторы должны иметь одинаковую длину")
    return sum(a * b for a, b in zip(left, right))


def histogram(vector, bins=10):
    if isinstance(bins, bool) or not isinstance(bins, int) or bins <= 0:
        raise ValueError("Количество бинов должно быть положительным целым числом")
    if not vector:
        raise ValueError("Исторограмма требует не пустого вектора")
    if not all(isfinite(value) for value in vector):
        raise ValueError("Исторограмма требует конечных значений")

    low, high = min(vector), max(vector)
    if low == high:
        low -= 0.5
        high += 0.5
    width = (high - low) / bins
    if not isfinite(width) or width <= 0:
        raise ValueError("Количество бинов должно быть положительным целым числом")

    edges = [low + i * width for i in range(bins)] + [high]
    counts = [0] * bins
    for value in vector:
        index = min(int((value - low) / width), bins - 1)
        counts[index] += 1
    return counts, edges


def filter_vector(vector, kernel):
    if not kernel:
        raise ValueError("Ядро не должно быть пустым")
    if len(kernel) > len(vector):
        raise ValueError("Ядро не должно быть длиннее вектора")

    return [
        sum(vector[i + j] * kernel[j] for j in range(len(kernel)))
        for i in range(len(vector) - len(kernel) + 1)
    ]
