import abc
import contextlib

from .point import Point


class BaseFunction(metaclass=abc.ABCMeta):
    ARGUMENTS = [
        ('a', int),
        ('b', int),
        ('c', int),
    ]
    FORMULA = ''
    HIGHLIGHT_SQUARES = False

    @classmethod
    def plot_all(cls, step_size, steps_count, left_x, alpha, beta, *args):
        with contextlib.suppress(ValueError):
            new_args = cls.prepare_params(*args)
            for i in range(steps_count):
                carg = i * step_size + left_x
                if carg < alpha or carg > beta:
                    continue
                yield cls.calc_point(carg, *new_args)

    @classmethod
    def prepare_params(cls, *args):
        new_args = []
        for i in range(len(cls.ARGUMENTS)):
            new_args.append(cls.ARGUMENTS[i][1](args[i]))
        return new_args

    @abc.abstractclassmethod
    def calc_point(cls, carg, *args):
        return Point(0, 0)
