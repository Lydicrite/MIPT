'''
Точные матрицы:

    RGB_TO_YIQ = [
        [0.299,  0.587,  0.114],
        [0.596, -0.274, -0.322],
        [0.211, -0.523,  0.312],
    ]

    # YIQ -> RGB
    YIQ_TO_RGB = [
        [1.0,  0.956,  0.621],
        [1.0, -0.272, -0.647],
        [1.0, -1.106,  1.703],
    ]
'''

def convert(color):
    # RGB -> YIQ
    RGB_TO_YIQ = [
        [0.299,   0.587,   0.114],
        [0.5959, -0.2746, -0.3213],
        [0.2115, -0.5227,  0.3112],
    ]

    # YIQ -> RGB
    YIQ_TO_RGB = [
        [1.0,  0.956,  0.619],
        [1.0, -0.272, -0.647],
        [1.0, -1.106,  1.703],
    ]

    # Допустимые диапазоны компонент
    RGB_RANGE = (0.0, 255.0)
    Y_RANGE   = (0.0, 255.0)
    I_RANGE   = (-152.0, 152.0)
    Q_RANGE   = (-133.0, 133.0)

    # Ограничение значений компонент
    def color_clamp(value, low, high):
        if value < low:
            return low
        if value > high:
            return high
        return value

    # Произведение 3x3 матрицы на вектор
    def mat_vec_mul_3x3(matrix, vector):
        return [
            matrix[i][0] * vector[0]
            + matrix[i][1] * vector[1]
            + matrix[i][2] * vector[2]
            for i in range(3)
        ]



    if len(color) != 4:
        raise ValueError("Вектор должен содержать ровно 4 компоненты")

    c1, c2, c3, t = color

    if t == 0:
        # RGB -> YIQ
        rgb = [
            color_clamp(c1, *RGB_RANGE),
            color_clamp(c2, *RGB_RANGE),
            color_clamp(c3, *RGB_RANGE),
        ]

        y, i, q = mat_vec_mul_3x3(RGB_TO_YIQ, rgb)

        y = round(color_clamp(y, *Y_RANGE), 3)
        i = round(color_clamp(i, *I_RANGE), 3)
        q = round(color_clamp(q, *Q_RANGE), 3)

        return [y, i, q, 1]

    elif t == 1:
        # YIQ -> RGB
        yiq = [
            color_clamp(c1, *Y_RANGE),
            color_clamp(c2, *I_RANGE),
            color_clamp(c3, *Q_RANGE),
        ]

        r, g, b = mat_vec_mul_3x3(YIQ_TO_RGB, yiq)

        r = int(round(color_clamp(r, *RGB_RANGE)))
        g = int(round(color_clamp(g, *RGB_RANGE)))
        b = int(round(color_clamp(b, *RGB_RANGE)))

        return [r, g, b, 0]

    else:
        raise ValueError("Тип (4-я компонента) должен быть 0 или 1")




if __name__ == "__main__":
    rgb_colors = [
        [255,   0,      0],
        [0,     255,    0],
        [0,     0,      255],
        [128,   128,    128],
        [200,   100,    50],
        [10,    20,     30],
        [250,   240,    230],
        [137,   88,    94]
    ]

    print(f"{'RGB':<20}{'YIQ':<40}{'RGB':<20}{'совпало':<10}")
    print("-" * 102)

    for rgb in rgb_colors:
        yiq = convert(rgb + [0])
        back = convert(yiq)
        ok = "OK" if back[:3] == rgb else "ERR"
        print(
            f"{str(rgb):<20}"
            f"{str(yiq[:3] + [yiq[3]]):<40}"
            f"{str(back[:3] + [back[3]]):<20}{ok:<10}"
        )