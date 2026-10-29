"""
Шаблонный метод (Template method)
"""
from pathlib import Path
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



# Task_1_i
class MonochromeImage(BinaryImage):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        gaussian = cv2.GaussianBlur(image, (5, 5), 0)
        return gaussian

    def segmentation(self, image):
        edges = cv2.Canny(image, 100, 200)
        output = cv2.connectedComponentsWithStats(
            edges,
            4,  # connectivity
            cv2.CV_32S)
        return (edges, output)

'''
Для data/1.jpg был вывод:

Monochrome Image Processing
[np.int32(112), np.int32(11), np.int32(45), np.int32(37), np.int32(156)]
[np.int32(15), np.int32(20), np.int32(48), np.int32(49), np.int32(175)]
[np.int32(96), np.int32(63), np.int32(88), np.int32(16), np.int32(198)]
[np.int32(105), np.int32(91), np.int32(59), np.int32(59), np.int32(213)]
[np.int32(27), np.int32(94), np.int32(46), np.int32(47), np.int32(178)]
[np.int32(174), np.int32(111), np.int32(33), np.int32(33), np.int32(124)]
'''





class ColorImage(MonochromeImage):
    def __init__(self):
        pass

    def segmentation(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        distance = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
        _, foreground = cv2.threshold(
            distance, 0.2 * distance.max(), 255, cv2.THRESH_BINARY
        )
        foreground = foreground.astype("uint8")

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        background = cv2.dilate(binary, kernel, iterations=3)
        unknown = cv2.subtract(background, foreground)

        _, markers = cv2.connectedComponents(foreground)
        markers += 1
        markers[unknown == 255] = 0
        cv2.watershed(image.copy(), markers)

        object_mask = ((markers > 1) * 255).astype("uint8")
        components = cv2.connectedComponentsWithStats(
            object_mask,
            4,  # connectivity
            cv2.CV_32S,
        )
        return (object_mask, components)

"""
Декоратор - структурный паттерн
"""
# 1.a.ii
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

# 1.b.i
class HuMomentsAnalysis(ObjectAnalysis):
    def __init__(self, obj):
        self._proc = obj

    def template_method(self, image):
        filtered_image = self._proc.noise_filtering(image)
        segmented_image, components = self._proc.segmentation(filtered_image)
        parameters = self._proc.object_parameters(
            (segmented_image, components)
        )

        num_labels, labels, _, _ = components
        hu_moments = []
        for label in range(1, num_labels):
            component_mask = (labels == label).astype("uint8")
            moments = cv2.moments(component_mask, binaryImage=True)
            hu = cv2.HuMoments(moments).flatten().tolist()
            hu_moments.append(hu)

        return (*parameters, hu_moments)





if __name__== '__main__':
    image_path = Path(__file__).resolve().parent.parent / 'data' / '1.jpg'
    monochrome_image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    color_image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if monochrome_image is None or color_image is None:
        raise FileNotFoundError(f"Не удалось загрузить изображение: {image_path}")

    print("Monochrome Image Processing")
    monochrome_segm = MonochromeImage()
    (x, y, w, h, area) = monochrome_segm.template_method(monochrome_image)
    for i in range(len(area)):
            print([x[i], y[i], w[i], h[i], area[i]])

    print("Color Image Processing")
    color_segm = ColorImage()
    (x, y, w, h, area) = color_segm.template_method(color_image)
    for i in range(len(area)):
            print([x[i], y[i], w[i], h[i], area[i]])

    print("Color Image Hu Moments")
    hu_analysis = HuMomentsAnalysis(ColorImage())
    (x, y, w, h, area, hu_moments) = hu_analysis.template_method(color_image)
    for i in range(len(area)):
            print([x[i], y[i], w[i], h[i], area[i], hu_moments[i]])
