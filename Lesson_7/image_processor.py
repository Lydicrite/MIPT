import numpy as np
from PIL import Image
from functools import partial
from itertools import groupby
from operator import itemgetter


def load_image(path):
    return np.array(Image.open(path))

def save_image(arr, path):
    Image.fromarray(arr.astype(np.uint8)).save(path)

def to_grayscale_lambda(img):
    if len(img.shape) == 3:
        # Лямбда-функция для преобразования RGB в серый
        rgb_to_gray = lambda r, g, b: 0.299 * r + 0.587 * g + 0.114 * b
        # Применяем функцию к каждому пикселю
        gray = np.array([
            [rgb_to_gray(pixel[0], pixel[1], pixel[2]) for pixel in row]
            for row in img
        ], dtype=np.uint8)
        return gray
    return img



# -------------------------- Итераторы обхода -------------------------- 

# Последовательный обход строк
def linear_iterator(height, width):
    return ((i, j) for i in range(height) for j in range(width))

# Обход по спирали из центра изображения
def spiral_iterator(height, width):

    center_i, center_j = height // 2, width // 2
    
    def get_spiral_coords():
        yield center_i, center_j
        
        for layer in range(1, max(height, width)):
            # Верхняя
            i = center_i - layer
            for j in range(center_j - layer, center_j + layer + 1):
                if 0 <= i < height and 0 <= j < width:
                    yield i, j
            
            # Правая
            j = center_j + layer
            for i in range(center_i - layer + 1, center_i + layer + 1):
                if 0 <= i < height and 0 <= j < width:
                    yield i, j
            
            # Нижняя
            i = center_i + layer
            for j in range(center_j + layer - 1, center_j - layer - 1, -1):
                if 0 <= i < height and 0 <= j < width:
                    yield i, j
            
            # Левая
            j = center_j - layer
            for i in range(center_i + layer - 1, center_i - layer, -1):
                if 0 <= i < height and 0 <= j < width:
                    yield i, j
    
    return get_spiral_coords()

# Диагональный обход с чередованием направления
def zigzag_iterator(height, width):
    def get_zigzag_coords():
        for diagonal in range(height + width - 1):
            if diagonal % 2 == 0:
                # Четные диагонали - идем вверх
                for i in range(min(diagonal, height - 1), max(0, diagonal - width + 1) - 1, -1):
                    j = diagonal - i
                    if 0 <= j < width:
                        yield i, j
            else:
                # Нечетные диагонали - идем вниз
                for i in range(max(0, diagonal - width + 1), min(diagonal + 1, height)):
                    j = diagonal - i
                    if 0 <= j < width:
                        yield i, j
    
    return get_zigzag_coords()

# Кривая Пеано
def peano_iterator(height, width):

    def peano_curve(x, y, size, orientation):
        if size == 1:
            if 0 <= x < height and 0 <= y < width:
                yield x, y
            return
        
        third = size // 3
        
        if third == 0:
            if 0 <= x < height and 0 <= y < width:
                yield x, y
            return
        
        if orientation == 0:
            # Нормальная ориентация
            yield from peano_curve(x, y, third, 1)
            yield from peano_curve(x, y + third, third, 0)
            yield from peano_curve(x, y + 2*third, third, 0)
            yield from peano_curve(x + third, y + 2*third, third, 2)
            yield from peano_curve(x + third, y + third, third, 0)
            yield from peano_curve(x + third, y, third, 2)
            yield from peano_curve(x + 2*third, y, third, 2)
            yield from peano_curve(x + 2*third, y + third, third, 1)
            yield from peano_curve(x + 2*third, y + 2*third, third, 0)
        elif orientation == 1:
            # 90 градусов
            yield from peano_curve(x, y + 2*third, third, 0)
            yield from peano_curve(x, y + third, third, 1)
            yield from peano_curve(x, y, third, 1)
            yield from peano_curve(x + third, y, third, 3)
            yield from peano_curve(x + third, y + third, third, 1)
            yield from peano_curve(x + third, y + 2*third, third, 3)
            yield from peano_curve(x + 2*third, y + 2*third, third, 3)
            yield from peano_curve(x + 2*third, y + third, third, 0)
            yield from peano_curve(x + 2*third, y, third, 1)
        elif orientation == 2:
            # 180 градусов
            yield from peano_curve(x + 2*third, y + 2*third, third, 3)
            yield from peano_curve(x + 2*third, y + third, third, 2)
            yield from peano_curve(x + 2*third, y, third, 2)
            yield from peano_curve(x + third, y, third, 0)
            yield from peano_curve(x + third, y + third, third, 2)
            yield from peano_curve(x + third, y + 2*third, third, 0)
            yield from peano_curve(x, y + 2*third, third, 0)
            yield from peano_curve(x, y + third, third, 1)
            yield from peano_curve(x, y, third, 2)
        elif orientation == 3:
            # 270 градусов
            yield from peano_curve(x + 2*third, y, third, 2)
            yield from peano_curve(x + 2*third, y + third, third, 3)
            yield from peano_curve(x + 2*third, y + 2*third, third, 3)
            yield from peano_curve(x + third, y + 2*third, third, 1)
            yield from peano_curve(x + third, y + third, third, 3)
            yield from peano_curve(x + third, y, third, 1)
            yield from peano_curve(x, y, third, 1)
            yield from peano_curve(x, y + third, third, 0)
            yield from peano_curve(x, y + 2*third, third, 3)

    size = 1
    while size < max(height, width):
        size *= 3
    
    return peano_curve(0, 0, size, 0)

def apply_iterator(img, iterator_func):
    height, width = img.shape[:2]
    coords = list(iterator_func(height, width))
    
    if len(img.shape) == 3:
        values = [tuple(img[i, j]) for i, j in coords]
    else:
        values = [img[i, j] for i, j in coords]
    
    return values, coords


# -------------------------- Свёрточные операторы -------------------------- 

def create_kernel_2d(kernel_func):
    return kernel_func

def average_filter_2d(size):
    return lambda: np.ones((size, size)) / (size * size)

def gaussian_filter_2d(size, sigma):
    def gaussian(x, y):
        return np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    half = size // 2
    kernel = np.array([
        [gaussian(i - half, j - half) for j in range(size)]
        for i in range(size)
    ])
    return kernel / kernel.sum()

def apply_convolution(img, kernel, iterator_func):
    kernel_size = kernel.shape[0]
    half = kernel_size // 2
    
    # Добавляем отступы
    padded = np.pad(img, half, mode='constant', constant_values=0)
    
    height, width = img.shape[:2]
    
    def convolve_pixel(i, j):
        """Вычисляет свертку для одного пикселя."""
        region = padded[i:i + kernel_size, j:j + kernel_size]
        return np.sum(region * kernel)
    
    # Создаем результат
    if len(img.shape) == 3:
        result = np.zeros_like(img)
        for c in range(img.shape[2]):
            channel = img[:, :, c]
            padded_c = np.pad(channel, half, mode='constant', constant_values=0)
            for i, j in iterator_func(height, width):
                region = padded_c[i:i + kernel_size, j:j + kernel_size]
                result[i, j, c] = np.sum(region * kernel)
    else:
        result = np.zeros_like(img)
        for i, j in iterator_func(height, width):
            region = padded[i:i + kernel_size, j:j + kernel_size]
            result[i, j] = np.sum(region * kernel)
    
    return result


# -------------------------- Метрики -------------------------- 

def mse(img1, img2):
    return np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2)

def compare_by_iterator(img, iterator_funcs):
    results = {}
    
    for name, iterator_func in iterator_funcs.items():
        values, coords = apply_iterator(img, iterator_func)
        results[name] = values
    
    comparisons = {}
    names = list(results.keys())
    
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            v1 = np.array(results[names[i]])
            v2 = np.array(results[names[j]])
            if v1.shape == v2.shape:
                comparisons[f"{names[i]}-{names[j]}"] = mse(v1, v2)
    
    return comparisons





if __name__ == "__main__":
    image_path = "image.jpg"
    output_path = "output_grayscale.jpg"
    img = load_image(image_path)
    print(f"Размер исходного изображения: {img.shape}")
    


    # Задание 1: Конвертация в оттенки серого
    print("\n1: Конвертация в оттенки серого")
    gray_img = to_grayscale_lambda(img)
    save_image(gray_img, output_path)
    print(f"Изображение сохранено в {output_path}")
    


    # Задание 1: Итераторы обхода
    print("\n1: Итераторы обхода")
    iterators = {
        "linear": linear_iterator,
        "spiral": spiral_iterator,
        "zigzag": zigzag_iterator,
        "peano": peano_iterator
    }
    for name, iterator_func in iterators.items():
        values, coords = apply_iterator(gray_img, iterator_func)
        print(f"{name}: {len(values)} пикселей")
    


    # Задание 3: Сверточные операторы
    print("\n3: Сверточные операторы")
    
    # Фильтр усреднения 3x3
    avg_kernel = average_filter_2d(3)
    avg_filter = partial(apply_convolution, kernel=avg_kernel(), iterator_func=linear_iterator)
    filtered_avg = avg_filter(img)
    save_image(filtered_avg, "output_average.jpg")
    print("Фильтр усреднения сохранен в output_average.jpg")
    
    # Фильтр Гаусса 5x5
    gauss_kernel = gaussian_filter_2d(5, 1.0)
    gauss_filter = partial(apply_convolution, kernel=gauss_kernel, iterator_func=linear_iterator)
    filtered_gauss = gauss_filter(img)
    save_image(filtered_gauss, "output_gaussian.jpg")
    print("Фильтр Гаусса сохранен в output_gaussian.jpg")
    


    # Задание 4: Сравнение результатов
    print("\n4: Сравнение результатов")
    kernel = gaussian_filter_2d(3, 0.8)
    filtered_results = {}
    for name, iterator_func in iterators.items():
        filtered = apply_convolution(gray_img, kernel, iterator_func)
        filtered_results[name] = filtered
        print(f"{name}: MSE = {mse(gray_img, filtered):.6f}")
    
    # Сравнение между итераторами
    comparisons = compare_by_iterator(gray_img, iterators)
    print("\nСравнение итераторов:")
    for pair, error in comparisons.items():
        print(f"  {pair}: MSE = {error:.10f}")
