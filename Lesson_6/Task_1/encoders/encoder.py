import csv
import json
import struct

# 2.a

class HistEncoder:
    @staticmethod
    def encode(file_path, data):
        raise NotImplementedError()

    @staticmethod
    def ordered_items(data):
        return sorted(data.items(), key=lambda item: int(item[0]))


class BinHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        values = [
            float(value)
            for _, value in HistEncoder.ordered_items(data)
        ]
        with open(file_path, "wb") as file:
            file.write(struct.pack(f"<{len(values)}f", *values))


class CsvHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(HistEncoder.ordered_items(data))


class TxtHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        with open(file_path, "w", encoding="utf-8") as file:
            for key, value in HistEncoder.ordered_items(data):
                file.write(f"{key} {value}\n")


class JsonHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        items = HistEncoder.ordered_items(data)
        content = {
            "keys": [int(key) for key, _ in items],
            "values": [float(value) for _, value in items],
        }
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(content, file, indent=2)
