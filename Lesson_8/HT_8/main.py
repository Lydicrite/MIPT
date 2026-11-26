import argparse
from pathlib import Path
import re

from PIL import Image, UnidentifiedImageError


IMAGE_EXTENSION = re.compile(r"\.(?:png|jpe?g|bmp|tiff?)", re.IGNORECASE | re.ASCII)
WHITE_PIXEL = re.compile(b"\xff")
DEFAULT_IMAGE = Path(__file__).resolve().parent / "images" / "example2.png"


def encode_image(image, block_size=16, threshold=128):
    # Вернуть строку кодов блоков и размеры сетки в порядке строк
    if block_size <= 0:
        raise ValueError("Размер блока должен быть положительным")
    if not 0 <= threshold <= 255:
        raise ValueError("Порог должен находиться в диапазоне от 0 до 255")

    width, height = image.size
    columns, rows = width // block_size, height // block_size
    if not columns or not rows:
        raise ValueError("Изображение меньше одного полного блока")

    binary = image.convert("L").point(
        [0 if value < threshold else 255 for value in range(256)]
    )
    codes = []
    for row in range(rows):
        for column in range(columns):
            left, top = column * block_size, row * block_size
            block = binary.crop((left, top, left + block_size, top + block_size))
            white_count = sum(1 for _ in WHITE_PIXEL.finditer(block.tobytes()))
            codes.append("1" if white_count > block_size * block_size / 2 else "0")
    return "".join(codes), columns, rows


def find_crosses(codes, columns, rows):
    # Найти все шаблоны крестика 101/000/101, включая перекрывающиеся
    if columns <= 0 or rows <= 0:
        raise ValueError("Размеры сетки должны быть положительными")
    if len(codes) != columns * rows or re.fullmatch(r"[01]+", codes) is None:
        raise ValueError("Строка кодов не соответствует размерам сетки")
    if columns < 3 or rows < 3:
        return []

    gap = columns - 3
    pattern = re.compile(rf"(?=(101[01]{{{gap}}}000[01]{{{gap}}}101))")
    return [
        divmod(match.start(), columns)
        for match in pattern.finditer(codes)
        if match.start() % columns <= columns - 3
    ]


def positive_integer(value):
    try:
        number = int(value)
        if number <= 0:
            raise ValueError
        return number
    except ValueError:
        raise argparse.ArgumentTypeError("Введите положительное целое число") from None


def threshold_value(value):
    try:
        number = int(value)
        if not 0 <= number <= 255:
            raise ValueError
        return number
    except ValueError:
        raise argparse.ArgumentTypeError("Введите целое число от 0 до 255") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", type=Path, default=DEFAULT_IMAGE,
                        help="Путь к изображению (по умолчанию images/example2.png)")
    parser.add_argument("--block-size", type=positive_integer, default=16,
                        help="Размер квадратного блока в пикселях (по умолчанию 16)")
    parser.add_argument("--threshold", type=threshold_value, default=128,
                        help="Порог бинаризации от 0 до 255 (по умолчанию 128)")
    args = parser.parse_args()

    if IMAGE_EXTENSION.fullmatch(args.image.suffix) is None:
        parser.error("Поддерживаются изображения PNG, JPG, JPEG, BMP, TIF и TIFF")

    try:
        with Image.open(args.image) as image:
            width, height = image.size
            codes, columns, rows = encode_image(image, args.block_size, args.threshold)
    except (OSError, UnidentifiedImageError, ValueError) as error:
        parser.error(str(error))

    crosses = find_crosses(codes, columns, rows)
    print(f"Изображение: {args.image}")
    print(f"Размер изображения: {width} x {height} пикселей")
    print(f"Сетка блоков: {columns} x {rows}; всего {len(codes)}")
    print(f"Исключено по краям: {width % args.block_size} столбцов, "
          f"{height % args.block_size} строк пикселей")
    print(f"\n4. Код изображения: {codes}")
    print("Сека кодов:")
    for row in re.findall(rf"[01]{{{columns}}}", codes):
        print(row)
    print(f"\n5. Количество шаблонов-крестов: {len(crosses)}")
    if crosses:
        print("Координаты верхнего левого блока (строка, столбец), с нуля:")
        print(", ".join(f"({row}, {column})" for row, column in crosses))


if __name__ == "__main__":
    main()

# python main.py
# python main.py images/example1.png --block-size 16 --threshold 128

# На первом изображении кресты на блоксайзе 73 (python main.py images/example1.png --block-size 73)
# На втором изображении кресты на блоксайзе 51 (python main.py images/example1.png --block-size 51)
# Если обрезать example_1, можно найти все 4 креста (python main.py images/test_2.png --block-size 75 --threshold 110)