"""
The first thing you need to know about type hints is that they are not enforced at all
by the Python bytecode compiler and interpreter.
"""

# Meaning of variable annotations:
from typing import NamedTuple


class DemoPlainClass:
    x: int
    y: float = 0.0
    c = 'deep'

print(DemoPlainClass.__annotations__)   # {'x': <class 'int'>, 'y': <class 'float'>}
print(DemoPlainClass.a) # Error: 'DemoPlainClass' object has no attribute 'a'

"""
The a survives only as an annotation. It doesn’t become a class attribute because no
value is bound to it.6 The b and c are stored as class attributes because they are bound
to values.
"""

class DemoNTClass(NamedTuple):
    x: int
    y: float = 0.0
    c = 'deep'

print(DemoNTClass.a)
print(DemoNTClass.b)
print(DemoNTClass.c)
print(DemoNTClass.__doc__)

'''
The a and b class attributes are descriptors.
In practice, this means a and b will work as read-only instance attributes—which makes sense when
we recall that DemoNTClass instances are just fancy tuples, and tuples are immutable.
'''
