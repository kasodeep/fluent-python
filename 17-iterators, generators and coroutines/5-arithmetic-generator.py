"""
My rule of thumb in choosing the syntax to use is simple: if the generator expression
spans more than a couple of lines, I prefer to code a generator function for the sake of
readability.
"""

class ArithmeticProgression:

    def __init__(self, begin, step, end=None):
            self.begin = begin
            self.step = step
            self.end = end

    def __iter__(self):
          result_type = type(self.begin + self.step)
          result = result_type(self.begin)

          forever = self.end is None
          index = 0

          while forever or result < self.end:
                yield result
                index += 1

                # This avoids the cumulative effect of floating-point errors after successive additions.
                result = self.begin + self.step * index

"""
>>> 100 * 1.1
110.00000000000001
>>> sum(1.1 for _ in in range(100))
109.99999999999982
>>> 1000 * 1.1
1100.0
>>> sum(1.1 for _ in range(1000))
1100.0000000000086
"""

"""
However, if the whole point of a class is to build a generator by implementing __iter__, 
we can replace the class with a generator function. A generator function is, after all, a generator factory.
"""

def aritprog_gen(begin, step, end=None):
    result_type = type(begin + step)
    result = result_type(begin)

    forever = end is None
    index = 0

    while forever or result < end:
        yield result
        index += 1

        # This avoids the cumulative effect of floating-point errors after successive additions.
        result = begin + step * index      

import itertools

# gen = itertools.count(1, .5) It does, not have an end list(count()) breaks the memory.

def aritprog_gen_library(begin, step, end=None):
    """
    It is not a generator function: it has no yield in its body.
    But it returns a generator, just as a generator function does.
    """

    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)

    if end is None:
        return ap_gen
    return itertools.takewhile(lambda n: n < end, ap_gen)