"""
Python variables are like reference variables in Java;
a better metaphor is to think of variables as labels with names attached to objects.
"""
 
a= [1, 2, 3]
b = a
a.append(4)
 
print(b)
"""
Therefore, the b = a statement does not copy the contents of box a into box b.
It attaches the label b to the object that already has the label a.
 
Python’s assignment statement x = … binds the x name to the object created
or referenced on the righthand side.
"""
 
class Gizmo:
    def __int__(self):
        print(f'Gizmo id: {id(self)}')
 
x = Gizmo()
y = Gizmo() * 10
# y will never be created.
print(dir())