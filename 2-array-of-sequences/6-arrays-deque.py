"""
The list type is flexible and easy to use, but depending on specific requirements,
there are better options. For example, an array saves a lot of memory when you need
to handle millions of floating-point values.
"""

from array import array
from random import random

floats = array('d', (random() for i in range(10**7)))
print(floats[-1])  # prints the last element of the array

fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()

floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close()

floats2[-1]  # prints the last element of the array
print(floats2[-1] == floats[-1])  # prints True

from collections import deque

dq = deque(range(10), maxlen=10)
dq.rotate(3)
print(dq)  # prints deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6])

dq.extendleft([-1, -2, -3])
print(dq)  # prints deque([-3, -2, -1, 7, 8, 9, 0, 1, 2, 3])
dq.extendleft([11, 12, 13])
print(dq)  # prints deque([13, 12, 11, -3, -2, -1, 7, 8, 9, 0])