import random
from functools import wraps

# Декоратор поканальной обработки
def per_channel(func):
    @wraps(func)
    def wrapper(image, *args, **kwargs):
        # Одноканальное изображение, если image[i][j] — число
        if not isinstance(image[0][0], list):
            return func(image, *args, **kwargs)

        # Многоканальное изображение [M][N][C]
        M = len(image)
        N = len(image[0])
        C = len(image[0][0])

        # Обрабатываем каждый канал отдельно
        filtered_channels = []
        for c in range(C):
            channel = [[image[i][j][c] for j in range(N)] for i in range(M)]
            filtered_channels.append(func(channel, *args, **kwargs))

        # Собираем каналы обратно в [M'][N'][C]
        out_M = len(filtered_channels[0])
        out_N = len(filtered_channels[0][0])
        result = [
            [
                [filtered_channels[c][i][j] for c in range(C)]
                for j in range(out_N)
            ]
            for i in range(out_M)
        ]
        return result

    return wrapper

# Двумерная свёртка изображения
@per_channel
def convolve2d(image: list[list[float]], kernel: list[list[float]]) -> list[list[float]]:
    H = len(image)
    W = len(image[0])
    kh = len(kernel)
    kw = len(kernel[0])

    out_H = H - kh + 1
    out_W = W - kw + 1

    if out_H <= 0 or out_W <= 0:
        raise ValueError("Ядро больше изображения")

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
    M, N, C = 6, 6, 3
    img = [
        [[random.randint(0, 255) for _ in range(C)] for _ in range(N)]
        for _ in range(M)
    ]
    
    kernel = [[1.0 / 9.0] * 3 for _ in range(3)]

    filtered = convolve2d(img, kernel)

    print("Исходное изображение:", M, "x", N, "x", C)
    print("После фильтрации:",
          len(filtered), "x", len(filtered[0]), "x", len(filtered[0][0]))
    print("Первый пиксель по каналам:", filtered[0][0])

if __name__ == "__main__":
    main()