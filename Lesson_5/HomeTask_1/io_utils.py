from pathlib import Path

from images import BinaryImage, ColorImage, Image, MonochromeImage


class ImageIOError(Exception):
    """Ошибка чтения/записи файла с изображением."""

# Все данные файла (как токены) + проверка корректности пути
def _read_tokens(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="ascii").split()
    except FileNotFoundError as error:
        raise ImageIOError(f"Файл не найден: {path}") from error
    except IsADirectoryError as error:
        raise ImageIOError(f"Это каталог, а не файл: {path}") from error
    except PermissionError as error:
        raise ImageIOError(f"Нет прав на чтение: {path}") from error
    except UnicodeDecodeError as error:
        raise ImageIOError(f"Файл не является текстовым: {path}") from error
    except OSError as error:
        raise ImageIOError(f"Ошибка чтения {path}: {error}") from error

# Загрузка изображения по P*
def load_image(path: Path) -> Image:
    tokens = _read_tokens(path)
    if not tokens:
        raise ImageIOError(f"Пустой файл: {path}")
    magic = tokens[0]
    if magic == "P1":
        return _load_pbm(tokens, path)
    if magic == "P2":
        return _load_pgm(tokens, path)
    if magic == "P3":
        return _load_ppm(tokens, path)
    raise ImageIOError(f"Неизвестный формат {magic!r} в {path}")

# Заголовок: P*, ширина, высота, (максимальный числовой уровень)
def _parse_header(tokens: list[str], path: Path) -> tuple[int, int, int]:
    if len(tokens) < 4:
        raise ImageIOError(f"Обрезанный заголовок в {path}")
    try:
        width = int(tokens[1])
        height = int(tokens[2])
    except ValueError as error:
        raise ImageIOError(f"Некорректные размеры в {path}") from error
    if width <= 0 or height <= 0:
        raise ImageIOError(f"Размеры должны быть положительными в {path}")
    return width, height, 3


# Бин
def _load_pbm(tokens, path):
    width, height, _ = _parse_header(tokens, path)
    data = tokens[3:]
    if len(data) != width * height:
        raise ImageIOError(
            f"Ожидалось {width * height} пикселей, получено {len(data)}"
        )
    try:
        values = [int(token) for token in data]
    except ValueError as error:
        raise ImageIOError(f"Некорректные пиксели в {path}") from error
    pixels = [values[i * width:(i + 1) * width] for i in range(height)]
    return BinaryImage([[1 - v for v in row] for row in pixels])

# ЧБ
def _load_pgm(tokens, path):
    width, height, _ = _parse_header(tokens, path)
    if len(tokens) < 5:
        raise ImageIOError(f"Обрезанный заголовок в {path}")
    data = tokens[4:]
    if len(data) != width * height:
        raise ImageIOError(
            f"Ожидалось {width * height} пикселей, получено {len(data)}"
        )
    try:
        values = [int(token) for token in data]
    except ValueError as error:
        raise ImageIOError(f"Некорректные пиксели в {path}") from error
    pixels = [values[i * width:(i + 1) * width] for i in range(height)]
    return MonochromeImage(pixels)

# Цветное
def _load_ppm(tokens, path):
    width, height, _ = _parse_header(tokens, path)
    if len(tokens) < 5:
        raise ImageIOError(f"Обрезанный заголовок в {path}")
    data = tokens[4:]
    if len(data) != width * height * 3:
        raise ImageIOError(
            f"Ожидалось {width * height * 3} значений, получено {len(data)}"
        )
    try:
        values = [int(token) for token in data]
    except ValueError as error:
        raise ImageIOError(f"Некорректные пиксели в {path}") from error
    pixels = []
    idx = 0
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append((values[idx], values[idx + 1], values[idx + 2]))
            idx += 3
        pixels.append(row)
    return ColorImage(pixels)



def save_image(image: Image, path: Path) -> None:
    if not isinstance(image, (BinaryImage, MonochromeImage, ColorImage)):
        raise TypeError(
            "Сохранять можно только Binary/Monochrome/Color изображения, "
            "получено {}".format(type(image).__name__)
        )

    # Эталонное расширение для данного типа изображения
    expected_extension = type(image)._extension()
    
    actual_extension = path.suffix.lower()
    if actual_extension != expected_extension:
        raise ImageIOError(
            "Расширение файла {} не соответствует типу {}: "
            "ожидалось {}, получено {}".format(
                path, type(image).__name__,
                expected_extension, actual_extension or "<пусто>",
            )
        )

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise ImageIOError(
            "Не удалось создать каталог {}: {}".format(path.parent, error)
        ) from error

    if isinstance(image, BinaryImage):
        header = "P1\n{} {}\n".format(image.width, image.height)
        rows = [
            " ".join("0" if pixel else "1" for pixel in row)
            for row in image.pixels
        ]
    elif isinstance(image, MonochromeImage):
        header = "P2\n{} {}\n255\n".format(image.width, image.height)
        rows = [" ".join(map(str, row)) for row in image.pixels]
    else:
        header = "P3\n{} {}\n255\n".format(image.width, image.height)
        rows = [
            " ".join(str(channel) for pixel in row for channel in pixel)
            for row in image.pixels
        ]

    try:
        path.write_text(header + "\n".join(rows) + "\n", encoding="ascii")
    except PermissionError as error:
        raise ImageIOError("Нет прав на запись: {}".format(path)) from error
    except IsADirectoryError as error:
        raise ImageIOError("Это каталог, а не файл: {}".format(path)) from error
    except OSError as error:
        raise ImageIOError(
            "Ошибка записи {}: {}".format(path, error)
        ) from error