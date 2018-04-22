import re
import traceback

from geometry import Vector


def string_to_points(s):
    try:
        res = []
        for x, y in re.findall(r'\((.*?),\s*(.*?)\)', s):
            res.append(Vector(float(x), float(y)))
        return res
    except (TypeError, ValueError):
        return []
    except Exception:
        traceback.print_exc()