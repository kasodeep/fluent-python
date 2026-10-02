"""
A dictcomp builds a dict instance by taking key:value pairs from any iterable.
"""

dial_codes = [
    (+1, 'United States'),
    (+44, 'United Kingdom'),
    (+91, 'India'),
]

country_code = {country: code for code, country in dial_codes}

# Unpack mappings

def dump(**kwargs):
    for k, v in kwargs.items():
        print(f"{k} = {v}")

print(dump(**{'a': 1}, b=2, **{'c': 3})) # duplicate keys, last one wins.

"""
An object is hashable if it has a hash code which never changes during its lifetime (it
needs a __hash__() method), and can be compared to other objects (it needs an
__eq__() method). Hashable objects which compare equal must have the same hash
code.
"""

tt = (1, 2, [3, 4])  # tuple is hashable, but not if it contains a mutable object like a list
hash(tt)  # TypeError: unhashable type: 'list'



