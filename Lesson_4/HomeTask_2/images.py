from abc import ABC, abstractmethod
from copy import deepcopy

# Изображение
class Image(ABC):
    def __init__(self, pixels: list[list]):
        if not pixels or not pixels[0]:
            raise ValueError("Изображение не может быть пустым")
        if any(len(row) != len(pixels[0]) for row in pixels):
            raise ValueError("Все строки изображения должны иметь одинаковую длину")

        self._pixels = [
            [self._validate_pixel(pixel) for pixel in row]
            for row in pixels
        ]

    @staticmethod
    @abstractmethod
    def _validate_pixel(pixel):
        pass

    @property
    def width(self) -> int:
        return len(self._pixels[0])

    @property
    def height(self) -> int:
        return len(self._pixels)

    @property
    def pixels(self) -> list[list]:
        return deepcopy(self._pixels)

    def __getitem__(self, index: int) -> list:
        return self._pixels[index].copy()

    def __repr__(self) -> str:
        return "{}({!r})".format(type(self).__name__, self._pixels)


# Бин
class BinaryImage(Image):
    @staticmethod
    def _validate_pixel(pixel) -> int:
        if pixel not in (0, 1):
            raise ValueError("Бинарный пиксель должен быть равен 0 или 1")
        return int(pixel)

# ЧБ
class MonochromeImage(Image):
    @staticmethod
    def _validate_pixel(pixel) -> int:
        if isinstance(pixel, bool) or not isinstance(pixel, (int, float)):
            raise TypeError("Яркость пикселя должна быть числом")
        if not 0 <= pixel <= 255:
            raise ValueError("Яркость пикселя должна находиться в диапазоне 0..255")
        return round(pixel)

# Цветное
class ColorImage(Image):
    @staticmethod
    def _validate_pixel(pixel) -> tuple[int, int, int]:
        if not isinstance(pixel, (tuple, list)) or len(pixel) != 3:
            raise TypeError("Цветной пиксель должен содержать три канала RGB")
        if any(
            isinstance(channel, bool)
            or not isinstance(channel, (int, float))
            or not 0 <= channel <= 255
            for channel in pixel
        ):
            raise ValueError("Каналы RGB должны быть числами из диапазона 0..255")
        return tuple(round(channel) for channel in pixel)
