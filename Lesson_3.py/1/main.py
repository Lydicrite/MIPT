# python "Lesson_3.py/1/main.py"

from pathlib import Path
from random import Random
from data_io import read_data, write_data, write_measurements
from matrix_operations import matrix_matrix_product, matrix_trace, matrix_vector_product
from timing import measure_time
from vector_operations import filter_vector, histogram, scalar_product

# Параметры вызова функций
SEED = 1375731
MATRIX_SIZES = (10, 50, 100)
VECTOR_SIZES = (100, 1000, 10000)
BIN_COUNTS = (5, 10, 20)
NUMBER = 5
REPEAT = 5
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

def create_vector(size, rng):
    return [rng.uniform(0, 1) for _ in range(size)]

def create_matrix(rows, columns, rng):
    return [create_vector(columns, rng) for _ in range(rows)]



# Демка работы функций
def demonstrate(output_dir):
    matrix_a = [[1, 2, 3], [4, 5, 6]]
    matrix_b = [[7, 8], [9, 10], [11, 12]]
    vector_a = [1, 2, 3]
    vector_b = [4, 5, 6]
    signal = [1, 4, 3, 7, 6, 8, 5, 9]
    kernel = [-1, 0, 1]

    results = {
        "matrix_matrix_product": matrix_matrix_product(matrix_a, matrix_b),
        "matrix_vector_product": matrix_vector_product(matrix_a, vector_a),
        "matrix_trace": matrix_trace([[1, 2], [3, 4]]),
        "scalar_product": scalar_product(vector_a, vector_b),
        "histogram": histogram(signal, 4),
        "filter_vector": filter_vector(signal, kernel),
    }
    for name, result in results.items():
        print(f"{name}: {result}")

    data = {"matrix": matrix_a, "vector": vector_a}
    path = output_dir / "example_data.json"
    write_data(path, data)
    restored = read_data(path)
    if restored != data:
        raise RuntimeError("Данные после JSON-преобразования изменились")
    print(f"read_data: {restored}")
    write_data(output_dir / "operation_results.json", results)



# Бенчмарки для измерения времени
def run_benchmarks(output_dir):
    rng = Random(SEED)
    measurements = []

    def record(operation, dimensions, function, *args):
        result = measure_time(function, *args, number=NUMBER, repeat=REPEAT)
        measurements.append({
            "operation": operation,
            "dimensions": dimensions,
            "seed": SEED,
            **result,
        })
        print(f"{operation:<24} {dimensions:<32} "
              f"{result['mean_seconds']:.9f} s")

    def record_io(data, kind, dimensions):
        path = output_dir / f"benchmark_{kind}.json"
        record(f"write_{kind}", dimensions, write_data, path, data)
        record(f"read_{kind}", dimensions, read_data, path)

    print("\nСреднее время вызова:")
    for size in MATRIX_SIZES:
        left = create_matrix(size, size, rng)
        right = create_matrix(size, size, rng)
        vector = create_vector(size, rng)
        shape = f"{size}x{size}"
        record("matrix_matrix_product", f"{shape} * {shape}",
               matrix_matrix_product, left, right)
        record("matrix_vector_product", f"{shape} * {size}",
               matrix_vector_product, left, vector)
        record("matrix_trace", shape, matrix_trace, left)
        record_io(left, "matrix", shape)

    kernel = [-1, 0, 1]
    for size in VECTOR_SIZES:
        left = create_vector(size, rng)
        right = create_vector(size, rng)
        record("scalar_product", f"N={size}", scalar_product, left, right)
        for bins in BIN_COUNTS:
            record("histogram", f"N={size}; bins={bins}",
                   histogram, left, bins)
        record("filter_vector", f"N={size}; kernel={len(kernel)}",
               filter_vector, left, kernel)
        record_io(left, "vector", f"N={size}")

    results_path = output_dir / "timings.csv"
    write_measurements(results_path, measurements)
    print(f"\nРезультаты измерений сохранены в файл {results_path}")
    return measurements



def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    demonstrate(OUTPUT_DIR)
    run_benchmarks(OUTPUT_DIR)

if __name__ == "__main__":
    main()
