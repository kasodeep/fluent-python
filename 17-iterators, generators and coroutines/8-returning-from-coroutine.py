from collections.abc import Generator
from typing import NamedTuple, Union

class Result(NamedTuple):
    count: int
    average: float

class Sentinel:
    def __repr__(self) -> str:
        return "<Sentinel>"

STOP = Sentinel()

SendType = Union[float, Sentinel]

def averager2(verbose: bool = False) -> Generator[None, SendType, Result]:
    """
    This coroutine returns a result when it is closed. The result is a named tuple
    containing the count and the average of the numbers sent to it.
    """
    total = 0.0
    count = 0

    average = 0.0
    while True:
        term = yield
        if verbose:
            print(f"Received term: {term}")
        if isinstance(term, Sentinel):
            break
        total += term
        count += 1
        average = total / count

    return Result(count, average)

coro_avg2 = averager2(verbose=True)
next(coro_avg2)  # Prime the coroutine
print(coro_avg2.send(10))  # None
print(coro_avg2.send(30))  # None

try:
    coro_avg2.send(STOP)  # Terminate the coroutine and get the result
except StopIteration as e:
    result = e.value
    print(f"Count: {result.count}, Average: {result.average}")  # Count: 2, Average: 20.0

def compute():
    res = yield from averager2(verbose=True)
    print(f"Count: {res.count}, Average: {res.average}")
    return res
