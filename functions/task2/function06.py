import math

from functions.base_function import BaseFunction
from functions.point import Point


class Function06(BaseFunction):
    ARGUMENTS = [
        ('a', float),
    ]
    FORMULA = r'$a \cdot \sin(3 \cdot \varphi)$'

    @classmethod
    def calc_point(cls, phi, *args):
        a = args[0]
        r = a * math.sin(3 * phi)
        return Point(r * math.cos(phi), r * math.sin(phi))
