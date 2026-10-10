import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()

        result = func(*args)
        elapsed = time.perf_counter() - t0

        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        
        print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
        return result
    return clocked

@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)

if __name__ == '__main__':
    print('*' * 40, 'Calling factorial(6)')
    print(factorial(6))

"""
The clock decorator implemented in Example 9-14 has a few shortcomings: it does
not support keyword arguments, and it masks the __name__ and __doc__ of the decorated function.

Example 9-16 uses the functools.wraps decorator to copy the relevant attributes from func to clocked.
Also, in this new version, keyword arguments are correctly handled.
"""

import time
import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()

        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0

        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = [f"{k}={w!r}" for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)

        print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
        return result
    return clocked

# functools.cache
# lru_cache = functools.lru_cache(maxsize=2**10)

