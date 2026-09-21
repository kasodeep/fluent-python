import math

class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        """
        The __repr__ special method is called by the repr built-in to get the string
        representation of the object for inspection.
        While __str__ is meant to be readable, __repr__ is meant to be unambiguous.
        """
        # what does !r do? It calls repr() on the value, which is useful for debugging.
        return f'Vector({self.x!r}, {self.y!r})'

    def __abs__(self):
        return math.hypot(self.x, self.y)

    # if bool, not implemented, Python will call __len__ and return False if the length is zero, True otherwise.
    def __bool__(self):
        return bool(self.x or self.y)

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self * scalar

