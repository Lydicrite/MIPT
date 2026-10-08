import argparse
import sys
from pathlib import Path

from converter import ConversionError, ImageConverter
from images import BinaryImage, ColorImage, MonochromeImage
from io_utils import ImageIOError, load_image, save_image


PALETTE = [(v, 255 - v, min(255, v * 2)) for v in range(256)]


def build_conversion(source, target, reference):
    if isinstance(source, BinaryImage):
        if target == "binary":
            return ImageConverter.binary_to_binary(source)
        if target == "monochrome":
            return ImageConverter.binary_to_monochrome(source)
        return ImageConverter.binary_to_color(source, PALETTE)

    if isinstance(source, MonochromeImage):
        if target == "binary":
            return ImageConverter.monochrome_to_binary(source)
        if target == "monochrome":
            if reference is None:
                raise ConversionError("Нужен --reference для monochrome -> monochrome")
            if not isinstance(reference, MonochromeImage):
                raise ConversionError("reference должен быть MonochromeImage")
            return ImageConverter.monochrome_to_monochrome(source, reference)
        return ImageConverter.monochrome_to_color(source, PALETTE)

    if isinstance(source, ColorImage):
        if target == "binary":
            return ImageConverter.color_to_binary(source)
        if target == "monochrome":
            return ImageConverter.color_to_monochrome(source)
        if reference is None:
            raise ConversionError("Нужен --reference для color -> color")
        if not isinstance(reference, ColorImage):
            raise ConversionError("reference должен быть ColorImage")
        return ImageConverter.color_to_color(source, reference)

    raise ConversionError(f"Неподдерживаемый тип: {type(source).__name__}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Работа с PBM/PGM/PPM")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--to", required=True,
                        choices=["binary", "monochrome", "color"])
    parser.add_argument("--reference", type=Path)
    args = parser.parse_args(argv)

    try:
        source = load_image(args.input)
        reference = load_image(args.reference) if args.reference else None
        result = build_conversion(source, args.to, reference)
        save_image(result, args.output)
    except ImageIOError as error:
        print(f"[файл] {error}", file=sys.stderr)
        return 1
    except (ConversionError, TypeError, ValueError) as error:
        print(f"[преобразование] {error}", file=sys.stderr)
        return 2
    except Exception as error:
        print(f"[непредвиденное] {error}", file=sys.stderr)
        return 3

    print(f"OK: {args.input} -> {args.output} ({args.to})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# python Lesson_5/HomeTask_1/main.py F:\Lydicrite\MIPT\Python\Lesson_4\HomeTask_2\source_images\binary.pbm F:\Lydicrite\MIPT\Python\Lesson_5\out\1.pbm --to color
# ошибка

# python Lesson_5/HomeTask_1/main.py F:\Lydicrite\MIPT\Python\Lesson_4\HomeTask_2\source_images\binary.pbm F:\Lydicrite\MIPT\Python\Lesson_5\out\1.ppm --to color
# норм