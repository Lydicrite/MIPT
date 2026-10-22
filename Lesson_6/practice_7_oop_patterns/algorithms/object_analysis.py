"""
Шаблонный метод (Template method)
"""
import cv2

class ObjectAnalysis(object):
    def template_method(self, image):

        image = self.noise_filtering(image)
        data = self.segmentation(image)
        data = self.object_parameters(data)

        return data

    def noise_filtering(self, image):
        raise NotImplementedError()

    def segmentation(self, data):
        raise NotImplementedError()

    def object_parameters(self, data):
        (image, data) = data
        (numLabels, labels, stats, centroids) = data
        x = []
        y = []
        w = []
        h = []
        area = []
        for i in range(1, numLabels):
            # extract the connected component statistics for the current
            # label
            x.append(stats[i, cv2.CC_STAT_LEFT])
            y.append(stats[i, cv2.CC_STAT_TOP])
            w.append(stats[i, cv2.CC_STAT_WIDTH])
            h.append(stats[i, cv2.CC_STAT_HEIGHT])
            area.append(stats[i, cv2.CC_STAT_AREA])

        return (x, y, w, h, area)


class BinaryImage(ObjectAnalysis):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        median = cv2.medianBlur(image, 5)
        return median

    def segmentation(self, image):
        output = cv2.connectedComponentsWithStats(
            image,
            4, # connectivity
            cv2.CV_32S)
        return (image, output)



class MonochromeImage(BinaryImage):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        return None

    def segmentation(self, image):
        return None

class ColorImage(MonochromeImage):
    def __init__(self):
        pass

    def segmentation(self, image):
        return None



"""
Декоратор - структурный паттерн
"""

class FilteredAnalysis(ObjectAnalysis):
    def __init__(self, obj):
        self._proc = obj

    def template_method(self, image):
        (_x, _y, _w, _h, _area) = self._proc.template_method(image)
        x = []
        y = []
        w = []
        h = []
        area = []

        for i in range(len(_area)):
            if _area[i] > 10 and _area[i] < 2500:
                x.append(_x[i])
                y.append(_y[i])
                w.append(_w[i])
                h.append(_h[i])
                area.append(_area[i])

        return (x,y,w,h,area)


if __name__== '__main__':
    print("Binary Image Processing")
    bin_segm = BinaryImage()
    (x,y,w,h,area) = bin_segm.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])

    print("Decorated Binary Image Processing")
    filt_bin = FilteredAnalysis(BinaryImage())
    (x, y, w, h, area) = filt_bin.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])
