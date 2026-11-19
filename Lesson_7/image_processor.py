import numpy as np
from PIL import Image
from functools import partial
from itertools import groupby
from operator import itemgetter
from pathlib import Path


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

# ---------- Ядра - ленивые фабрики ----------

def create_kernel_2d(kernel_func):
    """Возвращает фабрику ядра"""
    return kernel_func

def average_filter_2d(size):
    """Ленивая фабрика: ядро создается только при вызове make_kernel()"""
    def make_kernel():
        return np.ones((size, size)) / (size * size)
    return make_kernel

def _gaussian_rows(size, sigma):
    """Ленивый генератор строк ядра Гаусса"""
    half = size // 2

    def gaussian(x, y):
        return np.exp(-(x**2 + y**2) / (2 * sigma**2))

    for i in range(size):
        yield np.array([gaussian(i - half, j - half) for j in range(size)])

def gaussian_filter_2d(size, sigma):
    """Ленивая фабрика: строки генерируются лениво, ядро собирается при вызове"""
    def make_kernel():
        kernel = np.array(list(_gaussian_rows(size, sigma)))
        return kernel / kernel.sum()
    return make_kernel


# ---------- Ленивый итератор координат ----------

def linear_iterator(height, width):
    """Ленивый генератор координат пикселей"""
    for i in range(height):
        for j in range(width):
            yield i, j


# ---------- Ленивая свертка ----------

def lazy_convolve_pixels(img, kernel, iterator_func):
    """
    Ленивый генератор, выдает (i, j, value) по мере обхода
    Ничего не вычисляется, не начнётся итерирование
    """
    kernel_size = kernel.shape[0]
    half = kernel_size // 2
    height, width = img.shape[:2]
    is_color = img.ndim == 3
    channels = img.shape[2] if is_color else 1

    if is_color:
        padded = [np.pad(img[:, :, c], half, mode='constant') for c in range(channels)]
    else:
        padded = [np.pad(img, half, mode='constant')]

    for i, j in iterator_func(height, width):
        if is_color:
            value = np.empty(channels)
            for c in range(channels):
                region = padded[c][i:i + kernel_size, j:j + kernel_size]
                value[c] = np.sum(region * kernel)
            yield i, j, value
        else:
            region = padded[0][i:i + kernel_size, j:j + kernel_size]
            yield i, j, np.sum(region * kernel)

def materialize(pixel_stream, shape, channels=None):
    """Собирает ленивый поток (i, j, value) в массив"""
    if channels is not None:
        result = np.zeros((*shape, channels))
    else:
        result = np.zeros(shape)
    for i, j, value in pixel_stream:
        result[i, j] = value
    return result

def apply_convolution(img, kernel, iterator_func):
    """Обертка над ленивой сверткой"""
    height, width = img.shape[:2]
    channels = img.shape[2] if img.ndim == 3 else None
    stream = lazy_convolve_pixels(img, kernel, iterator_func)
    return materialize(stream, (height, width), channels)



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
    image_path = Path(__file__).resolve().parent / "image.jpg"
    output_path = "Lesson_7/output_grayscale.jpg"
    img = load_image(image_path)
    print(f"Размер исходного изображения: {img.shape}")
    


    # Задание 2: Конвертация в оттенки серого
    print("\n2: Конвертация в оттенки серого")
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
    
    # Усреднение 3x3
    avg_kernel = average_filter_2d(3)()
    avg_filter = partial(apply_convolution, kernel=avg_kernel, iterator_func=linear_iterator)
    filtered_avg = avg_filter(img)
    save_image(filtered_avg, "Lesson_7/output_average.jpg")

    # Гаусс 5x5
    gauss_kernel = gaussian_filter_2d(5, 1.0)()
    gauss_filter = partial(apply_convolution, kernel=gauss_kernel, iterator_func=linear_iterator)
    filtered_gauss = gauss_filter(img)
    save_image(filtered_gauss, "Lesson_7/output_gaussian.jpg")
    


    # Задание 4: Сравнение результатов
    print("\n4: Сравнение результатов")
    kernel = gaussian_filter_2d(3, 0.8)()
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
