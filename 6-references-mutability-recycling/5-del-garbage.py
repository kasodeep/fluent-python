
"""
Python’s garbage collector may discard an object from memory as an indirect result of del,
if the deleted variable was the last reference to the object.
 
Rebinding a variable may also
cause the number of references to an object to reach zero, causing its destruction.
"""
 
a = [1, 2]
b = a
del a
 
print(b)
b = [3] # now the above object [1, 2] is deleted.