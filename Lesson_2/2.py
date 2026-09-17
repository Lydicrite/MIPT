# Реализуйте функции:
# Создающая вектор заданной длины N, заполнение – случайные числа от 0..1
# Создающая матрицу MxN, заполнение – случайные числа 0..1
# Умножающая матрицу на вектор (см. предыдущее ДЗ)
# Печатающую матрицу
# Печатающую вектор
# Находящую сумму диагональных элементов матрицы
# Реализующая двумерную свертку изображения.

import random



# Случайный вектор длины N, uniform(0, 1)
def create_vector(N):
    return [random.uniform(0, 1) for _ in range(N)]

# Случайная матрица MxN, uniform(0, 1)
def create_matrix(M, N):
    return [[random.uniform(0, 1) for _ in range(N)] for _ in range(M)]

# Произведение матрицы на вектор
def matrix_vector_product(matrix, vector):
    if not matrix:
        return []

    m = len(matrix)
    n = len(matrix[0])

    if len(vector) != n:
        raise ValueError(f"Нельзя умножить матрицу {m}x{n} на вектор длины {len(vector)}")

    result = [sum(a * b for a, b in zip(row, vector)) for row in matrix]
    return result

# Декоратор для печати контейнера (матрица / вектор)
def print_container(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            print(result)
        return result
    return wrapper

# Печать матрицы
def print_matrix(matrix):
    for row in matrix:
        print_vector(row)

# Печать вектора
def print_vector(vector):
    print(vector)

# Сумма диагональных элементов матрицы
def sum_diagonal(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))

# Двумерная свёртка изображения
def convolve2d(image: list[list[float]], kernel: list[list[float]]) -> list[list[float]]:
    H = len(image)
    W = len(image[0])
    kh = len(kernel)
    kw = len(kernel[0])

    out_H = H - kh + 1
    out_W = W - kw + 1

    result = [[0.0] * out_W for _ in range(out_H)]

    for i in range(out_H):
        for j in range(out_W):
            s = 0.0
            for ki in range(kh):
                for kj in range(kw):
                    s += image[i + ki][j + kj] * kernel[ki][kj]
            result[i][j] = s

    return result



def main():
    print("Вектор: ")
    vec = create_vector(5)
    print_container(print_vector)(vec)
    print("\nМатрица: ")
    matrix_a = create_matrix(5, 5)
    print_container(print_matrix)(matrix_a)
    print("\nПроизведение матрицы на вектор: ")
    print(matrix_vector_product(matrix_a, vec))
    print("\nСумма диагональных элементов матрицы: {sum_diagonal(matrix_a)}")


    print("\nМатрица-ядро для свёртки: ")
    matrix_b = create_matrix(3, 3)
    print_container(print_matrix)(matrix_b)
    print("\nДвумерная свёртка изображения: ")
    print_container(print_matrix)(convolve2d(matrix_a, matrix_b))

if __name__ == "__main__":
    main()