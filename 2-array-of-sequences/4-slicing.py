import dis

l = [10, 20, 30, 40, 50]
print(l[1:4])  # Output: [20, 30, 40]
print(l[1:4:2])  # Output: [20, 40]

s = 'bicycle'
print(s[::-1])

l = list(range(10))
l[2:5] = [20, 30]
del l[5:7]

print(l)  # Output: [0, 1, 20, 30, 5, 6, 7, 8, 9]

l[2:5] = 100

# Use * and + operators with slices
l = [1, 2, 3, 4, 5]
print(l[1:4] * 2)  # Output: [2, 3, 4, 2, 3, 4]

my_list = [[]] * 3
print(my_list)
my_list[0].append(1)
print(my_list)

# Building list of list
board = [['_'] * 3 for i in range(3)]
print(board)  # Output: [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

print(weird_board = [['_'] * 3] * 3) # useless

"""
For mutable sequences (list, bytearray), *= calls __imul__, which modifies the object in place — same object, same id(), just its contents changed.
For immutable sequences (tuple, str), there's no __imul__, so a *= n falls back to a = a * n — Python builds a new object and rebinds a to it, so id(a) changes.
"""

t = (1, 2, [3, 4])
t[2] += [5, 6]

print(dis.dis('t = (1, 2, [3, 4]); t[2] += [5, 6]'))

"""
- Avoid putting mutable items in tuples.
- Augmented assignment is not an atomic operation—we just saw it throwing an
exception after doing part of its job.
•- Inspecting Python bytecode is not too difficult, and can be helpful to see what is
going on under the hood.
"""