"""
Goose typing property is the ability to register a class as a virtual subclass of an ABC, even if it
does not inherit from it.
"""

from random import randrange
from implement import Tombola

@Tombola.register
class TombolaList(list):

    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(self)

"""
Note that because of the registration, the functions issubclass and isinstance act
as if TomboList is a subclass of Tombola
"""

print(TombolaList.__mro__)
print(issubclass(TombolaList, Tombola))