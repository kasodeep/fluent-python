"""Notes: tuples as records vs immutable lists, and sequence unpacking."""

# --- Tuples as records ---
# Position carries meaning (e.g. (lat, lon)), unlike tuple-as-immutable-list use.

# --- Tuples as immutable lists ---
# Clarity: length never changes.
# Performance: less memory than a list of the same length.

# Immutability only applies to the tuple's own references, not to mutable
# objects those references point to.
a = (10, 'alpha', [1, 2])
b = (10, 'alpha', [1, 2])
print(a == b)          # True
b[-1].append(99)       # mutating the list inside b
print(a == b)          # False -- b's tuple "value" changed even though it's immutable
print(b)


# A tuple is only hashable if ALL its items are hashable.
def fixed(o):
    try:
        hash(o)
    except TypeError:
        return False
    return True

tf = (10, 'alpha', (1, 2))   # all immutable items
tm = (10, 'alpha', [1, 2])   # contains a list -> unhashable
print(fixed(tf))  # True
print(fixed(tm))  # False


# --- Unpacking sequences ---
a, b, *rest = range(5)
print(a, b, rest)   # 0 1 [2, 3, 4]

a, b, *rest = range(3)
print(a, b, rest)   # 0 1 [2]

a, b, *rest = range(2)
print(a, b, rest)   # 0 1 []


# *args-style unpacking also works when calling a function
def fun(a, b, c, d, *rest):
    return a, b, c, d, rest

print(fun(*[1, 2], 3, *range(4, 7)))   # (1, 2, 3, 4, (5, 6))