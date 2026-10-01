import csv
import json
from pathlib import Path
import struct

from PIL import Image

from audio_processing import AudioData, read_wav, write_wav
from histogram import validate_histogram


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}
HISTOGRAM_EXTENSIONS = {".txt", ".csv", ".json", ".bin"}


def histogram_from_pairs(pairs):
    data = {}
    for pair in pairs:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError("Ожидаемые части гистограмм: уровень, значение")
        key, value = pair
        level = int(key)
        if isinstance(key, float) and key != level:
            raise ValueError("Уровень гистограммы должен быть целым числом")
        if level in data:
            raise ValueError(f"Дубликат уровня гистограммы: {level}")
        data[level] = float(value)
    return validate_histogram(data)


def read_txt(path):
    with open(path, encoding="utf-8-sig") as file:
        tokens = file.read().split()
    if len(tokens) % 2:
        raise ValueError("TXT должен содержать пары уровня/значение")
    return histogram_from_pairs(list(zip(tokens[::2], tokens[1::2])))


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as file:
        return histogram_from_pairs(list(csv.reader(file)))


def read_json(path):
    with open(path, encoding="utf-8-sig") as file:
        data = json.load(file)
    if (not isinstance(data, dict)
            or not isinstance(data.get("keys"), list)
            or not isinstance(data.get("values"), list)
            or len(data["keys"]) != len(data["values"])):
        raise ValueError("JSON должен содержать равные списки уровней и значений")
    return histogram_from_pairs(list(zip(data["keys"], data["values"])))


def read_bin(path):
    raw = Path(path).read_bytes()
    if len(raw) != 256 * 4:
        raise ValueError("BIN должен содержать ровно 256 little-endian float32 значений")
    return validate_histogram(dict(enumerate(struct.unpack("<256f", raw))))


def read_image(path):
    with Image.open(path) as image:
        return image.convert("L")


READERS = {
    ".txt": read_txt,
    ".csv": read_csv,
    ".json": read_json,
    ".bin": read_bin,
    ".wav": read_wav,
    **{extension: read_image for extension in IMAGE_EXTENSIONS},
}


def read_data(path):
    path = Path(path)
    reader = READERS.get(path.suffix.lower())
    if reader is None:
        raise ValueError(f"Неподдерживаемое входное расширение: {path.suffix}")
    return reader(path)


def write_histogram(path, data):
    data = validate_histogram(data)
    extension = Path(path).suffix.lower()
    if extension not in HISTOGRAM_EXTENSIONS:
        raise ValueError("Гистограмма должна быть в формате TXT, CSV, JSON или BIN")
    if extension == ".bin":
        Path(path).write_bytes(struct.pack("<256f", *data.values()))
        return
    with open(path, "w", encoding="utf-8", newline="") as file:
        if extension == ".txt":
            for level, value in data.items():
                file.write(f"{level} {value}\n")
        elif extension == ".csv":
            csv.writer(file).writerows(data.items())
        else:
            json.dump(
                {"keys": list(data), "values": list(data.values())},
                file, indent=2, allow_nan=False,
            )


def write_data(path, data):
    path = Path(path)
    extension = path.suffix.lower()
    if isinstance(data, Image.Image):
        if extension not in IMAGE_EXTENSIONS:
            raise ValueError("Изображение должно быть сохранено в формате PNG, JPG, JPEG, BMP, TIF или TIFF")
        writer = lambda: data.save(path)
    elif isinstance(data, AudioData):
        if extension != ".wav":
            raise ValueError("Аудио-файл должно быть сохранено в формате WAV")
        writer = lambda: write_wav(path, data)
    elif isinstance(data, dict):
        if extension not in HISTOGRAM_EXTENSIONS:
            raise ValueError("Гистограмма должна быть в формате TXT, CSV, JSON или BIN")
        writer = lambda: write_histogram(path, data)
    else:
        raise ValueError("Неподдерживаемый тип выходных данных")
    path.parent.mkdir(parents=True, exist_ok=True)
    writer()
