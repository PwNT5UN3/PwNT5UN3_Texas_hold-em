"""Five-card hand evaluator used to rank Texas Hold'em showdowns."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations

from cards import Card, Rank, Suit, Deck

#debug
from random import random


class HandCategory(IntEnum):
    HIGH = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


@dataclass(frozen=True, order=True)
class HandRank:
    category: HandCategory
    ranks: list[int]

    @property
    def label(self) -> str:
        h_rank = Rank(sorted(self.ranks, reverse=True)[0])
        if self.category == HandCategory.HIGH:
            return (h_rank.name.capitalize() + " " +
                    self.category.name.capitalize())
        else:
            return self.category.name.capitalize().replace("_", ' ')


class HandEvaluator:
    def best_rank(self, cards: list[Card]) -> HandRank:
        if len(cards) != 7:
            raise ValueError("Need 7 cards (5 commons + 2 hole) for showdown!")
        return self._rank_seven(cards)

    @staticmethod
    def _check_flush(cards: list[Suit]) -> int:
        occ = {}
        occ[Suit.CLUBS] = len([i for i in cards if i == Suit.CLUBS])
        occ[Suit.DIAMONDS] = len([i for i in cards if i == Suit.DIAMONDS])
        occ[Suit.HEARTS] = len([i for i in cards if i == Suit.HEARTS])
        occ[Suit.SPADES] = len([i for i in cards if i == Suit.SPADES])
        return sorted(list(map(lambda x: x[0].value if x[1] >= 5 else -1,
                               occ.items())), reverse=True)[0]

    def _rank_seven(self, cards: list[Card]) -> HandRank:
        ranks = list(map(lambda x: x.rank.value, cards))
        suits = list(map(lambda x: x.suit, cards))
        is_flush = self._check_flush(suits) + 1
        straight_ranks = self._straight_high(cards)
        straight_flush_ranks = None
        if is_flush:
            straight_flush_ranks =\
                self._check_straight_flush(cards, Suit(is_flush - 1))
        rank_counts = self._get_grouped(cards)
        best_group = self._get_best_group_hand(rank_counts)
        print(list(map(lambda x: str(x), cards)))
        if straight_flush_ranks and Rank(straight_flush_ranks[0]) == Rank.ACE:
            return HandRank(HandCategory.ROYAL_FLUSH, straight_flush_ranks)
        elif straight_flush_ranks:
            return HandRank(HandCategory.STRAIGHT_FLUSH, straight_flush_ranks)
        elif best_group == HandCategory.FOUR_OF_A_KIND:
            return HandRank(HandCategory.FOUR_OF_A_KIND,
                            self._get_best_group_cards(cards, rank_counts, 4,
                                                       False, False))
        elif best_group == HandCategory.FULL_HOUSE:
            return HandRank(HandCategory.FULL_HOUSE,
                            self._get_best_group_cards(cards, rank_counts, 0,
                                                       True, False))
        elif is_flush:
            return HandRank(HandCategory.FLUSH,
                            self._get_best_flush_cards(cards, is_flush - 1))
        elif straight_ranks:
            return HandRank(HandCategory.STRAIGHT, straight_ranks)
        elif best_group == HandCategory.THREE_OF_A_KIND:
            return HandRank(HandCategory.THREE_OF_A_KIND,
                            self._get_best_group_cards(cards, rank_counts, 3,
                                                       False, False))
        elif best_group == HandCategory.TWO_PAIR:
            return HandRank(HandCategory.TWO_PAIR,
                            self._get_best_group_cards(cards, rank_counts, 0,
                                                       False, True))
        elif best_group == HandCategory.PAIR:
            return HandRank(HandCategory.PAIR,
                            self._get_best_group_cards(cards, rank_counts, 2,
                                                       False, False))
        else:
            return HandRank(HandCategory.HIGH,
                            sorted(list(map(lambda x: x.rank.value, cards)),
                                   reverse=True)[:5])
        print(rank_counts)
        return HandRank(HandCategory.HIGH, [2])

    def _check_straight_flush(self, cards: list[Card],
                              flush: Suit) -> [int] | None:
        cards = [i for i in cards if i.suit == flush]
        return self._straight_high(cards)

    def _get_best_group_hand(self,
                             groups: dict[Rank, int]) -> HandCategory | None:
        groups_int = sorted(list(i for i in groups.values() if i != 1),
                            reverse=True)
        print(groups_int)
        if 4 in groups_int:
            return HandCategory.FOUR_OF_A_KIND
        elif (3 in groups_int and 2 in groups_int) or groups_int.count(3) >= 2:
            return HandCategory.FULL_HOUSE
        elif 3 in groups_int:
            return HandCategory.THREE_OF_A_KIND
        elif groups_int.count(2) >= 2:
            return HandCategory.TWO_PAIR
        elif 2 in groups_int:
            return HandCategory.PAIR
        else:
            return None

    def _straight_high(self, cards: list[Card]) -> [int] | None:
        ranks = sorted(list(map(lambda x: x.rank.value, cards)), reverse=True)
        discards = []
        while len(ranks) >= 5:
            if (ranks[0] == ranks[1] + 1 and ranks[1] == ranks[2] + 1 and
               ranks[2] == ranks[3] + 1 and ranks[3] == ranks[4] + 1):
                return ranks[:5]
            elif (ranks[0] == 5 and ranks[1] == 4 and
                  ranks[2] == 3 and ranks[3] == 2 and 14 in discards):
                return [5, 4, 3, 2, 1]
            else:
                discards.append(ranks.pop(0))
        if (ranks[0] == 5 and ranks[1] == 4 and
                ranks[2] == 3 and ranks[3] == 2 and 14 in discards):
            return [5, 4, 3, 2, 1]
        return None

    def _get_grouped(self, cards: list[Card]) -> {Rank, int}:
        ranks = list(map(lambda x: x.rank, cards))
        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        return rank_counts

    def _get_best_group_cards(self, cards: list[Card],
                              rank_counts: {Rank, int},
                              size: int, fh: bool, tp: bool) -> [int]:
        ranks = sorted(list(map(lambda x: x.rank.value, cards)), reverse=True)
        rank_counts_list = sorted(rank_counts.items(), key=lambda x: x[1],
                                      reverse=True)
        order = []
        if fh and tp:
            raise Exception("something unexpected happened")
        elif fh:
            if rank_counts_list[1][1] == 3:
                if rank_counts_list[0][0].value > rank_counts_list[1][0].value:
                    return [rank_counts_list[0][0].value,
                            rank_counts_list[0][0].value,
                            rank_counts_list[0][0].value,
                            rank_counts_list[1][0].value,
                            rank_counts_list[1][0].value]
                else:
                    return [rank_counts_list[1][0].value,
                            rank_counts_list[1][0].value,
                            rank_counts_list[1][0].value,
                            rank_counts_list[0][0].value,
                            rank_counts_list[0][0].value]
            else:
                if [i[1] for i in rank_counts_list].count(2) == 2:
                    print("EXPECTED FOR 322")
                    if rank_counts_list[1][0].value > rank_counts_list[2][0]:
                        return [rank_counts_list[0][0].value,
                                rank_counts_list[0][0].value,
                                rank_counts_list[0][0].value,
                                rank_counts_list[1][0].value,
                                rank_counts_list[1][0].value]
                    else:
                        return [rank_counts_list[0][0].value,
                                rank_counts_list[0][0].value,
                                rank_counts_list[0][0].value,
                                rank_counts_list[2][0].value,
                                rank_counts_list[2][0].value]
                else:
                    return [rank_counts_list[0][0].value,
                            rank_counts_list[0][0].value,
                            rank_counts_list[0][0].value,
                            rank_counts_list[1][0].value,
                            rank_counts_list[1][0].value]
        elif tp:
            if [i[1] for i in rank_counts_list].count(2) == 3:
                if (rank_counts_list[0][0].value < rank_counts_list[1][0]
                        and rank_counts_list[0][0].value <
                        rank_counts_list[2][0]):
                    order.extend([rank_counts_list[1][0].value,
                                  rank_counts_list[1][0].value,
                                  rank_counts_list[2][0].value,
                                  rank_counts_list[2][0].value])
                elif (rank_counts_list[1][0].value < rank_counts_list[0][0]
                        and rank_counts_list[1][0].value <
                        rank_counts_list[2][0]):
                    order.extend([rank_counts_list[0][0].value,
                                  rank_counts_list[0][0].value,
                                  rank_counts_list[2][0].value,
                                  rank_counts_list[2][0].value])
                else:
                    order.extend([rank_counts_list[0][0].value,
                                  rank_counts_list[0][0].value,
                                  rank_counts_list[1][0].value,
                                  rank_counts_list[1][0].value])
                order.sort(reverse=True)
                order.append([i for i in ranks if i not in order][0])
            else:
                order.extend([rank_counts_list[0][0].value,
                              rank_counts_list[0][0].value,
                              rank_counts_list[1][0].value,
                              rank_counts_list[1][0].value])
                order.sort(reverse=True)
                order.append([i for i in ranks if i not in order][0])
        else:
            order.extend([i for i in ranks if i == rank_counts_list[0][0]])
            print("nonspecial group", size, order)
            order.extend([i for i in ranks if i not in order][:5-size])
        return order

    def _get_best_flush_cards(self, cards: list[Card], suit: Suit) -> [int]:
        ranks = sorted(list(map(lambda x: x.rank.value,
                                [i for i in cards if i.suit == suit])),
                       reverse=True)
        return ranks[:5]
