 
from dataclasses import field


@dataclass(init=True, repr=True, eq=True, order=True, frozen=False, unsafe_hash=False)
class Temp:
    pass
 
"""
If the eq and frozen arguments are both True, @dataclass produces a suitable
__hash__ method, so the instances will be hashable.
If frozen=False (the default), @dataclass will set
__hash__ to None, signalling that the instances are unhashable, therefore overriding
__hash__ from any superclass.
"""
 
# Field Options
 
# the default value is set by calling the dataclasses.field function with default_factory=list.
# It’s good that @dataclass rejects class definitions with a list default value in a field
@dataclass
class ClubMember:
    name: str
    guests: list[str] = field(default_factory=list)
    athlete: bool = field(default=False, repr=False)
 
# We can also have Post-Init processing
 
"""
Here, <factory> is a short way of saying that some callable will produce the default
value for guests (in our case, the factory is the list class). The point is: to provide a
handle but no guests, we must pass handle as a keyword argument.
"""
 
from dataclasses import dataclass, InitVar
from club import ClubMember
 
@dataclass
class HackerClubMember(ClubMember):
    all_handles = set() # no annotation: shared by instances
    handle: str = '' # type annotation: instance attribute
 
    def __post_init__(self):
        cls = self.__class__
 
        if self.handle == '':
            self.handle = self.name.split()[0]
 
        if self.handle in cls.all_handles:
            msg = f'handle {self.handle!r} is already taken'
            raise ValueError(msg)
        cls.all_handles.add(self.handle)
 
"""
To make the type checker and @dataclass happy, this is how we are supposed to
declare all_handles
 
all_handles: ClassVar[set[str]] = set()
"""
 
"""
Sometimes you may need to pass arguments to __init__ that are not instance fields.
Such arguments are called init-only variables
"""
 
from dataclasses import dataclass, InitVar
 
class DatabaseType:
    def lookup(self, key):
        return 42
 
@dataclass
class C:
    i: int
    j: int = None
    database: InitVar[DatabaseType] = None
 
    def __post_init__(self, database):
        if self.j is None and database is not None:
            self.j = database.lookup('j')
 
c = C(10, database=DatabaseType())
print(c)   # C(i=10, j=42)
 