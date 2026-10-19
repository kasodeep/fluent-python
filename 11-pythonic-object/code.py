"""
Vector2D study notes (Fluent Python style)
Topics: name mangling, @property, __slots__, class-attribute overriding,
        __format__ / str.format / format() / f-strings.
Run it:  python vector2d_notes.py
"""

from array import array
import math


class Vector2D:
    # ------------------------------------------------------------------
    # CLASS ATTRIBUTE
    # ------------------------------------------------------------------
    # Lives on the class, shared by all instances. Used by __bytes__ /
    # frombytes as the array typecode: 'd' = 8-byte double, 'f' = 4-byte float.
    # A subclass (or even a single instance) can override it (see below).
    typecode = 'd'

    def __init__(self, x, y):
        # NAME MANGLING, NOT PRIVACY:
        # The compiler rewrites `self.__x` to `self._Vector2D__x` (only for
        # code written inside this class body). It prevents accidental
        # collisions in subclasses, e.g. Dog.__mood -> _Dog__mood and
        # Beagle.__mood -> _Beagle__mood are two separate attributes.
        # Anyone can still do v._Vector2D__x = 99, so it is not real privacy.
        self.__x = float(x)
        self.__y = float(y)

    # READ-ONLY ACCESS:
    # A property with a getter and NO setter -> `v.x = 10` raises
    # AttributeError. Needed because we define __hash__: hashable objects
    # must not change value while they sit in a set / dict key.
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        # Makes the object iterable -> enables unpacking `x, y = v`,
        # tuple(v), and the `*self` used in __repr__ / __bytes__.
        # (Simpler equivalent: `yield self.x; yield self.y`.)
        return (i for i in (self.x, self.y))

    def __repr__(self):
        # type(self).__name__ (not a hardcoded 'Vector2D') so subclasses
        # print their own name, e.g. ShortVector2D(3.0, 4.0).
        # {!r} = call repr() on the value, so floats show as 3.0, not '3.0'.
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        # Layout: [1 byte: typecode char][raw bytes of the numbers]
        # ord('d') -> 100, bytes([100]) -> b'd'
        # array(typecode, self) builds a typed array from our iterable;
        # bytes(array) gives its raw memory.
        return (bytes([ord(self.typecode)])
                + bytes(array(self.typecode, self)))

    def __eq__(self, other):
        # Note: this raises TypeError if `other` is not iterable (e.g. v == 3).
        # A more defensive version would catch that and return NotImplemented.
        # It also makes Vector2D(3, 4) == (3.0, 4.0) True, which may or may
        # not be what you want.
        return tuple(self) == tuple(other)

    def __hash__(self):
        # Must agree with __eq__: equal objects -> equal hashes.
        # Safe only because x and y are effectively immutable.
        return hash((self.x, self.y))

    def __abs__(self):
        # Euclidean length. math.hypot avoids overflow/underflow vs sqrt(x*x+y*y).
        return math.hypot(self.x, self.y)

    def __bool__(self):
        # Falsy only for the zero vector.
        return bool(abs(self))

    def angle(self):
        # Polar angle in radians, used by the 'p' format below.
        return math.atan2(self.y, self.x)

    # ------------------------------------------------------------------
    # CUSTOM FORMAT SPEC  (used by format(v, spec), '{:spec}'.format(v),
    # and f'{v:spec}')
    # ------------------------------------------------------------------
    def __format__(self, fmt_spec=''):
        # Python hands us everything after the colon as fmt_spec.
        # We invent our own mini-language: a trailing 'p' means polar
        # coordinates <r, theta>; the rest of the spec is passed along
        # to each float.
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())   # (r, theta)
            outer_fmt = '<{}, {}>'
        else:
            coords = self                        # (x, y)
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    # ------------------------------------------------------------------
    # ALTERNATIVE CONSTRUCTOR
    # ------------------------------------------------------------------
    # @classmethod -> receives the CLASS as first arg (cls).
    # A @staticmethod receives no implicit first argument at all.
    # Using cls(...) instead of Vector2D(...) lets subclasses get instances
    # of themselves back.
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])                       # int 100 -> 'd'
        # Slice the memoryview (no copy). octets[1:] on bytes WOULD copy.
        memv = memoryview(octets)[1:].cast(typecode)    # reinterpret as floats
        return cls(*memv)                               # unpack -> cls(x, y)


# ======================================================================
# DEMO 1: name mangling
# ======================================================================
print("=== 1. Name mangling ===")
v1 = Vector2D(3, 4)
print(v1.__dict__)            # {'_Vector2D__x': 3.0, '_Vector2D__y': 4.0}
try:
    v1.__x                    # looked up literally as '__x' -> not found
except AttributeError as e:
    print("v1.__x fails:", e)
print("mangled access works:", v1._Vector2D__x)
try:
    v1.x = 10                 # property without setter
except AttributeError as e:
    print("v1.x = 10 fails:", e)


# ======================================================================
# DEMO 2: __slots__
# ======================================================================
# __slots__ replaces the per-instance __dict__ with a fixed hidden array of
# references. Saves memory when you have millions of instances.
class Pixel:
    __slots__ = ('x', 'y')


print("\n=== 2. __slots__ ===")
p = Pixel()
try:
    print(p.__dict__)         # Pixel instances have NO __dict__
except AttributeError as e:
    print("Pixel has no __dict__:", e)

p.x = 1
try:
    p.color = 'red'           # not in __slots__
except AttributeError as e:
    print("can't add new attribute:", e)


# A subclass that does NOT redeclare __slots__ gets a __dict__ again.
class OpenPixel(Pixel):
    pass


op = OpenPixel()
print(op.__dict__)            # {}   <- surprise: a dict exists
op.x = 8                      # 'x' is a slot of the base -> stored in the
print(op.__dict__)            # {}      hidden array, NOT in __dict__
print(op.x)                   # 8
op.color = 'green'            # not a slot -> goes into __dict__
print(op.__dict__)            # {'color': 'green'}


# Redeclare __slots__ in the subclass to keep instances dict-free.
class ColorPixel(Pixel):
    __slots__ = ('color',)    # slots are x, y (inherited) + color
    # __slots__ = ()  would mean "add nothing, but stay dict-free"


cp = ColorPixel()
cp.x, cp.y, cp.color = 1, 2, 'blue'
print(hasattr(cp, '__dict__'))   # False

# CAVEATS OF __slots__ (from the book):
#  - Redeclare __slots__ in every subclass, or instances get a __dict__.
#  - Only attributes listed in __slots__ are allowed, unless you include
#    '__dict__' in __slots__ (which may negate the memory savings).
#  - @cached_property doesn't work unless '__dict__' is in __slots__.
#  - No weak references unless '__weakref__' is in __slots__.


# ======================================================================
# DEMO 3: overriding class attributes
# ======================================================================
# `typecode` is a class attribute used as a default. Overriding it in a
# subclass changes behaviour without touching the parent's code.
class ShortVector2D(Vector2D):
    typecode = 'f'            # 4-byte floats instead of 8-byte doubles


print("\n=== 3. Overriding class attributes ===")
v = Vector2D(3, 4)
sv = ShortVector2D(3, 4)
print(len(bytes(v)), len(bytes(sv)))        # 17 vs 9  (1 + 2*8, 1 + 2*4)
print(repr(sv))                             # ShortVector2D(3.0, 4.0)
print(ShortVector2D.frombytes(bytes(sv)))   # (3.0, 4.0)  -> cls is ShortVector2D

# Setting it on an INSTANCE creates an instance attribute that shadows the
# class one (the class attribute itself is untouched). Can't do it on
# Vector2D if __slots__ were used, but here it works because we have a __dict__.
v.typecode = 'f'
print(len(bytes(v)), Vector2D.typecode)     # 9 'd'


# ======================================================================
# DEMO 4: bytes round trip
# ======================================================================
print("\n=== 4. bytes round trip ===")
b = bytes(Vector2D(3, 4))
print(b)                                    # b'd\x00...@' (typecode + 16 bytes)
print(Vector2D.frombytes(b) == Vector2D(3, 4))   # True