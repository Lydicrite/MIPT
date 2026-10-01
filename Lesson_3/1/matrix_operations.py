# Матричные операции

def matrix_shape(matrix):
    if not matrix or not matrix[0]:
        raise ValueError("Матрица не должна быть пустой")

    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError("Все строки матрицы должны иметь одинаковую длину")
    return len(matrix), columns


def matrix_matrix_product(left, right):
    _, left_columns = matrix_shape(left)
    right_rows, _ = matrix_shape(right)
    if left_columns != right_rows:
        raise ValueError("Недопустимые размеры матриц для перемножения")

    columns = list(zip(*right))
    return [
        [sum(a * b for a, b in zip(row, column)) for column in columns]
        for row in left
    ]


def matrix_vector_product(matrix, vector):
    _, columns = matrix_shape(matrix)
    if len(vector) != columns:
        raise ValueError("Длина вектора должна совпадать с количеством столбцов матрицы")

    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def matrix_trace(matrix):
    rows, columns = matrix_shape(matrix)
    if rows != columns:
        raise ValueError("Матрица должна быть квадратной")
    return sum(matrix[i][i] for i in range(rows))
