"""Console input/output helpers."""

from __future__ import annotations

from cards import Card
from player import Player
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
import pygame  # noqa: E402
from time import sleep


class GameManager:

    colors = {
        "bg": (0, 81, 44, 1)
    }

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
        self.running = True
        self.clock.tick(60)

    def menu(self):
        menu_option = 0
        menu_font = pygame.font.Font(None, size=128)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option + 2) % 3
                    elif event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % 3
                    elif event.key == pygame.K_SPACE:
                        if menu_option == 0:
                            self.play()
                        elif menu_option == 1:
                            self.settings()
                        elif menu_option == 2:
                            self.running = False
                        else:
                            raise Exception("Something unexpected happened!")
            self.screen.fill(GameManager.colors["bg"])
            play_btn = menu_font.render("PLAY", True, (255, 255, 255) if
                                        menu_option == 0 else (0, 0, 0))
            self.screen.blit(play_btn, (500, 200))
            play_btn = menu_font.render("SETTINGS", True, (255, 255, 255) if
                                        menu_option == 1 else (0, 0, 0))
            self.screen.blit(play_btn, (500, 350))
            play_btn = menu_font.render("QUIT", True, (255, 255, 255) if
                                        menu_option == 2 else (0, 0, 0))
            self.screen.blit(play_btn, (500, 500))
            pygame.draw.rect(self.screen,
                             (255, 255, 255),
                             pygame.Rect(500, 275 + (menu_option * 150),
                                         225 + (menu_option % 2 * 225),
                                         10))
            pygame.display.flip()
            pygame.event.pump()

    def settings(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            self.screen.fill(GameManager.colors["bg"])
            pygame.display.flip()
            pygame.event.pump()

    def setup(self):
        pass

    def play(self):
        self.setup()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            self.screen.fill(GameManager.colors["bg"])
            pygame.display.flip()
            pygame.event.pump()
