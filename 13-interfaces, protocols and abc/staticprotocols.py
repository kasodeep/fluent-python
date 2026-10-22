from typing import TypeVar, Protocol

T = TypeVar('T')

class Repeatable(Protocol):
    def __mul__(self: T, repeat_count: int) -> T: ...

RT = TypeVar('RT', bound=Repeatable)
    
def double(x: RT) -> RT:
    return x * 2

"""
When defining a typing.Protocol subclass, you can use the @runtime_checkable decorator
to make that protocol support isinstance/issubclass checks at runtime.
"""
@runtime_checkable
class SupportsComplex(Protocol):
    """An ABC with one abstract method __complex__."""
    __slots__ = ()
    
    @abstractmethod
    def __complex__(self) -> complex:
        pass