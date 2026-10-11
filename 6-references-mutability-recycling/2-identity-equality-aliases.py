charles = {'name': 'Charles L. Dodgson', 'born': 1832}
lewis = charles
 
print(lewis is charles)
print(id(charles), id(lewis))
 
# lewis and charles are aliases, two variables bound to the same object.
# The object bound to alex and charles have the same value: == compares that, but they have different identities.
 
alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}
 
print(alex == charles)
print(alex is not charles)
 
"""
In contrast, a == b is syntactic sugar for a.__eq__(b).
The __eq__ method inherited from object compares object IDs, so it produces the same result as is
 
But most built-in types override __eq__ with more
meaningful implementations that actually take into account the values of the object attributes.
"""