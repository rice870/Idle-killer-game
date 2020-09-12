import math


def find_rel_angle(cx, cy, ox, oy):
    rx = ox - cx
    ry = oy - cy
    return (180 / math.pi) * -math.atan2(rx, ry)


print(find_rel_angle(50, 50, 100, 100))
