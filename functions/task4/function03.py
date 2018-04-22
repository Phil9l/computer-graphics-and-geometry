from geometry import Vector, Segment, sort_cw, in_polygon

from functions.base_function import BaseFunction
from functions.point import Point
from functions.utils import string_to_points


class Function03(BaseFunction):
    ARGUMENTS = [
        ('a', string_to_points),
        ('b', string_to_points),
        ('с', int),
    ]

    @classmethod
    def plot_component(cls, polygons, used, start_ind):
        yield polygons[0][start_ind].x, polygons[0][start_ind].y, False
        prev_point = polygons[0][start_ind]
        cur_polygon = 0
        next_point_ind = (start_ind + 1) % len(polygons[0])
        finished = False
        used[start_ind] = True

        while True:
            next_point = polygons[cur_polygon][next_point_ind]
            intersection = None
            seg = Segment(prev_point, next_point)
            for other_point_ind in range(len(polygons[1 - cur_polygon])):
                other_next_point_ind = (other_point_ind + 1) % len(polygons[1 - cur_polygon])
                other_seg = Segment(polygons[1 - cur_polygon][other_point_ind],
                                    polygons[1 - cur_polygon][other_next_point_ind])
                if seg.does_intersect(other_seg) and not other_seg.contains(prev_point):
                    intersection_point = seg.get_intersection_point(other_seg)
                    if intersection is None or (prev_point - intersection[0]).len2() > (prev_point - intersection_point).len2():
                        intersection = (intersection_point, other_next_point_ind)

            if intersection is not None:
                prev_point = intersection[0]
                yield Point(*prev_point.as_tuple())
                next_point_ind = intersection[1]
                cur_polygon = 1 - cur_polygon
            else:
                if cur_polygon == 0:
                    used[next_point_ind] = True
                prev_point = polygons[cur_polygon][next_point_ind]
                yield Point(*prev_point.as_tuple())
                next_point_ind = (next_point_ind + 1) % len(polygons[cur_polygon])
            if next_point_ind == start_ind and cur_polygon == 0 and not finished:
                finished = True
                continue
            if finished:
                return

    @classmethod
    def plot_all(cls, step_size, steps_count, left_x, alpha, beta, *args):
        # ﻿(2, 2), (7, 1), (11, 6), (8, 8), (3, 6)
        #  (9, 1), (14, 5), (7, 5)
        #  (4, 1), (5, 1), (5, 8), (4, 8)
        #  (4, 1), (5, 1), (5, 3), (4, 3)
        try:
            a, b, c = cls.prepare_params(*args)
        except ValueError:
            return
        a, b = sort_cw(a), list(sort_cw(b, reverse=True))
        if c == 1:
            for p in a:
                yield Point(p.x, p.y, True, 0xe74c3c)
            if a:
                yield Point(a[0].x, a[0].y, True, 0xe74c3c)
            t = False
            for p in b:
                yield Point(p.x, p.y, t, 0x3c4ce7)
                t = True
            if b:
                yield Point(b[0].x, b[0].y, True, 0x3c4ce7)
            return

        used = [False] * len(a)
        polygons = [a, b]
        if len(a) < 3:
            for i in a:
                yield i.as_tuple()
            return
        for i in range(len(a)):
            if not used[i] and not in_polygon(polygons[0][i], polygons[1]):
                yield from cls.plot_component(polygons, used, i)

    @classmethod
    def calc_point(cls, x, *args):
        raise NotImplementedError
