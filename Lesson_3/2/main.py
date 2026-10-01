# python "Lesson_3/2/main.py" --help

# Гистограмма изображения: 256 значений, количество пикселей
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/cells.jpg" -o "Lesson_3/2/output_data/cells.bin" -m histogram

# Нормированная гистограмма: сумма значений равна 1
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/cells.jpg" -o "Lesson_3/2/output_data/cells.csv" -m histogram --normalize

# Эквализация
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/sar_1_gray.jpg" -o "Lesson_3/2/output_data/sar_1_gray_equalize.jpg" -m equalize

#  Гамма-коррекция
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/sar_1_gray.jpg" -o "Lesson_3/2/output_data/sar_1_gray_gamma.jpg" -m gamma --gamma 0.5

# Статистическая коррекция
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/cells.jpg" -o "Lesson_3/2/output_data/cells_statcorr.png" -m stat --reference  "Lesson_3/2/input_data/json_test.json"

# Пересохранение готовой гистограммы в другом формате
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/txt_test.txt" -m histogram -o "Lesson_3/2/output_data/converted.json"

# Часть про звук
# Только гистограмма из 256 бинов
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/input.wav" -m histogram -o "Lesson_3/2/output_data/audio_hist.json"

# Квантованный WAV и автоматически создаваемая audio_8bit.hist.json
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/input.wav" -m quantize -o "Lesson_3/2/output_data/audio_8bit.wav"

# Явный путь и нормировка гистограммы, WAV остаётся тем же
# python "Lesson_3/2/main.py" -p "Lesson_3/2/input_data/input.wav" -m quantize --histogram-output "Lesson_3/2/output_data/audio_hist_norm.csv" --normalize

import argparse
from pathlib import Path

from PIL import Image

from audio_processing import AudioData, audio_histogram, quantize_audio
from file_io import HISTOGRAM_EXTENSIONS, read_data, write_data
from histogram import normalize_histogram
from image_processing import (
    equalize_histogram,
    gamma_correction,
    image_histogram,
    statistical_correction,
)


OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def init_parser():
    parser = argparse.ArgumentParser(
        description="Читает файлы по их расширению; обрабатывает серые изображения или PCM WAV файлы."
    )
    parser.add_argument("-p", "--path", required=True, type=Path, help="Путь к файлу")
    parser.add_argument(
        "-m", "--operation", required=True,
        choices=("histogram", "equalize", "gamma", "quantize", "stat"),
        help="Операция для выполнения",
    )
    parser.add_argument("-o", "--output", type=Path, help="Файл вывода")
    parser.add_argument("--gamma", type=float, help="Позитивная экспонента для gamma")
    parser.add_argument(
        "--reference", type=Path,
        help="Справочная изображение или гистограмма для статистической коррекции",
    )
    parser.add_argument(
        "--histogram-output", type=Path,
        help="Только для quantize: путь к гистограмме (по умолчанию: output_name.hist.json)",
    )
    parser.add_argument(
        "--normalize", action="store_true",
        help="Сохранить вероятности вместо счетчиков",
    )
    return parser


def get_histogram(data):
    if isinstance(data, Image.Image):
        return image_histogram(data)
    if isinstance(data, AudioData):
        return audio_histogram(data)
    return data


def check_output_paths(inputs, outputs):
    resolved_inputs = {path.resolve() for path in inputs}
    resolved_outputs = [path.resolve() for path in outputs]
    if len(set(resolved_outputs)) != len(resolved_outputs):
        raise ValueError("Вывод должен быть разным")
    for output in resolved_outputs:
        if output in resolved_inputs:
            raise ValueError("Вывод не должен перезаписывать входной файл")
        if output.exists() and any(output.samefile(path) for path in inputs):
            raise ValueError("Вывод ссылается на входной файл")


def run(args):
    if args.operation == "gamma" and args.gamma is None:
        raise ValueError("Укажите --gamma для гамма-коррекции")
    if args.operation != "gamma" and args.gamma is not None:
        raise ValueError("--gamma является допустимым только с --operation gamma")
    if (args.reference is not None) != (args.operation == "stat"):
        raise ValueError("--reference требуется только с --operation stat")
    if args.histogram_output and args.operation != "quantize":
        raise ValueError("--histogram-output является допустимым только с --operation quantize")
    if args.normalize and args.operation not in ("histogram", "quantize"):
        raise ValueError("--normalize является допустимым только с --operation histogram или --operation quantize")

    data = read_data(args.path)
    suffix = {"histogram": ".json", "quantize": ".wav"}.get(args.operation, ".png")
    output = args.output or OUTPUT_DIR / f"{args.path.stem}_{args.operation}{suffix}"
    inputs = [args.path] + ([args.reference] if args.reference else [])
    outputs = [output]
    histogram_path = None
    if args.operation == "quantize":
        histogram_path = args.histogram_output or output.with_suffix(".hist.json")
        if histogram_path.suffix.lower() not in HISTOGRAM_EXTENSIONS:
            raise ValueError("Гистограмма должна быть в формате TXT, CSV, JSON формате или BIN")
        outputs.append(histogram_path)
    check_output_paths(inputs, outputs)

    if args.operation == "histogram":
        result = get_histogram(data)
        if args.normalize:
            result = normalize_histogram(result)
    elif args.operation == "quantize":
        if not isinstance(data, AudioData):
            raise ValueError("Квантизация требует вход файл PCM WAV")
        result = quantize_audio(data)
        hist = audio_histogram(data)
        if args.normalize:
            hist = normalize_histogram(hist)
    else:
        if not isinstance(data, Image.Image):
            raise ValueError("Требуется входной файл-изображение")
        if args.operation == "equalize":
            result = equalize_histogram(data)
        elif args.operation == "gamma":
            result = gamma_correction(data, args.gamma)
        else:
            reference = read_data(args.reference)
            result = statistical_correction(data, get_histogram(reference))

    write_data(output, result)
    print(f"Сохранено: {output}")
    if histogram_path is not None:
        write_data(histogram_path, hist)
        print(f"Гистограмма (256 бинов): {histogram_path}")
        print(f"PCM: {data.sample_width * 8} -> 8 bit; "
              f"{data.channels} канал(ов); {data.sample_rate} Hz; "
              f"{len(data.samples) // data.channels} кадров")


def main():
    parser = init_parser()
    args = parser.parse_args()
    try:
        run(args)
    except (OSError, ValueError, TypeError, OverflowError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
