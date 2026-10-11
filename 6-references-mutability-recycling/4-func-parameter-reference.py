"""
The only mode of parameter passing in Python is call by sharing.
In other words, the parameters inside the function become aliases of the actual arguments.
 
The result of this scheme is that a function may change any mutable object passed as
a parameter, but it cannot change the identity of those objects.
"""
 
def f(a, b):
    a += b
    return a
 
a=[1, 2]
b=[3, 4]
f(a, b)
print(a, b)
 
t = (10, 20)
u = (30, 40)
f(t, u)
print(t, u) # func does not change any immutable object.
 
"""
You should avoid mutable objects as default values for parameters.
"""
 
class HauntedBus:
    """A bus model haunted by ghost passengers"""
 
    def __init__(self, passengers=[]):
        self.passengers = passengers
 
    def pick(self, name):
        self.passengers.append(name)
 
    def drop(self, name):
        self.passengers.remove(name)
 
"""
Strange things happen only when a HauntedBus starts empty,
because then self.passengers becomes an alias for the default value of the passengers parameter.
The problem is that each default value is evaluated when the function is defined.
"""
 
# Defensive Programming with Mutable Parameters
basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
 
print(basketball_team)
 
class TwilightBus:
    """A bus model that makes passengers vanish"""
 
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers # we should use list(passengers)
 
    def pick(self, name):
        self.passengers.append(name)
 
    def drop(self, name):
        self.passengers.remove(name)
 
"""
Unless a method is explicitly intended to mutate an object received as an argument,
You should think twice before aliasing the argument object by simply assigning it to an instance variable in your class.
If in doubt, make a copy. Your clients will be happier.
"""
 