from functools import partial
from statistics import mean
from timeit import repeat as timeit_repeat

# Измерение времени (среднее, min/max) работы функций
# Передаются количество повторов в серии и количество серий
def measure_time(function, *args, number=3, repeat=3, **kwargs):
    for value in (number, repeat):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("Количество повторов в серии и количество серий должны быть положительными целыми числами")

    elapsed = timeit_repeat(
        partial(function, *args, **kwargs), number=number, repeat=repeat
    )
    per_call = [seconds / number for seconds in elapsed]
    return {
        "number": number,
        "repeat": repeat,
        "mean_seconds": mean(per_call),
        "min_seconds": min(per_call),
        "max_seconds": max(per_call),
    }
