from config import FUNCTION_COLOR


class Point:
    def __init__(self, x, y, need_line=True, color=None):
        self.x = x
        self.y = y
        self.need_line = need_line
        self.color = color if color is not None else FUNCTION_COLOR

    def __repr__(self):
        return '<Point: x={}, y={}, need_line={}, color={}>'.format(
            self.x, self.y, self.need_line, self.color)

    def __str__(self):
        return '({}, {}; need_line={}, color={})'.format(
            self.x, self.y, self.need_line, self.color)
