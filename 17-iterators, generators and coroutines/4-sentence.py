"""
Lazy implementations of Sentence
=================================

The previous version (`words = RE_WORD.findall(text)`) is EAGER: the
instant you construct a Sentence, the entire text is scanned and every
word is matched and stored in a list — even if the caller only ever
asks for the first word.

Both versions below are LAZY: no scanning happens at construction
time. Work happens incrementally, word by word, only as the caller
actually asks for the next item. For a huge text (or a stream you
can't even fit in memory), lazy evaluation means you only pay for the
words you actually consume.

The key tool that makes this possible is `re.finditer()` instead of
`re.findall()`:
  - `findall()` -> runs the regex over the whole string immediately
                   and returns a LIST of all matches (eager).
  - `finditer()` -> returns a GENERATOR of match objects, computed
                     one at a time as you iterate (lazy).
"""

import re
import reprlib

RE_WORD = re.compile(r'\w+')


# ---------------------------------------------------------------------------
# Version 1: __iter__ as a generator function (uses `yield`)
# ---------------------------------------------------------------------------
class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()


# ---------------------------------------------------------------------------
# Example 17-9: eager list comprehension vs. lazy generator expression
# ---------------------------------------------------------------------------
"""
This example isolates the SAME laziness idea, stripped of the Sentence
class, so you can see exactly when code inside a generator runs
relative to the loop consuming it.

    >>> def gen_AB():
    ...     print('start')
    ...     yield 'A'
    ...     print('continue')
    ...     yield 'B'
    ...     print('end.')

A LIST COMPREHENSION is eager: `[x*3 for x in gen_AB()]` immediately
drives gen_AB() to exhaustion to build the full list, right there on
that line — all three prints happen up front, before res1 is even
looped over.

    >>> res1 = [x*3 for x in gen_AB()]
    start
    continue
    end.
    >>> for i in res1:
    ...     print('-->', i)
    --> AAA
    --> BBB

A GENERATOR EXPRESSION `(x*3 for x in gen_AB())` is lazy: this line
does NOT run gen_AB() at all yet — it just builds a generator object
wrapping it.

    >>> res2 = (x*3 for x in gen_AB())
    >>> res2                                   # doctest: +ELLIPSIS
    <generator object <genexpr> at 0x...>

Only once we actually iterate res2 does gen_AB() start executing —
and it interleaves with the consuming loop: 'start' prints, THEN the
first '--> AAA' prints, THEN 'continue' prints, THEN '--> BBB'. Work
and consumption are interleaved, not front-loaded.

    >>> for i in res2:
    ...     print('-->', i)
    start
    --> AAA
    continue
    --> BBB
"""


# ---------------------------------------------------------------------------
# Version 2: __iter__ returning a generator expression directly
# ---------------------------------------------------------------------------
class Sentence:  # noqa: F811 (intentional redefinition — alternate impl)
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s)
    print(list(s))
    print(list(s))   # reusable: __iter__ builds a fresh genexpr each call