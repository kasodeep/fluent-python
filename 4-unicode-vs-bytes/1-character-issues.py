"""
The concept of string is simple enough, a string is a sequence of characters.
The problem lies in the definition of “character.”

The Unicode standard explicitly separates the identity of characters from specific
byte representations:

1. The identity of a character—its code point—is a number from 0 to 1,114,111
(base 10), shown in the Unicode standard as 4 to 6 hex digits with a “U+” prefix.

2. The actual bytes that represent a character depend on the encoding in use. An
encoding is an algorithm that converts code points to byte sequences and vice
versa.
"""

s = 'café'
print(s, len(s))

b = s.encode('utf-8')
print(b, len(b))

print(b.decode('utf-8'))

# Bytes Essentials

cafe = bytes('café', encoding='utf-8')
print(cafe, len(cafe))

# cafe[0] returns an item, which is an int. ord('c') is 99.
# cafe[:1] returns a slice, which is always the same type as the container.
print(cafe[0], cafe[:1])

cafe_arr = bytearray(cafe)
print(cafe_arr, len(cafe_arr))
print(cafe_arr[-1:])
