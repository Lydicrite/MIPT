from pathlib import Path
from random import Random

from converter import ImageConverter
from images import BinaryImage, ColorImage, Image, MonochromeImage


class ImageDemo:
    def __init__(self, width: int = 16, height: int = 16, seed: int = 42):
        self.width = width
        self.height = height
        self.random = Random(seed)
        self.root = Path(__file__).parent
        self.palette = [
            (value, 255 - value, min(255, value * 2))
            for value in range(256)
        ]

    def _random_binary(self) -> BinaryImage:
        pixels = [
            [self.random.randint(0, 1) for _ in range(self.width)]
            for _ in range(self.height)
        ]
        pixels[0][0] = 1
        return BinaryImage(pixels)

    def _random_monochrome(self) -> MonochromeImage:
        return MonochromeImage([
            [self.random.randint(0, 255) for _ in range(self.width)]
            for _ in range(self.height)
        ])

    def _random_color(self) -> ColorImage:
        return ColorImage([
            [
                tuple(self.random.randint(0, 255) for _ in range(3))
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ])

    @staticmethod
    def _extension(image: Image) -> str:
        if isinstance(image, BinaryImage):
            return ".pbm"
        if isinstance(image, MonochromeImage):
            return ".pgm"
        return ".ppm"

    @staticmethod
    def _save(image: Image, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(image, BinaryImage):
            header = "P1\n{} {}\n".format(image.width, image.height)
            rows = [" ".join("0" if pixel else "1" for pixel in row)
                    for row in image.pixels]
        elif isinstance(image, MonochromeImage):
            header = "P2\n{} {}\n255\n".format(image.width, image.height)
            rows = [" ".join(map(str, row)) for row in image.pixels]
        else:
            header = "P3\n{} {}\n255\n".format(image.width, image.height)
            rows = [
                " ".join(str(channel) for pixel in row for channel in pixel)
                for row in image.pixels
            ]
        path.write_text(header + "\n".join(rows) + "\n", encoding="ascii")

    def run(self) -> None:
        binary = self._random_binary()
        monochrome = self._random_monochrome()
        monochrome_reference = self._random_monochrome()
        color = self._random_color()
        color_reference = self._random_color()

        source_images = {
            "binary": binary,
            "monochrome": monochrome,
            "monochrome_reference": monochrome_reference,
            "color": color,
            "color_reference": color_reference,
        }
        for name, image in source_images.items():
            self._save(
                image,
                self.root / "source_images" / (name + self._extension(image)),
            )

        converted_images = {
            "monochrome_to_monochrome":
                ImageConverter.monochrome_to_monochrome(
                    monochrome, monochrome_reference
                ),
            "color_to_color":
                ImageConverter.color_to_color(color, color_reference),
            "binary_to_binary":
                ImageConverter.binary_to_binary(binary),
            "color_to_monochrome":
                ImageConverter.color_to_monochrome(color),
            "monochrome_to_color":
                ImageConverter.monochrome_to_color(monochrome, self.palette),
            "monochrome_to_binary":
                ImageConverter.monochrome_to_binary(monochrome),
            "binary_to_monochrome":
                ImageConverter.binary_to_monochrome(binary),
            "color_to_binary":
                ImageConverter.color_to_binary(color),
            "binary_to_color":
                ImageConverter.binary_to_color(binary, self.palette),
        }

        for conversion, image in converted_images.items():
            path = (
                self.root / "converted_images" / conversion
                / ("result" + self._extension(image))
            )
            self._save(image, path)
            valid = image.width == self.width and image.height == self.height
            status = "корректно" if valid else "ошибка"
            print("{}: {} -> {}".format(conversion, status, path))


if __name__ == "__main__":
    ImageDemo().run()
