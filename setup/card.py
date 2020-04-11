from colorama import Style, Fore

class Rank:
    ranks = {i: char for i, char in enumerate("23456789TJQKA", 2)}

    def __init__(self, rank):
        assert 2 <= rank <= 14
        self.rank = rank

    def __str__(self):
        return Rank.ranks[self.rank]

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __hash__(self):
        return hash(self.rank)


class Suit:
    suits = {i: char for i, char in enumerate("♠♥♦♣")}
    colours = {i: colour for i, colour in enumerate([Fore.WHITE, Fore.RED, Fore.BLUE, Fore.GREEN])}

    def __init__(self, suit):
        assert 0 <= suit <= 3
        self.suit = suit

    def __str__(self):
        return f"{self.colours[self.suit]}{Suit.suits[self.suit]}{Style.RESET_ALL}"

    def __eq__(self, other):
        return self.suit == other.suit

    def __hash__(self):
        return hash(self.suit)


class Card:
    def __init__(self, rank, suit):
        assert isinstance(rank, Rank)
        assert isinstance(suit, Suit)
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"[{self.rank}{self.suit}]"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.rank.__lt__(other.rank)

    def __le__(self, other):
        return self.rank.__le__(other.rank)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))
