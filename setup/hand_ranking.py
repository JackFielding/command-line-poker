from collections import defaultdict

from aenum import IntEnum


class HandRank(IntEnum):
    _init_ = 'value string'

    HIGH_CARD = 1, "High Card"
    ONE_PAIR = 2, "One Pair"
    TWO_PAIR = 3, "Two Pair"
    THREE_OF_A_KIND = 4, "Three of a Kind"
    STRAIGHT = 5, "Straight"
    FLUSH = 6, "Flush"
    FULL_HOUSE = 7, "Full House"
    FOUR_OF_A_KIND = 8, "Four of a Kind"
    STRAIGHT_FLUSH = 9, "Straight Flush"

    def __str__(self):
        return self.string


def rank_hand(cards):
    assert len(cards) <= 7

    flush_cards = []  # list of cards descending in rank st any 5 are a flush

    cards = sorted(cards, reverse=True)  # sort by rank
    cards_by_suit = defaultdict(list)
    cards_by_rank = defaultdict(list)

    for card in cards:
        cards_by_suit[card.suit.suit].append(card)
        cards_by_rank[card.rank.rank].append(card)
    suit, cards_of_commonest_suit = max(cards_by_suit.items(), key=lambda x: len(x[1]))
    if len(cards_of_commonest_suit) >= 5:
        flush_cards = cards_of_commonest_suit

    straight_ranges = set()
    if 14 in cards_by_rank and all(rank in cards_by_rank for rank in range(2, 6)):  # A2345 is a straight too
        straight_ranges |= {14} | set(range(2, 6))
    for start_rank in range(2, 10):
        rank_range = range(start_rank, start_rank + 5)
        if all(rank in cards_by_rank for rank in rank_range):
            straight_ranges |= set(rank_range)
    straight_cards = [card for card in cards if card.rank.rank in straight_ranges]

    straight_flush = sorted(set(straight_cards) & set(flush_cards), reverse=True)
    if len(straight_flush) >= 5:
        if straight_flush[0].rank.rank == 14 and straight_flush[1].rank.rank == 5:
            straight_flush = straight_flush[1:] + straight_flush[:1]
        else:
            straight_flush = straight_cards[:5]
        return HandRank.STRAIGHT_FLUSH, straight_flush

    trips = []
    pairs = []
    cards_by_rank = sorted(cards_by_rank.items(), key=lambda x: len(x[1]), reverse=True)
    for rank, cards_for_rank in cards_by_rank:
        if len(cards_for_rank) == 4:
            return HandRank.FOUR_OF_A_KIND, cards_for_rank + [x for x in cards if x not in cards_for_rank][:1]
        if len(cards_for_rank) == 3:
            trips.append(cards_for_rank)
        if len(cards_for_rank) == 2:
            pairs.append(cards_for_rank)

    if len(trips) >= 2 or (len(trips) == 1 and len(pairs) >= 1):
        return HandRank.FULL_HOUSE, trips[0] + sorted(trips[1:] + pairs, reverse=True)[0][:2]

    if flush_cards:
        return HandRank.FLUSH, flush_cards[:5]

    if straight_cards:
        # any duplicated ranks are removed
        straight_cards = sorted({c.rank.rank: c for c in straight_cards}.values(), reverse=True)
        # if the 2nd biggest is a 5 then either the biggest is a 6 and we have 23456 or it's an ace and we have A2345
        if straight_cards[0].rank.rank == 14 and straight_cards[1].rank.rank == 5:
            straight = straight_cards[1:] + straight_cards[:1]
        else:
            straight = straight_cards[:5]
        return HandRank.STRAIGHT, straight

    if trips:
        hand = trips[0]
        return HandRank.THREE_OF_A_KIND, hand + [x for x in cards if x not in hand][:2]

    if len(pairs) >= 2:
        hand = pairs[0] + pairs[1]
        return HandRank.TWO_PAIR, hand + [x for x in cards if x not in hand][:1]

    if len(pairs) == 1:
        hand = pairs[0]
        return HandRank.ONE_PAIR, hand + [x for x in cards if x not in hand][:3]

    return HandRank.HIGH_CARD, cards[:5]
