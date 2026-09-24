"""Notes: sequence types, list comprehensions, generator expressions."""

# --- Container vs Flat sequences ---
# Container: holds references to objects of any type (list, tuple, deque)
# Flat: stores values directly in its own memory, one simple type (str, bytes, array.array)

# --- Mutable vs Immutable sequences ---
# Mutable:   list, bytearray, array.array, collections.deque
# Immutable: tuple, str, bytes


# --- List comprehensions ---
symbols = '$¢£¥€¤'
codes = [ord(symbol) for symbol in symbols]
print(codes)

# walrus operator: assign inside the comprehension and reuse the value after
codes2 = [last := ord(c) for c in symbols]
print(codes2, "last seen:", last)

# filter with a condition
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
print(beyond_ascii)

# same result using filter/map instead of a comprehension
beyond_ascii2 = list(filter(lambda c: c > 127, map(ord, symbols)))
print(beyond_ascii2)

# cartesian product: one loop per "for" clause
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors for size in sizes]
print(tshirts)


# --- Generator expressions ---
# Same syntax as list comprehension but with () instead of []
# Doesn't build the whole list in memory -- yields items one by one.

print(tuple(ord(symbol) for symbol in symbols))

import array
print(array.array('I', (ord(symbol) for symbol in symbols)))

for tshirt in (f'{c} {s}' for c in colors for s in sizes):
    print(tshirt)