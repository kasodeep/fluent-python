"""
The iceberg is called the Python Data Model, and it is the API
that we use to make our own objects play well with the most idiomatic language features.

You can think of the data model as a description of Python as a framework. It formalizes
the interfaces of the building blocks of the language itself, such as sequences,
functions, iterators, coroutines, classes, context managers, and so on.
"""

import collections
from random import choice

# We use namedtuple to build classes of objects that
# are just bundles of attributes with no custom methods, like a database record.
Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit)
                       for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


beer_card = Card('7', 'diamonds')
print(beer_card)

print(len(FrenchDeck()))
print(FrenchDeck()[0])

print(choice(FrenchDeck()))

"""
Because our __getitem__ delegates to the [] operator of self._cards, our deck automatically supports slicing.
Just by implementing __getitem__, we get iteration, slicing, and other sequence-like behavior for free.
"""

print(FrenchDeck()[:3])

for card in FrenchDeck():
    print(card)

"""
Iteration is often implicit. If a collection has no __contains__ method, the in operator does a sequential scan.
"""

print(Card('Q', 'hearts') in FrenchDeck())

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(FrenchDeck(), key=spades_high):
    print(card)

"""
Special methods are meant to be called by the Python interpreter, not directly by you.
Python variable-sized collections written in C include a struct called PyVarObject,
which has an ob_size field holding the number of items in the collection.
"""

