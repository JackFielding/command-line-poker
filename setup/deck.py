import itertools
import random
import sys

from setup.card import Card, Suit, Rank


class Deck:
    def __init__(self):
        self.cards = [Card(Rank(r), Suit(s)) for r, s in itertools.product(range(2, 15), range(4))]
        self.shuffle()
        self._dealt = 0  # would be better if each card picked randomly on the fly, pre-hand shuffle works for now

    def shuffle(self):
        random.shuffle(self.cards)

    def reset(self):
        self._dealt = 0
        self.shuffle()

    def deal(self, n):
        self._dealt += n
        return self.cards[self._dealt - n: self._dealt]
