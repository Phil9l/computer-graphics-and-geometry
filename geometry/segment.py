class Segment:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def dir_vector(self):
        return self.b - self.a

    def __repr__(self):
        return '<Segment: A={}, B={}>'.format(str(self.a), str(self.b))

    def __str__(self):
        return '({}, {})'.format(str(self.a), str(self.b))

    def __eq__(self, other):
        return isinstance(other, Segment) and self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b))

    def does_intersect(self, other):
        intersect = True
        intersect &= ((self.b - self.a) ^ (other.a - self.a)) * ((self.b - self.a) ^ (other.b - self.a)) < 0
        intersect &= ((other.b - other.a) ^ (self.a - other.a)) * ((other.b - other.a) ^ (self.b - other.a)) < 0
        return intersect

    def get_intersection_point(self, other):
        if self.dir_vector ^ other.dir_vector == 0:
            return None

        y = ((self.a - other.a) ^ self.dir_vector) / (other.dir_vector ^ self.dir_vector)
        return other.a + other.dir_vector * y

    def contains(self, point):
        return abs((point - self.a) ^ (point - self.b)) < 10**(-5)
