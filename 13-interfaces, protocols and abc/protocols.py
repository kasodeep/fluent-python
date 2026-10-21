"""
Dynamic protocol:
The informal protocols Python always had. Dynamic protocols are implicit,
defined by convention, and described in the documentation. Pythons most
important dynamic protocols are supported by the interpreter itself, and are
documented in the “Data Model” chapter of The Python Language Reference.

Static protocol:
A protocol as defined by PEP 544—Protocols: Structural subtyping (static duck
typing), since Python 3.8. A static protocol has an explicit definition: a
typing.Protocol subclass.

There are two key differences between them:
- An object may implement only part of a dynamic protocol and still be useful;
  but to fulfill a static protocol, the object must provide every method
  declared in the protocol class, even if your program doesnt need them all.

- Static protocols can be verified by static type checkers, but dynamic
  protocols cant.
"""

from collections import abc, namedtuple
from random import shuffle

Card = namedtuple("Card", ["rank", "suit"])

# In summary, given the importance of sequence-like data structures, Python manages
# to make iteration and the in operator work by invoking __getitem__ when __iter__
# and __contains__ are unavailable.


class Vowels:
    def __getitem__(self, key):
        return 'AEIOU'[key]


# MONKEY PATCHING

"""
When you follow established protocols, you improve your chances of leveraging
existing standard library and third-party code, thanks to duck typing.
"""


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


def set_card(deck, position, card):
    deck._cards[position] = card


FrenchDeck.__setitem__ = set_card

# GOOSE TYPING

"""
goose typing entails:
- Subclassing from ABCs to make it explict that you are implementing a
  previously defined interface.
- Runtime type checking using ABCs instead of concrete classes as the second
  argument for isinstance and issubclass.
"""


class FrenchDeck2(abc.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):
        self._cards[position] = value

    def __delitem__(self, position):
        del self._cards[position]

    def insert(self, position, value):
        self._cards.insert(position, value)