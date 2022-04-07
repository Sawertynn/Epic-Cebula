
rel_width = 1920
rel_height = 1080

store = 150, 190
back = 380, 90
cart = 1600, 90

scrollbar_x = 1915


def cast(point: (int, int), size: (int, int)):
    x = point[0] * size[0] / rel_width
    y = point[1] * size[1] / rel_height
    return int(x), int(y)