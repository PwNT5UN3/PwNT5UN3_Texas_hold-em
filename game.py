"""Console input/output helpers."""

from __future__ import annotations

from cards import Card, Deck
from player import Player
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
import pygame  # noqa: E402


class GameManager:

    colors = {
        "bg": (0, 81, 44, 1)
    }

    def __init__(self):
        self._settings = {"name": "Player", "buy-in": 10000,
                          "total_number_of_players": 5}
        self._players = []
        self._side_pots = []
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
        self._players = []
        buy_in = self._settings.get("buy-in", 10000)
        for p in range(self._settings.get("total_number_of_players", 5)):
            if p == 0:
                self._players.append(Player(self._settings.get("name",
                                                               "Player"),
                                            buy_in, True))
            else:
                self._players.append(Player(f"Bot {p}", buy_in, False))
        dealer_deck = Deck()
        dealer_cards = []
        for player in range(len(self._players)):
            dealer_cards.append(dealer_deck.draw()[0].rank.value)
        dealer_cards = sorted(list(enumerate(dealer_cards)),
                              key=lambda x: x[1], reverse=True)
        dealer_cards = list(filter(lambda x: x[1] == dealer_cards[0][1],
                                   dealer_cards))
        while len(dealer_cards) > 1:
            dealer_deck = Deck()
            for player in range(len(dealer_cards)):
                dealer_cards[player] = (dealer_cards[player][0],
                                        dealer_deck.draw()[0].rank.value)
            dealer_cards = sorted(list(dealer_cards),
                                  key=lambda x: x[1], reverse=True)
            dealer_cards = list(filter(lambda x: x[1] == dealer_cards[0][1],
                                       dealer_cards))
        self._dealer_position = (dealer_cards[0][0] + len(self._players) - 1)\
            % len(self._players)

    def betting_round(self, info: list[int]) -> bool:
        active, bidder, cc = info
        while cc < active:
            print(cc, active, bidder, self._dealer_position)
            if self._players[bidder].folded:
                cc += 1
            elif self._players[bidder].is_human:
                return False
            else:
                result = self._players[bidder].bot_action([], 0)
                match result:
                    case "C":
                        cc += 1
                    case "R":
                        cc = 1
                    case "F":
                        cc += 1
            bidder = (bidder + 1) % len(self._players)
        return True


    def play(self):
        self.setup()
        # states: "hand_setup", "preflop", "flop", "turn", "river", "showdown"
        card_font = pygame.font.Font('CourierPrime-Regular.ttf', size=100)
        suit_font = pygame.font.Font('Tinos-Italic.ttf', size=100)
        current_state = 0
        betting_pool = 0
        current_bet = 0
        current_big = 100
        hand_num = 4
        communal_cards = []
        bidder = -1
        active = len(self._players)
        player_turn = False
        while self.running:
            if current_state == 0:
                player_turn = False
                fist_betting_round = True
                print("new hand")
                betting_pool = 0
                current_bet = 0
                active = len(self._players)
                for p in self._players:
                    p.reset_for_hand()
                play_deck = Deck()
                communal_cards = []
                self._dealer_position = (self._dealer_position + 1)\
                    % len(self._players)
                hand_num = (hand_num + 1) % 5
                if hand_num == 0:
                    current_bet *= 2
                if active > 2:
                    bet = self._players[(self._dealer_position + 1)
                                        % len(self._players)]\
                                            .bet(current_big / 2)
                    betting_pool += bet
                    current_bet = bet
                    self._players[(self._dealer_position + 2)
                                  % len(self._players)].bet(current_big)
                    betting_pool += bet
                    current_bet = bet
                else:
                    bet = self._players[(self._dealer_position)
                                        % len(self._players)]\
                                            .bet(current_big / 2)
                    betting_pool += bet
                    current_bet = bet
                    self._players[(self._dealer_position + 1)
                                % len(self._players)].bet(current_big)
                    betting_pool += bet
                    current_bet = bet
                for _ in range(2):
                    for p in self._players:
                        p.receive(play_deck.draw(1)[0])
                    play_deck.draw(1)
                current_state += 1
            elif current_state == 1:
                if fist_betting_round:
                    current_bet = 0
                    if active > 2:
                        bidder = (self._dealer_position + 3) % len(self._players)
                    else:
                        bidder = self._dealer_position
                    cc = 0
                    fist_betting_round = False
                info = [active, bidder, cc]
                if not player_turn:
                    if self.betting_round(info):
                        current_state += 1
                    else:
                        player_turn = True
                active, bidder, cc = info
            elif current_state == 2:
                current_bet = 0
                if len(communal_cards) != 3:
                    play_deck.draw(3)
                    communal_cards.extend(play_deck.draw(3))
                    if active > 2:
                        bidder = (self._dealer_position + 3) % len(self._players)
                    else:
                        bidder = self._dealer_position
                    cc = 0
                info = [active, bidder, cc]
                if not player_turn:
                    if self.betting_round(info):
                        current_state += 1
                    else:
                        player_turn = True
                active, bidder, cc = info
            elif current_state == 3:
                current_bet = 0
                if len(communal_cards) != 4:
                    play_deck.draw(1)
                    communal_cards.extend(play_deck.draw(1))
                    if active > 2:
                        bidder = (self._dealer_position + 3) % len(self._players)
                    else:
                        bidder = self._dealer_position
                    cc = 0
                info = [active, bidder, cc]
                if not player_turn:
                    if self.betting_round(info):
                        current_state += 1
                    else:
                        player_turn = True
                active, bidder, cc = info
            elif current_state == 4:
                current_bet = 0
                if len(communal_cards) != 5:
                    play_deck.draw(1)
                    communal_cards.extend(play_deck.draw(1))
                    if active > 2:
                        bidder = (self._dealer_position + 3) % len(self._players)
                    else:
                        bidder = self._dealer_position
                    cc = 0
                info = [active, bidder, cc]
                if not player_turn:
                    if self.betting_round(info):
                        current_state = 1
                    else:
                        player_turn = True
                active, bidder, cc = info
            elif current_state == 5:
                current_state = 0
            if active == 1:
                for p in self._players:
                    if not p.folded:
                        p.chips += betting_pool
            print(bidder)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        current_state = (current_state + 1) % 6
                    elif event.key == pygame.K_c:
                        self._players[0].bet(0)
                        cc += 1
                        bidder += 1
                        print(bidder)
                        player_turn = False
            self.screen.fill(GameManager.colors["bg"])
            pygame.draw.rect(self.screen, (255, 255, 255),
                             pygame.Rect(1000, 600, 200, 280))
            pygame.draw.rect(self.screen, (255, 255, 255),
                             pygame.Rect(1300, 600, 200, 280))
            card_text = card_font.render(self._players[0].hole_cards[0]
                                         .rank.label, True, (0, 0, 0))
            self.screen.blit(card_text, (1020, 610))
            card_text = suit_font.render(self._players[0].hole_cards[0]
                                         .suit.symbol, True, (0, 0, 0)
                                         if self._players[0].hole_cards[0]
                                         .suit.value in [0, 3] 
                                         else (155, 17, 30))
            self.screen.blit(card_text, (1020, 670))
            card_text = card_font.render(self._players[1].hole_cards[0]
                                         .rank.label, True, (0, 0, 0))
            self.screen.blit(card_text, (1320, 610))
            card_text = suit_font.render(self._players[1].hole_cards[0]
                                         .suit.symbol, True, (0, 0, 0)
                                         if self._players[0].hole_cards[1]
                                         .suit.value in [0, 3]
                                         else (155, 17, 30))
            self.screen.blit(card_text, (1320, 670))
            for c in range(5):
                pygame.draw.rect(self.screen, (255, 255, 255)
                                 if len(communal_cards) > c else (75, 0, 130),
                                 pygame.Rect(200 + (250 * c), 200, 200, 280))
            for c in range(len(communal_cards)):
                card_text = card_font.render(communal_cards[c].rank.label,
                                             True, (0, 0, 0))
                self.screen.blit(card_text, (220 + (250 * c), 210))
                card_text = suit_font.render(communal_cards[c].suit.symbol,
                                             True, (0, 0, 0)
                                             if communal_cards[c]
                                             .suit.value in [0, 3]
                                             else (155, 17, 30))
                self.screen.blit(card_text, (220 + (250 * c), 270))
            pygame.display.flip()
            pygame.event.pump()

    def end_screen(self):
        end_font = pygame.font.Font(None, size=200)
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
            txt = end_font.render("Thanks for playing!", True, (0, 0, 0))
            self.screen.blit(txt, (150, 350))
            pygame.display.flip()
            pygame.event.pump()
