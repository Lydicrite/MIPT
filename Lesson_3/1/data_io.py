# Пишет и считывает векторы и матрицы в/из JSON-файл(а) ; записывает данные о выполнении операций (в т.ч. временные) в CSV-файл.

import csv
import json

def write_data(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, allow_nan=False)

def read_data(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def write_measurements(path, measurements):
    fields = [
        "operation", "dimensions", "seed", "number", "repeat",
        "mean_seconds", "min_seconds", "max_seconds",
    ]
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(measurements)
