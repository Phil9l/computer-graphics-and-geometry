class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '<Vector: x={}, y={}>'.format(self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Vector) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def as_tuple(self):
        return self.x, self.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, float):
            return Vector(other * self.x, other * self.y)
        elif isinstance(other, Vector):
            return self.x * other.x + self.y * other.y

    def __xor__(self, other):
        return self.x * other.y - self.y * other.x

    def len2(self):
        return self.x**2 + self.y**2


def sort_cw(data, reverse=False):
    if not data:
        return data
    leftmost = (data[0], 0)
    for i, point in enumerate(data):
        if point.x < leftmost[0].x or (point.x == leftmost[0].x and point.y < leftmost[0].y):
            leftmost = (point, i)
    leftmost = leftmost[1]
    p1 = data[(len(data) + leftmost - 1) % len(data)]
    p2 = data[leftmost]
    p3 = data[(leftmost + 1) % len(data)]

    need_rev = ((p2 - p1) ^ (p3 - p2)) < 0

    if reverse ^ need_rev:
        return reversed(data)
    return data


def get_square(polygon, start_point=None):
    if not polygon:
        return 0
    if start_point is None:
        start_point = polygon[0]
    res = 0
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        res += abs((p1 - start_point) ^ (p2 - start_point))
    return res / 2.0


def in_polygon(point, polygon):
    if len(polygon) < 3:
        return False
    return abs(get_square(polygon) - get_square(polygon, point)) < 10**(-5)
