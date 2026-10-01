from math import isfinite, sqrt

from histogram import count_levels, normalize_histogram


def image_histogram(image):
    return count_levels(image.convert("L").tobytes())


def equalize_histogram(image):
    image = image.convert("L")
    counts = image_histogram(image)
    total = sum(counts.values())
    if total == 0:
        raise ValueError("Изображение не может быть пустым")
    first_count = next(count for count in counts.values() if count)
    if first_count == total:
        return image.copy()

    cumulative = 0
    table = []
    for count in counts.values():
        cumulative += count
        value = round(255 * (cumulative - first_count) / (total - first_count))
        table.append(max(0, min(255, value)))
    return image.point(table)


def gamma_correction(image, gamma):
    if not isfinite(gamma) or gamma <= 0:
        raise ValueError("Gamma должна быть конечным и положительным")
    table = [round(255 * (level / 255) ** gamma) for level in range(256)]
    return image.convert("L").point(table)


def statistical_correction(image, reference_histogram):
    target = normalize_histogram(reference_histogram)
    source = normalize_histogram(image_histogram(image))

    def statistics(hist):
        mean = sum(level * probability for level, probability in hist.items())
        variance = sum(
            (level - mean) ** 2 * probability
            for level, probability in hist.items()
        )
        return mean, sqrt(variance)

    source_mean, source_std = statistics(source)
    target_mean, target_std = statistics(target)
    if source_std == 0:
        raise ValueError("Статистическая нормализация требует нестандартного изображения, которое не может быть постоянным")
    table = [
        max(0, min(255, round(target_std * (level - source_mean) / source_std
                              + target_mean)))
        for level in range(256)
    ]
    return image.convert("L").point(table)
