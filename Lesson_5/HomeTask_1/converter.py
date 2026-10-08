# ------------------------------------------------------  ------------------------------------------------------
from math import sqrt
from statistics import mean, pstdev

from images import BinaryImage, MonochromeImage, ColorImage

class ConversionError(Exception):
    """Ошибка преобразования изображения."""

class ImageConverter:
    # ------------------------------------------------------ Методы для проверки корректности ------------------------------------------------------
    @staticmethod
    def _require(image, expected_type, name: str = "image") -> None:
        if not isinstance(image, expected_type):
            raise TypeError(
                "{} должен быть {}, получено {}".format(
                    name, expected_type.__name__, type(image).__name__
                )
            )

    @staticmethod
    def _require_same_size(a, b, name_a: str = "image",
                           name_b: str = "reference") -> None:
        if (a.width, a.height) != (b.width, b.height):
            raise ConversionError(
                "Размеры {} и {} не совпадают: {}x{} и {}x{}".format(
                    name_a, name_b,
                    a.width, a.height, b.width, b.height,
                )
            )

    @staticmethod
    def _require_palette(palette) -> None:
        if isinstance(palette, dict):
            missing = [v for v in range(256) if v not in palette]
            if missing:
                preview = ", ".join(map(str, missing[:5]))
                if len(missing) > 5:
                    preview += ", ..."
                raise ConversionError(
                    "В палитре отсутствуют оттенки серого: {}".format(preview)
                )
        elif isinstance(palette, list):
            if len(palette) < 256:
                raise ConversionError(
                    "В списке-палитре должно быть не менее 256 цветов, "
                    "получено {}".format(len(palette))
                )
        else:
            raise TypeError(
                "Палитра должна быть dict или list, получено {}".format(
                    type(palette).__name__
                )
            )

    @staticmethod
    def _correct(values: list, reference: list) -> list:
        if not values:
            raise ConversionError("Пустой список значений для коррекции")
        if not reference:
            raise ConversionError("Пустой эталонный список значений")
        if len(values) != len(reference):
            raise ConversionError(
                "Разные длины списков: {} и {}".format(
                    len(values), len(reference)
                )
            )

        source_mean, reference_mean = mean(values), mean(reference)
        source_std, reference_std = pstdev(values), pstdev(reference)

        if source_std == 0:
            result = [round(reference_mean)] * len(values)
        else:
            result = [
                round(max(0, min(255, (value - source_mean) * reference_std
                                     / source_std + reference_mean)))
                for value in values
            ]

        # Проверка целостности
        if any(not 0 <= value <= 255 for value in result):
            raise ConversionError(
                "Результат коррекции вышел за границы диапазона 0..255"
            )
        return result




# ------------------------------------------------------ Бинарные изображения ------------------------------------------------------
    # Бинарное изображение -> бинарное изображение
    @staticmethod
    def binary_to_binary(image: BinaryImage) -> BinaryImage:
        ImageConverter._require(image, BinaryImage)
        return BinaryImage(image.pixels)

    # Бинарное изображение -> монохромное изображение
    # (градиент ЧБ в зависимости от минимального расстояния до белого пикселя)
    @staticmethod
    def binary_to_monochrome(image: BinaryImage) -> MonochromeImage:
        ImageConverter._require(image, BinaryImage)
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
        
        result = [
            [distance * 255 / maximum for distance in row]
            for row in distances
        ]

        if any(not 0 <= value <= 255 for row in result for value in row):
            raise ConversionError(
                "Был выход за границы диапазона 0...255"
            )
        return MonochromeImage(result)

    # Бинарное изображение -> цветное изображение
    @classmethod
    def binary_to_color(
        cls,
        image: BinaryImage,
        palette: dict[int, tuple[int, int, int]] | list[tuple[int, int, int]],
    ) -> ColorImage:
        cls._require(image, BinaryImage)
        return cls.monochrome_to_color(
            cls.binary_to_monochrome(image), palette
        )




# ------------------------------------------------------ ЧБ изображения ------------------------------------------------------
    # Монохромное изображение -> бинарное изображение
    # (итог: Ч или Б пиксель в зависимости от порога)
    @staticmethod
    def monochrome_to_binary(
        image: MonochromeImage, threshold: int | None = None
    ) -> BinaryImage:
        ImageConverter._require(image, MonochromeImage)

        if threshold is None:
            threshold = round(mean(
                pixel for row in image.pixels for pixel in row
            ))
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool):
            raise TypeError("Порог должен быть числом")
        if not 0 <= threshold <= 255:
            raise ConversionError("Порог должен находиться в диапазоне 0...255")

        return BinaryImage([
            [int(pixel >= threshold) for pixel in row]
            for row in image.pixels
        ])

    # Монохромное изображение -> монохромное изображение
    # (статистическая цветокоррекция через _correct с изображением того же типа)
    @classmethod
    def monochrome_to_monochrome(
        cls, image: MonochromeImage, reference: MonochromeImage
    ) -> MonochromeImage:
        cls._require(image, MonochromeImage)
        cls._require(reference, MonochromeImage, "reference")
        cls._require_same_size(image, reference)

        values = [pixel for row in image.pixels for pixel in row]
        sample = [pixel for row in reference.pixels for pixel in row]
        corrected = iter(cls._correct(values, sample))

        result = [
            [next(corrected) for _ in range(image.width)]
            for _ in range(image.height)
        ]
        if any(not 0 <= value <= 255 for row in result for value in row):
            raise ConversionError(
                "Результат преобразования вышел за границы диапазона 0...255"
            )
        return MonochromeImage(result)

    # Монохромное изображение -> цветное изображение
    # (замена цвета на яркость по palette, которая словарь или список кортежей)
    @staticmethod
    def monochrome_to_color(
        image: MonochromeImage,
        palette: dict[int, tuple[int, int, int]] | list[tuple[int, int, int]],
    ) -> ColorImage:
        ImageConverter._require(image, MonochromeImage)
        ImageConverter._require_palette(palette)

        try:
            return ColorImage([
                [palette[pixel] for pixel in row]
                for row in image.pixels
            ])
        except (KeyError, IndexError) as error:
            raise ConversionError("В палитре отсутствует требуемый оттенок серого") from error




# ------------------------------------------------------ Цветные изображения ------------------------------------------------------
    # Цветное изображение -> бинарное изображение
    @classmethod
    def color_to_binary(
        cls, image: ColorImage, threshold: int | None = None
    ) -> BinaryImage:
        cls._require(image, ColorImage)
        return cls.monochrome_to_binary(
            cls.color_to_monochrome(image), threshold
        )

    # Цветное изображение -> монохромное изображение
    @staticmethod
    def color_to_monochrome(image: ColorImage) -> MonochromeImage:
        ImageConverter._require(image, ColorImage)

        result = [
            [sum(pixel) / 3 for pixel in row]
            for row in image.pixels
        ]

        if any(not 0 <= value <= 255 for row in result for value in row):
            raise ConversionError(
                "Яркость после усреднения вышла за границы 0...255"
            )
        return MonochromeImage(result)

    # Цветное изображение -> цветное изображение
    # (статистическая цветокоррекция через _correct с изображением того же типа)
    @classmethod
    def color_to_color(
        cls, image: ColorImage, reference: ColorImage
    ) -> ColorImage:
        cls._require(image, ColorImage)
        cls._require(reference, ColorImage, "reference")
        cls._require_same_size(image, reference)

        pixels = [pixel for row in image.pixels for pixel in row]
        sample = [pixel for row in reference.pixels for pixel in row]

        channels = [
            iter(cls._correct(
                [pixel[channel] for pixel in pixels],
                [pixel[channel] for pixel in sample],
            ))
            for channel in range(3)
        ]

        result = [
            [tuple(next(channel) for channel in channels)
             for _ in range(image.width)]
            for _ in range(image.height)
        ]

        if any(
            not 0 <= value <= 255
            for row in result
            for pixel in row
            for value in pixel
        ):
            raise ConversionError(
                "Цветовые каналы вышли за границы диапазона 0..255"
            )
        return ColorImage(result)