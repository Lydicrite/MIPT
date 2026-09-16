import random

def random_vector(N):
    return [random.randint(-100, 100) for _ in range(N)]

def matrix_vector_product(matrix, vector):
    result = [sum(a * b for a, b in zip(row, vector)) for row in matrix]
    return result

def main():
    N = 3
    matrix = [random_vector(N), random_vector(N)]
    vector = random_vector(N)
    result = matrix_vector_product(matrix, vector)
    print(matrix)
    print(vector)
    print(result)

if __name__ == "__main__":
    main()
