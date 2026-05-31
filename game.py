"""Console input/output helpers."""

from __future__ import annotations

from cards import Card
from player import Player
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
import pygame  # noqa: E402


class GameManager:
    def __init__(self):
        self._settings = {"name": "Player", "buy-in": 10000,
                          "total_number_of_players": 5}
        self._players = []
        self._side_pots = []
        self._communal_cards = []
        self._dealer_position = -1
        pygame.init()
        self.x_len = 1600
        self.y_len = 900
        self.screen = pygame.display.set_mode((self.x_len, self.y_len))
        self.clock = pygame.time.Clock()

    def menu(self):
        pass

    def settings(self):
        pass

    def setup(self):
        pass

    def play(self):
        pass
