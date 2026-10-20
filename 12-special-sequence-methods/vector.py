"""
Vector (n-dimensional) study notes, Fluent Python style.

Topics covered:
  - sequence protocol / duck typing (__len__ + __getitem__)
  - slicing support, operator.index
  - __getattr__ (dynamic attribute access), __match_args__
  - __setattr__ (why it is needed, and why not __slots__)
  - __hash__ with functools.reduce + operator.xor
  - __format__ with hyperspherical coordinates ('h' suffix)

Needs Python 3.10+ (pattern matching demo). Run: python vector_notes.py
"""

from array import array
import functools          # the pasted code used functools without importing it
import itertools          # same for itertools (used in __format__)
import math
import operator
import reprlib


class Vector:
    typecode = 'd'

    # Names usable as read-only "virtual" attributes: v.x, v.y, v.z, v.t.
    # Also lets pattern matching destructure: `case Vector(x, y):`.
    __match_args__ = ('x', 'y', 'z', 't')

    def __init__(self, components):
        # Protected by convention (single underscore), not name-mangled:
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        # reprlib.repr truncates long sequences with '...'.
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    # ------------------------------------------------------------------
    # SEQUENCE PROTOCOL  (duck typing)
    # ------------------------------------------------------------------
    # Python has no formal "Sequence interface" you must inherit. Implement
    # __len__ and __getitem__ and the object behaves like a sequence:
    # len(v), v[i], v[1:3], `in`, reversed(v), and iteration (even without
    # __iter__, via the __getitem__ fallback) all work.
    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        # a real int and raises TypeError for floats/strings, e.g. v[1.5].
        index = operator.index(key)
        return self._components[index]

    # ------------------------------------------------------------------
    # DYNAMIC ATTRIBUTE ACCESS  (v.x, v.y, v.z, v.t)
    # ------------------------------------------------------------------
    # __getattr__ is called ONLY when normal lookup fails. For `my_obj.x`:
    #   1. instance __dict__ -> 2. class -> 3. base classes
    #   4. only then: type(my_obj).__getattr__(my_obj, 'x')
    # (Contrast: __getattribute__ is called for EVERY lookup.)
    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'
        raise AttributeError(msg)

    # THE TRAP THIS CREATES:
    # If you assign v.x = 10, the instance now HAS a real attribute 'x' in
    # its __dict__, so __getattr__ is never called again for v.x: Python
    # just returns 10, while v[0] still holds the old value. The vector is
    # now inconsistent. (Demo 4 below reproduces this.)
    #
    # THE FIX: intercept ALL assignments with __setattr__.
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:                        # single-letter names only
            if name in cls.__match_args__:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''                        # 'A'..'Z', digits: allowed
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        # Everything else (e.g. '_components', 'foo') is stored normally.
        # super().__setattr__ is what actually writes into the instance.
        super().__setattr__(name, value)

    # WHY NOT __slots__ INSTEAD?
    # __slots__ stops *new* attributes, but it's the wrong tool here: it is
    # meant for memory savings, not for guarding API design, and it would
    # not produce our tailored error messages or protect x/y/z/t specifically.

    # ------------------------------------------------------------------
    # HYPERSPHERICAL COORDINATES
    # ------------------------------------------------------------------
    def angle(self, n):
        # n-th angular coordinate (n = 1 .. len-1) of the n-dimensional
        # spherical system: r is the length of the tail components from
        # index n on; atan2(r, previous component) is the angle.
        r = math.hypot(*self[n:])
        a = math.atan2(r, self[n - 1])
        # The LAST angle ranges over 0..2*pi, so flip it when the last
        # component is negative.
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        # A trailing 'h' means hyperspherical: <r, angle1, angle2, ...>.
        # Everything before it is forwarded to each number's format().
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets)[1:].cast(typecode)   # slice the view: no copy
        # NOTE: cls(memv), not cls(*memv). Vector.__init__ takes ONE iterable
        # (Vector2D took x, y separately, hence the star there).
        return cls(memv)

# NOTE (from the book): __str__, __eq__, __bool__ and frombytes barely changed
# from Vector2D (only the '*' in frombytes was removed). That's the payoff of
# making the original class iterable: everything else builds on iteration.


# ======================================================================
# DEMOS
# ======================================================================
print("=== 1. Basics & repr ===")
v = Vector([3, 4, 5])
print(repr(v), str(v), abs(v), bool(v), bool(Vector([0, 0])))
print(Vector(range(10)))                  # str shows everything
print(repr(Vector(range(10))))            # repr truncates: Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])

print("\n=== 2. Sequence protocol ===")
print(len(v), v[0], v[-1])
print(repr(v[1:]))                        # Vector([4.0, 5.0]) -> slice keeps the type
print(list(reversed(v)))                  # works via __len__ + __getitem__
print(4.0 in v)                           # `in` falls back to iteration
try:
    v[1.5]
except TypeError as e:
    print("v[1.5] ->", e)                 # operator.index rejects floats

print("\n=== 3. __getattr__ / __setattr__ ===")
print(v.x, v.y, v.z)                      # 3.0 4.0 5.0 via __getattr__
try:
    v.t                                   # only 3 components -> pos 3 out of range
except AttributeError as e:
    print(e)
try:
    v.x = 10                              # readonly
except AttributeError as e:
    print(e)
try:
    v.k = 1                               # single lowercase letter
except AttributeError as e:
    print(e)
v.X = 'ok'                                # uppercase single letter allowed
v.color = 'red'                           # longer names allowed
print(v.X, v.color)


print("\n=== 4. Why __setattr__ exists (the shadowing trap) ===")
class LooseVector(Vector):
    # Bypass our guard: restore plain object behaviour.
    __setattr__ = object.__setattr__


lv = LooseVector([3, 4, 5])
print(lv.x, lv[0])                        # 3.0 3.0 consistent
lv.x = 10                                 # now creates a real instance attribute
print(lv.x, lv[0])                        # 10 3.0 <- inconsistent! __getattr__ skipped
print(lv.__dict__.keys())                 # includes 'x'

print("\n=== 5. __hash__ / __eq__ ===")
print(Vector([1, 2]) == Vector([1, 2]), Vector([1, 2]) == (1.0, 2.0))
print(hash(Vector([1, 2])) == hash(Vector([1, 2])))
print(hash(Vector([1, 1])), hash(Vector([2, 2])))      # 0 0 -> XOR collision weakness
print(len({Vector([1, 2]), Vector([1, 2])}))           # 1 (usable in sets)

print("\n=== 6. bytes round trip ===")
b = bytes(Vector([1, 2, 3]))
print(len(b), Vector.frombytes(b))        # 25 (1 + 3*8) (1.0, 2.0, 3.0)

print("\n=== 7. __match_args__ and pattern matching ===")
for obj in (Vector([1, 2]), Vector([1, 2, 3]), Vector([])):
    match obj:
        case Vector(x, y, z):             # positional -> __match_args__ -> v.x, v.y, v.z
            print("3D:", x, y, z)
        case Vector(x, y):
            print("2D:", x, y)
        case _:
            print("other, length", len(obj))
# A class pattern only checks isinstance + that each named attribute can be
# read; it does NOT check length. Vector([1, 2, 3]) would ALSO match
# `Vector(x, y)` (it just ignores z), so the more specific 3D case must come
# first. Vector([1, 2]) fails the 3D case because v.z raises AttributeError,
# which the matcher treats as "no match".

print("\n=== 8. __format__ with 'h' (hyperspherical) ===")
print(format(Vector([3, 4])))                   # (3.0, 4.0)
print(format(Vector([3, 4]), '.2f'))            # (3.00, 4.00)
print(format(Vector([3, 4]), 'h'))              # <5.0, 0.9272952180016122>
print(format(Vector([3, 4]), '.3eh'))           # <5.000e+00, 9.273e-01>
print(format(Vector([1, 1, 1]), '0.5fh'))       # <1.73205, 0.95532, 0.78540>
print(format(Vector([1, 1, -1]), '.3fh'))       # last angle flipped to 2*pi - a
print(f'{Vector([2, 2, 2, 2]):.2fh}')           # f-strings use the same mechanism