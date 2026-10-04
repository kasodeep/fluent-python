"""
Data Class Builders in Python (Fluent Python, Ch. 5)
=====================================================

Three builders:
    1. collections.namedtuple   -> function-call syntax, immutable, tuple subclass
    2. typing.NamedTuple        -> class syntax + type hints, immutable, tuple subclass
    3. dataclasses.dataclass    -> class decorator, mutable by default, plain class

Run this file directly: every assert should pass and prints show the behaviour.
"""

import typing
from collections import namedtuple
from dataclasses import dataclass, field, fields, asdict, replace, make_dataclass


# =============================================================================
# 1. THE PROBLEM: __init__ boilerplate
# =============================================================================
# Each attribute is mentioned THREE times (parameter, left of '=', right of '=').
# No useful __repr__ and no value-based __eq__ either.
class PlainCoordinate:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon


# Without __repr__ / __eq__, two "equal" objects are not equal:
assert PlainCoordinate(55.75, 37.61) != PlainCoordinate(55.75, 37.61)


# =============================================================================
# 2. collections.namedtuple  (function call syntax)
# =============================================================================
CoordinateNT = namedtuple('CoordinateNT', ['lat', 'lon'])

# It builds a tuple SUBCLASS (via metaprogramming that injects methods/attrs).
assert issubclass(CoordinateNT, tuple)

moscow = CoordinateNT(55.75, 37.61)
print(moscow)                                   # CoordinateNT(lat=55.75, lon=37.61)
assert moscow == CoordinateNT(55.75, 37.61)     # value-based equality
assert moscow == (55.75, 37.61)                 # it is also just a tuple
lat, lon = moscow                               # unpacking works


# =============================================================================
# 3. typing.NamedTuple  (function-call form AND class form)
# =============================================================================
# 3a. Function-call form: pairs of (name, type)
CoordinateTD = typing.NamedTuple('CoordinateTD', [('lat', float), ('lon', float)])
assert issubclass(CoordinateTD, tuple)


# 3b. Class statement form: the most readable, supports defaults and methods.
# (Original notes called this "CoordinateDC", which is misleading: it is a
#  NamedTuple, not a dataclass. Renamed to CoordinateCNT.)
class CoordinateCNT(typing.NamedTuple):
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        ew = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{ew}'


assert issubclass(CoordinateCNT, tuple)         # still a tuple subclass
print(CoordinateCNT(55.75, 37.61))              # 55.8°N, 37.6°E

# =============================================================================
# 4. dataclasses.dataclass  (class decorator)
# =============================================================================
# The decorator does not use inheritance or a metaclass, so it does not
# interfere with your own use of either. It just edits the class in place.
#
# Original notes had a typo: `fronzen=True`. Correct spelling: `frozen=True`.
@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        ew = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat)}°{ns}, {abs(self.lon)}°{ew}'


c = Coordinate(55.75, 37.61)
print(c)                                        # 55.75°N, 37.61°E
print(repr(c))                                  # Coordinate(lat=55.75, lon=37.61)
assert not issubclass(Coordinate, tuple)        # plain class, NOT a tuple

# frozen=True makes instances immutable (and hashable together with eq=True).
try:
    c.lat = 0.0
except Exception as e:                          # dataclasses.FrozenInstanceError
    print('frozen ->', type(e).__name__)


# =============================================================================
# 5. COMPARISON: key properties
# =============================================================================
"""
Mutable?
    namedtuple / NamedTuple : immutable (they are tuples)
    dataclass               : mutable by default; frozen=True makes it immutable

Class statement syntax?
    typing.NamedTuple and @dataclass use `class` syntax.
    collections.namedtuple uses a function call only.

Convert instance to dict?
    namedtuple / NamedTuple : instance._asdict()
    dataclass               : dataclasses.asdict(instance)

Inheritance / metaprogramming?
    namedtuple, NamedTuple  : build tuple subclasses
    @dataclass              : decorator, class hierarchy untouched
"""

assert moscow._asdict() == {'lat': 55.75, 'lon': 37.61}
assert asdict(c) == {'lat': 55.75, 'lon': 37.61}


# =============================================================================
# 6. GET FIELD NAMES AND DEFAULT VALUES
# =============================================================================
# namedtuple / NamedTuple: class attributes ._fields and ._field_defaults
# (Book text says "_fields_defaults"; the real attribute is `_field_defaults`.)
CoordWithDefault = namedtuple('CoordWithDefault', ['lat', 'lon'], defaults=[0.0])
assert CoordWithDefault._fields == ('lat', 'lon')
assert CoordWithDefault._field_defaults == {'lon': 0.0}   # defaults bind from the RIGHT


# dataclass: dataclasses.fields() returns a tuple of Field objects
# (attributes include .name, .type, .default, .default_factory)
@dataclass
class Trip:
    name: str
    stops: list = field(default_factory=list)   # mutable defaults need default_factory
    days: int = 1


for f in fields(Trip):
    print(f.name, f.type, f.default, f.default_factory)

assert [f.name for f in fields(Trip)] == ['name', 'stops', 'days']
assert fields(Trip)[2].default == 1


# =============================================================================
# 7. GET FIELD TYPES
# =============================================================================
# typing.NamedTuple and @dataclass store a name -> type mapping in __annotations__.
# Prefer typing.get_type_hints(): it resolves string/forward references, whereas
# raw __annotations__ may hold unevaluated strings.
assert typing.get_type_hints(CoordinateCNT) == {'lat': float, 'lon': float}
assert typing.get_type_hints(Trip) == {'name': str, 'stops': list, 'days': int}
# collections.namedtuple has no types, so there is nothing to retrieve.


# =============================================================================
# 8. NEW INSTANCE WITH CHANGES  (the immutable-friendly "update")
# =============================================================================
# namedtuple / NamedTuple : x._replace(**kwargs)
# dataclass               : dataclasses.replace(x, **kwargs)
# Both return a NEW object. The original is untouched.
moved_nt = moscow._replace(lat=0.0)
assert moved_nt == CoordinateNT(0.0, 37.61) and moscow.lat == 55.75

moved_dc = replace(c, lat=0.0)                  # works even on a frozen dataclass
assert moved_dc == Coordinate(0.0, 37.61) and c.lat == 55.75


# =============================================================================
# 9. NEW CLASS AT RUNTIME
# =============================================================================
# `class` syntax is readable but hardcoded. Frameworks that must build classes
# on the fly use the function forms:
#   collections.namedtuple(...)   and   typing.NamedTuple(...)   (shown above)
#   dataclasses.make_dataclass(...)
Point = make_dataclass(
    'Point',
    [('x', float), ('y', float, field(default=0.0))],
)
p = Point(1.5)
print(p)                                        # Point(x=1.5, y=0.0)
assert [f.name for f in fields(Point)] == ['x', 'y']


# =============================================================================
# 10. WHEN TO USE WHICH
# =============================================================================
"""
namedtuple      : quick immutable record, no types, need tuple behaviour/unpacking
typing.NamedTuple: same, but with type hints, defaults, and methods in class form
@dataclass      : need mutability, inheritance-friendly design, field(), __post_init__,
                  or frozen/slots/order options; not a tuple, so no unpacking by default
"""

print('\nAll assertions passed.')