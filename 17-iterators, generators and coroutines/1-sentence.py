"""
iterables_vs_iterators.py

ITERABLE vs ITERATOR — the core distinction:

  Iterable
    - Any object Python can pass to iter() to get an iterator back.
    - Implements __iter__ (preferred), or falls back to __getitem__.
    - Holds NO iteration state of its own — you can call iter() on it
      many times and get a fresh, independent iterator each time.

  Iterator
    - The object that actually does the work of producing items one
      at a time, remembering where it left off (i.e. it HAS state).
    - Must implement:
        __next__(self)  -> returns the next item, or raises StopIteration
                            when exhausted
        __iter__(self)  -> returns self (so an iterator is itself
                            iterable — this is what lets `for x in it`
                            work directly on an iterator, not just on
                            the original collection)
    - Once exhausted, it stays exhausted — you can't rewind it.
      To iterate again you need a NEW iterator from the iterable.

Rule of thumb: an iterable's job is to CREATE iterators;
an iterator's job is to PRODUCE the values, one __next__() at a time.
"""
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:
    """ITERABLE (not an iterator itself).

    No __iter__ defined here on purpose — this relies on the classic
    fallback: Python's iter() sees no __iter__, finds __getitem__, and
    builds an iterator for us automatically, pulling self.words[0],
    self.words[1], ... until IndexError.
    """

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said')

    it1 = iter(s)
    it2 = iter(s)          # independent iterator, own index
    print(next(it1), next(it1))   # The time
    print(next(it2))              # The <- unaffected by it1's progress

    # exhausting one iterator doesn't affect the iterable itself
    print(list(s))         # full sentence again, from a NEW iterator