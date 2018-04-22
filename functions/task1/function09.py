import math

from functions.base_function import BaseFunction
from functions.point import Point


class Function09(BaseFunction):
    ARGUMENTS = [
        ('a', float),
        ('b', float),
    ]
    FORMULA = r'$\frac{\arcsin(a \cdot x)}{\sqrt{b^2 - x^2}}$'

    @classmethod
    def calc_point(cls, x, *args):
        a, b = args
        try:
            val = math.asin(a * x) / math.sqrt(b**2 - x**2)
            return Point(x, val)
        except:
            return Point(x, 1e8)
