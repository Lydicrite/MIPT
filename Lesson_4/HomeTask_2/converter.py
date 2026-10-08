from math import sqrt
from statistics import mean, pstdev

from images import BinaryImage, ColorImage, MonochromeImage


class ImageConverter:
    @staticmethod
    def _correct(values: list[int], reference: list[int]) -> list[int]:
        source_mean, reference_mean = mean(values), mean(reference)
        source_std, reference_std = pstdev(values), pstdev(reference)
        if source_std == 0:
            return [round(reference_mean)] * len(values)
        return [
            round(max(0, min(255, (value - source_mean) * reference_std
                                 / source_std + reference_mean)))
            for value in values
        ]





    # Бинарное изображение -> бинарное изображение
    @staticmethod
    def binary_to_binary(image: BinaryImage) -> BinaryImage:
        return BinaryImage(image.pixels)

    # Бинарное изображение -> монохромное изображение
    @staticmethod
    def binary_to_monochrome(image: BinaryImage) -> MonochromeImage:
        white = [
            (y, x)
            for y, row in enumerate(image.pixels)
            for x, pixel in enumerate(row)
            if pixel == 1
        ]
        if not white:
            raise ValueError("Требуется хотя бы один белый пиксель")

        distances = [
            [min(sqrt((y - wy) ** 2 + (x - wx) ** 2)
                 for wy, wx in white)
             for x in range(image.width)]
            for y in range(image.height)
        ]
        maximum = max(max(row) for row in distances)
        if maximum == 0:
            return MonochromeImage(distances)
        return MonochromeImage([
            [distance * 255 / maximum for distance in row]
            for row in distances
        ])

    # Бинарное изображение -> цветное изображение
    @classmethod
    def binary_to_color(
        cls,
        image: BinaryImage,
        palette: dict[int, tuple[int, int, int]] | list[tuple[int, int, int]],
    ) -> ColorImage:
        return cls.monochrome_to_color(
            cls.binary_to_monochrome(image), palette
        )





    # Монохромное изображение -> монохромное изображение
    @classmethod
    def monochrome_to_monochrome(
        cls, image: MonochromeImage, reference: MonochromeImage
    ) -> MonochromeImage:
        values = [pixel for row in image.pixels for pixel in row]
        sample = [pixel for row in reference.pixels for pixel in row]
        corrected = iter(cls._correct(values, sample))
        return MonochromeImage([
            [next(corrected) for _ in range(image.width)]
            for _ in range(image.height)
        ])

    # Монохромное изображение -> бинарное изображение
    @staticmethod
    def monochrome_to_binary(
        image: MonochromeImage, threshold: int | None = None
    ) -> BinaryImage:
        if threshold is None:
            threshold = round(mean(
                pixel for row in image.pixels for pixel in row
            ))
        if not 0 <= threshold <= 255:
            raise ValueError("Порог должен находиться в диапазоне 0..255")
        return BinaryImage([
            [int(pixel >= threshold) for pixel in row]
            for row in image.pixels
        ])

    # Монохромное изображение -> цветное изображение
    @staticmethod
    def monochrome_to_color(
        image: MonochromeImage,
        palette: dict[int, tuple[int, int, int]] | list[tuple[int, int, int]],
    ) -> ColorImage:
        try:
            return ColorImage([
                [palette[pixel] for pixel in row]
                for row in image.pixels
            ])
        except (KeyError, IndexError) as error:
            raise ValueError("В палитре отсутствует требуемый оттенок серого") from error





    # Цветное изображение -> бинарное изображение
    @classmethod
    def color_to_binary(
        cls, image: ColorImage, threshold: int | None = None
    ) -> BinaryImage:
        return cls.monochrome_to_binary(
            cls.color_to_monochrome(image), threshold
        )

    # Цветное изображение -> монохромное изображение
    @staticmethod
    def color_to_monochrome(image: ColorImage) -> MonochromeImage:
        return MonochromeImage([
            [sum(pixel) / 3 for pixel in row]
            for row in image.pixels
        ])

    # Цветное изображение -> цветное изображение
    @classmethod
    def color_to_color(
        cls, image: ColorImage, reference: ColorImage
    ) -> ColorImage:
        pixels = [pixel for row in image.pixels for pixel in row]
        sample = [pixel for row in reference.pixels for pixel in row]
        channels = [
            iter(cls._correct(
                [pixel[channel] for pixel in pixels],
                [pixel[channel] for pixel in sample],
            ))
            for channel in range(3)
        ]
        return ColorImage([
            [tuple(next(channel) for channel in channels)
             for _ in range(image.width)]
            for _ in range(image.height)
        ])