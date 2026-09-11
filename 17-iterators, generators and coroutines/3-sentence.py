"""
How a generator works
======================

Any Python function that has the `yield` keyword in its body is a
*generator function*: a function which, when called, returns a
*generator object*. In other words, a generator function is a
generator factory.

Terminology matters here — it's confusing to say a generator "returns"
values. FUNCTIONS return values. GENERATORS yield values.

A generator doesn't "return" values in the usual sense: the `return`
statement inside a generator function's body doesn't hand back a
value to the caller of `next()`. Instead, it causes the generator
object to raise `StopIteration`, signaling that iteration is done.

    >>> def gen_123():
    ...     yield 1
    ...     yield 2
    ...     yield 3

    >>> gen_123                     # doctest: +ELLIPSIS
    <function gen_123 at 0x...>

    >>> gen_123()                   # doctest: +ELLIPSIS
    <generator object gen_123 at 0x...>

    >>> for i in gen_123():         # a generator is iterable
    ...     print(i)
    1
    2
    3

    >>> g = gen_123()
    >>> next(g)
    1
    >>> next(g)
    2
    >>> next(g)
    3
    >>> next(g)
    Traceback (most recent call last):
      ...
    StopIteration

A generator function builds a generator object that WRAPS the body of
the function. When you call `next()` on the generator object:

  1. Execution advances to the next `yield` in the function body.
  2. The function body is *suspended* right there — all local state
     (variables, the instruction pointer, the call stack frame) is
     preserved, not discarded.
  3. The value passed to `yield` becomes the return value of that
     `next()` call.

When the function body eventually returns (falls off the end, or hits
an explicit `return`), the generator object raises `StopIteration`
internally — this is how Python's Iterator protocol signals "no more
items" to whatever is driving the iteration (a `for` loop, a
comprehension, `next()` calls, etc.).

Key distinction to keep straight:
  - `iterable`  -> an object you can call `iter()` on to GET an iterator
                   (e.g. our Sentence object below, via `__iter__`).
  - `iterator`  -> an object with `__next__()` that produces values
                   one at a time and raises StopIteration when done.
  - `generator` -> a convenient way to IMPLEMENT an iterator without
                   manually writing a class with `__next__` and
                   internal state — Python builds that state machine
                   for you from a function containing `yield`.
"""

import re
import reprlib

# Matches runs of word characters — used to split the text into words.
RE_WORD = re.compile(r'\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s)                 
    print(list(s))   
    print(list(s))           