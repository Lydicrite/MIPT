import copy
from pathlib import Path
import sys

try:
    from ..decoders.decoder import (
        BinHistDecoder,
        CsvHistDecoder,
        ImageHistDecoder,
        JsonHistDecoder,
        TxtHistDecoder,
    )
    from ..encoders.encoder import (
        BinHistEncoder,
        CsvHistEncoder,
        JsonHistEncoder,
        TxtHistEncoder,
    )
except ImportError:
    task_directory = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(task_directory))
    from decoders.decoder import (
        BinHistDecoder,
        CsvHistDecoder,
        ImageHistDecoder,
        JsonHistDecoder,
        TxtHistDecoder,
    )
    from encoders.encoder import (
        BinHistEncoder,
        CsvHistEncoder,
        JsonHistEncoder,
        TxtHistEncoder,
    )


class Hist:
    _decoders = {
        ".bin": BinHistDecoder,
        ".csv": CsvHistDecoder,
        ".txt": TxtHistDecoder,
        ".json": JsonHistDecoder,
        ".png": ImageHistDecoder,
        ".jpg": ImageHistDecoder,
        ".jpeg": ImageHistDecoder,
        ".bmp": ImageHistDecoder,
    }
    _encoders = {
        ".bin": BinHistEncoder,
        ".csv": CsvHistEncoder,
        ".txt": TxtHistEncoder,
        ".json": JsonHistEncoder,
    }

    def __init__(self, data):
        self._data = {
            int(key): float(value) for key, value in data.items()
        }

    @classmethod
    def read(cls, file_path):
        extension = Path(file_path).suffix.lower()
        decoder = cls._decoders.get(extension)
        if decoder is None:
            raise ValueError(
                f"Невозможно прочитать гистограмму формата '{extension}'"
            )
        return cls(decoder.decode(file_path))

    def write(self, file_path):
        extension = Path(file_path).suffix.lower()
        encoder = self._encoders.get(extension)
        if encoder is None:
            raise ValueError(
                f"Невозможно записать гистограмму формата '{extension}'"
            )
        encoder.encode(file_path, self._data)

    def get_data(self):
        return copy.deepcopy(self._data)


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent.parent / "data" / "csv_test.csv"
    histogram = Hist.read(data_path)
    print(histogram.get_data())
