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
                            self.settings_menu()
                        elif menu_option == 2:
                            self.running = False
                        else:
                            raise Exception("Something unexpected happened!")
                        if not self.running:
                            return
            self.screen.fill(GameManager.colors["bg"])
            pygame.draw.rect(self.screen,
                             (153,122,141),
                             pygame.Rect(500, 275 + (menu_option * 150),
                                         195 + (menu_option % 2 * 185),
                                         10))
            btn = menu_font.render("Play", True, (255, 255, 255) if
                                   menu_option == 0 else (0, 0, 0))
            self.screen.blit(btn, (500, 200))
            btn = menu_font.render("Settings", True, (255, 255, 255) if
                                   menu_option == 1 else (0, 0, 0))
            self.screen.blit(btn, (500, 350))
            btn = menu_font.render("Quit", True, (255, 255, 255) if
                                   menu_option == 2 else (0, 0, 0))
            self.screen.blit(btn, (500, 500))
            pygame.display.flip()
            pygame.event.pump()

    def settings_menu(self):
        settings_option = 0
        buy_ins = [1000, 5000, 10000, 20000, 50000]
        buy_in_index = buy_ins.index(self._settings.get("buy-in", 10000))
        settings_font = pygame.font.Font(None, size=118)
        player_name = self._settings.get("name", "")
        bot_num = self._settings.get("total_number_of_players", 5) - 1
        line_lens = [250, 280, 645, 240, 285]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and settings_option != 0:
                        self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        settings_option = (settings_option + 4) % 5
                    elif event.key == pygame.K_DOWN:
                        settings_option = (settings_option + 1) % 5
                    elif event.key == pygame.K_SPACE:
                        if settings_option == 3:
                            self._settings = {"name": player_name,
                                              "buy-in": buy_ins[buy_in_index],
                                              "total_number_of_players":
                                              bot_num + 1}
                            return
                        if settings_option == 4:
                            return
                    elif settings_option == 0:
                        if event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            player_name = ''.join([i for i in
                                                  (player_name + event.unicode)
                                                  if i.isalnum()])
                    elif event.key == pygame.K_LEFT:
                        if settings_option == 1:
                            if buy_in_index != 0:
                                buy_in_index -= 1
                        elif settings_option == 2:
                            if bot_num != 1:
                                bot_num -= 1
                    elif event.key == pygame.K_RIGHT:
                        if settings_option == 1:
                            if buy_in_index != 4:
                                buy_in_index += 1
                        elif settings_option == 2:
                            if bot_num != 8:
                                bot_num += 1
            self.screen.fill(GameManager.colors["bg"])
            pygame.draw.rect(self.screen,
                             (153, 122, 141),
                             pygame.Rect(500,
                                         170 + (settings_option * 150),
                                         line_lens[settings_option],
                                         10))
            opt = settings_font.render(f"Name: {player_name}", True,
                                       (255, 255, 255) if
                                       settings_option == 0 else (0, 0, 0))
            self.screen.blit(opt, (500, 100))
            opt = settings_font.render(f"Buy-In: {buy_ins[buy_in_index]}",
                                       True,
                                       (255, 255, 255) if
                                       settings_option == 1 else (0, 0, 0))
            self.screen.blit(opt, (500, 250))
            opt = settings_font.render(f"Number of Bots: {bot_num}", True,
                                       (255, 255, 255) if
                                       settings_option == 2 else (0, 0, 0))
            self.screen.blit(opt, (500, 400))
            opt = settings_font.render("Apply", True,
                                       (255, 255, 255) if
                                       settings_option == 3 else (0, 0, 0))
            self.screen.blit(opt, (500, 550))
            opt = settings_font.render("Cancel", True,
                                       (255, 255, 255) if
                                       settings_option == 4 else (0, 0, 0))
            self.screen.blit(opt, (500, 700))
            pygame.display.flip()
            pygame.event.pump()

    def setup(self):
        buy_in = self._settings.get("buy-in", 10000)
        for p in range(self._settings.get("total_number_of_players", 5) - 1):
            if p == 0:
                self._players.append(Player(self._settings.get("name",
                                                               "Player"),
                                            buy_in, True))

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
