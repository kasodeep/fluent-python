from collections.abc import Generator

def average() -> Generator[float, float, None]:
    """
    That’s why coroutines are attractive replacements for callbacks in asynchronous programming,
    they keep local state between activations. (total and count)
    """
    total = 0.0
    count = 0

    average = 0.0
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count

coro_avg = average()
next(coro_avg)  # Prime the coroutine
print(coro_avg.send(10))  # 10.0
print(coro_avg.send(30))  # 20.0

"""
We dont usually need to terminate a generator, because it is garbage collected as soon as
there are no more valid references to it. If you need to explicitly terminate it, use
the .close() method

It raises GeneratorExit at the suspended yield expression.
If not handled in the coroutine function, the exception terminates it. Generator
Exit is caught by the generator object that wraps the coroutine—thats why we dont see it.
"""

coro_avg.close()  # Terminate the coroutine