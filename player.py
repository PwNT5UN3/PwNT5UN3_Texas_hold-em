"""Player model for the poker table."""

from __future__ import annotations

from cards import Card


class Player:
    def __init__(self, name: str, chips: int, is_human: bool):
        self.name = name
        self.chips = chips
        self.is_human = is_human
        self.hole_cards: list[Card] = list()
        self.current_bet: int = 0
        self.folded: bool = False

    def reset_for_hand(self) -> None:
        # TODO: Task 2 - reset the player's state for a new hand
        self.hole_cards = []
        self.current_bet = 0
        self.folded = False

    def receive(self, card: Card) -> None:
        # TODO: Task 3 - add the received cards to the player's hole cards
        self.hole_cards.append(card)

    def bet(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("cannot bet negative amounts!")
        self.chips -= amount
        self.current_bet += amount
        return amount

    def bot_action(self, communal_cards: list[Card],
                   table_bet: int) -> (str, int):
        return ("F", 0)

    @property
    def active(self) -> bool:
        # TODO: Task 5 - return True if the player is still active in the hand
        return not self.folded
