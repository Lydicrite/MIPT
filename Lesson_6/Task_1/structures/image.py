import cv2


class AbstractFactoryImageReader:
    def read_image(self, file_path):
        raise NotImplementedError()

    @staticmethod
    def _read(file_path, mode):
        image = cv2.imread(str(file_path), mode)
        if image is None:
            raise FileNotFoundError(
                f"Не удалось загрузить изображение: {file_path}"
            )
        return image


class BinImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = self._read(file_path, cv2.IMREAD_GRAYSCALE)
        _, binary = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return binary


class MonochromeImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        return self._read(file_path, cv2.IMREAD_GRAYSCALE)


class ColorImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        return self._read(file_path, cv2.IMREAD_COLOR)


def get_image_reader(ident):
    readers = {
        0: BinImageReader,
        1: MonochromeImageReader,
        2: ColorImageReader,
    }
    reader = readers.get(ident)
    if reader is None:
        raise ValueError(f"Неизвестный тип изображения: {ident}")
    return reader()
