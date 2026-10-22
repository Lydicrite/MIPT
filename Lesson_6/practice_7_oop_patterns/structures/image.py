import cv2

"""
Абстрактная фабрика 
"""

class AbstractFactoryImageReader():
    def read_image(self, file_path):
        raise NotImplementedError()

class BinImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        raise NotImplementedError()

class MonochromeImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        return image

class ColorImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        raise NotImplementedError()

def get_image_reader(ident):
    if ident == 0:
        return BinImageReader()
    elif ident == 1:
        return MonochromeImageReader()
    elif ident == 2:
        return ColorImageReader()

if __name__ == "__main__":
    try:
        for i in range(3):
            print(get_image_reader(i))
    except Exception as e:
        print(e)