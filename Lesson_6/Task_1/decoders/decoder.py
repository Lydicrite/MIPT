import csv
import json
import struct

import cv2

# 2.a

class HistDecoder:
    @staticmethod
    def decode(file_path):
        raise NotImplementedError()


class BinHistDecoder(HistDecoder):
    @staticmethod
    def decode(file_path):
        with open(file_path, "rb") as file:
            raw_data = file.read()

        if len(raw_data) % 4 != 0:
            raise ValueError("Размер бинарной гистограммы не кратен 4 байтам")

        values = struct.unpack(f"<{len(raw_data) // 4}f", raw_data)
        return {index: value for index, value in enumerate(values)}


class CsvHistDecoder(HistDecoder):
    @staticmethod
    def decode(file_path):
        with open(file_path, newline="", encoding="utf-8") as csv_file:
            data = dict(csv.reader(csv_file))
        return {int(key): float(value) for key, value in data.items()}


class TxtHistDecoder(HistDecoder):
    @staticmethod
    def decode(file_path):
        with open(file_path, encoding="utf-8") as file:
            source = file.read().split()

        if len(source) % 2 != 0:
            raise ValueError("TXT-гистограмма должна содержать пары ключ-значение")

        return {
            int(source[index]): float(source[index + 1])
            for index in range(0, len(source), 2)
        }


class JsonHistDecoder(HistDecoder):
    @staticmethod
    def decode(file_path):
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        return {
            int(key): float(value)
            for key, value in zip(data["keys"], data["values"])
        }


class ImageHistDecoder(HistDecoder):
    @staticmethod
    def decode(file_path):
        image = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError(
                f"Не удалось загрузить изображение: {file_path}"
            )

        pixel_count = image.shape[0] * image.shape[1]
        return {
            value: float((image == value).sum()) / pixel_count
            for value in range(256)
        }
