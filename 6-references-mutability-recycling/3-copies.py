"""
The easiest way to copy a list (or most built-in mutable collections) is to use the builtin constructor for the type itself.
"""
 
l1 = [3, [44, 55], (7, 8, 9)]
l2 = list(l1)
 
print(l2)
print(l2 is l1) # Output: None
 
"""
However, using the constructor or [:] produces a shallow copy (i.e., the outermost
container is duplicated, but the copy is filled with references to the same items held
by the original container)
"""
 
# Deep Copies
 
class Bus:
 
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)
 
    def pick(self, name):
        self.passengers.append(name)
 
    def drop(self, name):
        self.passengers.remove(name)
 
import copy
 
bus1 = Bus(['Alice', 'Bill', 'Carol'])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)
 
print(id(bus1), id(bus2), id(bus3))
bus1.drop('Alice')
print(bus2.passengers)
 
print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))
 
# deepcopy function is smart to not go into the cyclic loop with this reference game.
a = [10, 20]
b = [a, 30]
a.append(b)
 
print(a)
c = copy.deepcopy(a)
print(c)
 