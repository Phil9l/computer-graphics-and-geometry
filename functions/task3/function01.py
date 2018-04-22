import math

from functions.base_function import BaseFunction
from functions.point import Point


class Function01(BaseFunction):
    ARGUMENTS = [
        ('a', float),
        ('b', float),
        ('c', float),
    ]
    FORMULA = r'$a \cdot x^2 + b \cdot x + c$'
    HIGHLIGHT_SQUARES = True

    @classmethod
    def calc_point(cls, x, *args):
        a, b, c = args
        return Point(x, a * x**2 + b * x + c)
