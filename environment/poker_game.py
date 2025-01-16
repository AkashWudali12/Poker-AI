import random
import time
from itertools import combinations
from utils.utils import evaluate_hand, compare_hands
from .poker_table import PokerTable
from game_objects.poker_game_animations import PokerGameAnimations
import pygame
from components.button import Button

class PokerEnv:
    """
    A simple environment to manage a multi-agent poker game.
    """

    def __init__(self, agents, buy_in, screen):
        """
        :param agents: List of agent instances (e.g. [ConservativeAgent(...), AggressiveAgent(...), ...])
        :param buy_in: starting amount in dollars for each player
        :param screen: pygame screen object
        """

        self.agents = agents
        self.buy_in = buy_in

        # Initialize each agent's stack
        for agent in self.agents:
            agent.stack = buy_in
        
        # Game state variables
        self.community_cards = []         # Current community cards
        self.pot = 0
        self.current_bet = 0
        self.deck = self._create_deck()
        
        self.small_blind = buy_in // 10
        self.big_blind = buy_in // 5
                
        self.started = False

        self.round_stage = "Not Started"

        self.table = PokerTable(self.agents)
        self.total_players = self.table.size()

        self.screen = screen
        self._init_frontend()

    def reset(self):
        """
        Reset or start a new round of poker. Shuffle deck, deal cards, reset pots, etc.
        """

        # reset agent specific state
        curr = self.table.get_head()
        for _ in range(self.table.size()):
            # If an agent busted (stack <= 0), reset them to buy_in
            if curr.agent.stack <= 0:
                self.buy_in
            curr.agent.hand = []
            curr.agent.folded = False
            curr.agent.current_bet = 0
            curr.agent.previous_action = None
            curr = curr.next
        
        # Reset round-specific state
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.total_players = self.table.size()
        
        # Create and shuffle a new deck
        self.deck = self._create_deck()

        self.round_stage = "Not Started"

        # Reset pot and update display
        self.pot = 0
        self.animations.update_pot(self.pot)  # Update pot display to zero

    def play(self):
        """
        Play a complete poker game from start to finish.
        Deals hands, reveals community cards, and manages betting rounds.
        """
        # If we've already started a game, reset for a new round
        if self.started:
            self.reset()
        else:
            self.started = True
        
        while self.running:
            dt = self.clock.tick(60)
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    self.running = False
                    self.next_scene = "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Start a new round when space is pressed
                        self._deal_hand()  
                        print("\n=== Starting New Poker Game ===")
                        print("Initial hands dealt to players")
                        time.sleep(1)

                        self._blinds()
                        print("\n=== Handling Blinds ===")
                        print(f"Small blind pays {self.small_blind}")
                        print(f"Big blind pays {self.big_blind}")
                        time.sleep(1)
        
            # Update animations
            self.animations.update(dt)

            # Update button states
            for btn in self.buttons:
                btn.update(event_list)

            # Draw everything
            self.screen.blit(self.background, (0, 0))
            
            # Draw game animations
            self.animations.draw()
            
            # Draw buttons
            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()

        return self.next_scene
        
        # # Pre-Flop betting round
        # print("\n=== Pre-Flop Betting Round ===")
        # self.round_stage = "Pre-Flop"
        # self.step()
        
        # # Flop (first 3 community cards)
        # if not self.is_game_over():
        #     flop_cards = [self.deck.pop() for _ in range(3)]
        #     self.community_cards.extend(flop_cards)
        #     self.round_stage = "Flop"
        #     print(f"\n=== Flop ===\nCommunity Cards: {', '.join(map(str, self.community_cards))}")
        #     time.sleep(1)
        #     self.step()
        
        # # Turn (4th community card)
        # if not self.is_game_over():
        #     turn_card = self.deck.pop()
        #     self.community_cards.append(turn_card)
        #     self.round_stage = "Turn"
        #     print(f"\n=== Turn ===\nCommunity Cards: {', '.join(map(str, self.community_cards))}")
        #     time.sleep(1)
        #     self.step()
        
        # # River (5th community card)
        # if not self.is_game_over():
        #     river_card = self.deck.pop()
        #     self.community_cards.append(river_card)
        #     self.round_stage = "River"
        #     print(f"\n=== River ===\nCommunity Cards: {', '.join(map(str, self.community_cards))}")
        #     time.sleep(1)
        #     self.step()
        
        # # Determine the winner and end the round
        # self._end_game()

    def step(self):
        """
        Progress one betting round. Query each agent in turn for an action,
        starting from self.action_index.
        """

        curr_action_agent = self.table.get_action()
        settled_count, total_count = 0, 0 # number of players that settled on a bet, total players that went
        previous_action = None
        while True:
            if not curr_action_agent.agent.folded:
                print("Current Agent:", curr_action_agent.agent.name)
                print()
                print("Current Bet On Table:", self.current_bet)
                print()
                if self.total_players == 1:
                    break

                agent_state = {
                    "game_stage": self.round_stage,
                    "previous_action": previous_action,
                    "hand": curr_action_agent.agent.hand,
                    "community_cards": self.community_cards,
                    "pot": self.pot,
                    "current_bet": self.current_bet,
                    "buy_in": self.buy_in,
                    "small_blind": self.small_blind,
                    "big_blind": self.big_blind,
                }
                action, amount = curr_action_agent.agent.decide_action(agent_state)
                self._apply_action(curr_action_agent.agent, action, amount)

                previous_action = (action, amount)

                if action == "check" or action == "call":
                    settled_count += 1            
                total_count += 1

                if total_count == self.total_players:
                    if settled_count == self.total_players:
                        print("\n=== All players have settled on a bet. ===")
                        self.current_bet = 0
                        for agent in self.agents:
                            agent.current_bet = 0
                        break
                    else:
                        settled_count = 0
                        total_count = 0

            curr_action_agent = curr_action_agent.next
    
    def rotate(self):
        self.table.move_positions()
    
    def _on_quit(self):
        self.running = False
        self.next_scene = "main_menu"
            
    def _end_game(self):
        winner, hand_type = self._determine_winner()
        if hand_type == "Last Man Standing":
            print(f"{winner.name} won because they did not fold.")
        else:
            print(f"{winner.name} won with a {hand_type}")

    def _deal_hand(self):
        """
        Deal 2 cards to each active player.
        """
        player_hands = {agent.name: [] for agent in self.agents}

        for _ in range(2):
            curr = self.table.get_head()
            for _ in range(self.table.size()):
                curr_hand = self.deck.pop()
                curr.agent.hand.append(curr_hand)
                player_hands[curr.agent.name].append(curr_hand)
                curr = curr.next
        
        self.animations.deal_player_cards(player_hands)

    def _blinds(self):
        """
        Handle the small and big blinds.
        """
        # Small Blind
        small_blind_agent = self.table.get_small_blind()
        print(f"\nAgent {small_blind_agent.agent.name} posts small blind (${self.small_blind})")
        time.sleep(0.5)
        small_blind_agent.agent.stack -= self.small_blind
        small_blind_agent.agent.current_bet += self.small_blind
        small_blind_agent.agent.net_profit -= self.small_blind
        self.pot += self.small_blind
        self.animations.animate_player_bet(small_blind_agent.agent.name, self.small_blind)  # Animate chip movement

        # Big Blind
        big_blind_agent = self.table.get_big_blind()
        print(f"Agent {big_blind_agent.agent.name} posts big blind (${self.big_blind})")
        time.sleep(0.5)
        big_blind_agent.agent.stack -= self.big_blind
        big_blind_agent.agent.current_bet += self.big_blind
        big_blind_agent.agent.net_profit -= self.big_blind
        self.pot += self.big_blind
        self.animations.animate_player_bet(big_blind_agent.agent.name, self.big_blind)  # Animate chip movement
        self.current_bet = self.big_blind

    def _apply_action(self, agent, action, amount):
        """
        Apply the agent's action (fold, call, raise, etc.) to the game state.
        """
        if action == "fold":
            print(f"\nAgent {agent.name} folds")
            time.sleep(0.5)
            agent.folded = True
            self.total_players -= 1

        elif action == "call":
            print(f"\nAgent {agent.name} calls ${amount}")
            agent.stack -= amount
            agent.net_profit -= amount
            agent.current_bet += amount
            self.pot += amount
            self.animations.animate_player_bet(agent.name, amount)  # Animate chip movement
            time.sleep(0.5)

        elif action == "raise":
            print(f"\nAgent {agent.name} raises by ${amount}")
            time.sleep(0.5)
            agent.stack -= amount
            agent.net_profit -= amount
            self.current_bet = (amount + agent.current_bet)
            agent.current_bet += amount
            self.pot += amount
            self.animations.animate_player_bet(agent.name, amount)  # Animate chip movement

    def is_game_over(self):
        """
        The game is over if only one player remains or if we've revealed all 5 community cards.
        """
        return self.total_players == 1 or len(self.community_cards) == 5

    def _create_deck(self):
        """
        Create a standard 52-card deck and shuffle it.
        """
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['hearts', 'clubs', 'diamonds', 'spades']
        deck = [(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck
    
    def _determine_winner(self):
        """
        Determine the winner among the active players. Returns (winner, hand_type).
        """
        # If only one player hasn't folded, that player wins automatically
        if self.total_players == 1:
            winner = [agent for agent in self.agents if not agent.folded][0]
            winner.stack += self.pot
            winner.net_profit += self.pot
            self.pot = 0
            self.animations.update_pot(self.pot)  # Update pot display to zero
            return winner, "Last Man Standing"
        
        # Otherwise, compare the best 5-card hands for each active player
        player_hands = []
        player = self.table.get_head()
        for _ in range(self.table.size()):
            if not player.agent.folded:
                # Combine community cards with player's hole cards
                all_cards = self.community_cards + player.agent.hand
                best_hand = None
                best_hand_value = None
                
                # Evaluate all possible 5-card combinations
                for five_cards in combinations(all_cards, 5):
                    if best_hand is None:
                        best_hand = five_cards
                        best_hand_value = evaluate_hand(five_cards)
                    else:
                        current_value = evaluate_hand(five_cards)
                        if compare_hands(five_cards, best_hand) == 1:
                            best_hand = five_cards
                            best_hand_value = current_value
                
                player_hands.append((player.agent, best_hand, best_hand_value))
            player = player.next
        
        # Find the winner(s) – compare best hands
        winners = [player_hands[0]]
        for hand_info in player_hands[1:]:
            comparison = compare_hands(hand_info[1], winners[0][1])
            if comparison > 0:
                winners = [hand_info]
            elif comparison == 0:
                winners.append(hand_info)
        
        # Split pot among all tying winners
        split_amount = self.pot // len(winners)
        for winner_data in winners:
            winner_player, _, _ = winner_data
            winner_player.stack += split_amount
            winner_player.net_profit += split_amount
        
        self.pot = 0
        self.animations.update_pot(self.pot)  # Update pot display to zero
        
        # Return the first winner and their hand type (e.g., "Flush", "Straight", etc.)
        return winners[0][0], winners[0][2][0]

    def _init_frontend(self):
        """
        Initialize the animations for the game.
        """

        self.clock = pygame.time.Clock()
        self.running = True
        self.next_scene = "game"

        self.background = pygame.image.load('assets/poker_table.jpg')
        self.background = pygame.transform.scale(self.background, (1040, 720))
        self.animations = PokerGameAnimations(self.screen)
        for i, agent in enumerate(self.agents):
            self.animations.add_player(agent.name, i)

        button_styles = {
            "Check": {
                "normal": (33, 150, 243),   # #2196f3
                "hover": (30, 135, 220),    # #1e87dc
                "pressed": (25, 118, 210),
            },
            "Call": {
                "normal": (76, 175, 80),    # #4caf50
                "hover": (69, 160, 73),     # #45a049
                "pressed": (56, 142, 60),
            },
            "Raise": {
                "normal": (255, 152, 0),    # #ff9800
                "hover": (245, 124, 0),     # #f57c00
                "pressed": (230, 81, 0),
            },
            "Fold": {
                "normal": (244, 67, 54),    # #f44336
                "hover": (229, 57, 53),     # #e53935
                "pressed": (211, 47, 47),
            },
            "Quit": {
                "normal": (158, 158, 158),  # #9e9e9e
                "hover": (117, 117, 117),   # #757575
                "pressed": (97, 97, 97),
            }
        }

        # Button dimensions and positioning
        button_width = 120
        button_height = 50
        spacing = 20
        
        # Bottom row for action buttons
        action_buttons = [
            ("Check", print("Check")),
            ("Call", print("Call")),
            ("Raise", print("Raise")),
            ("Fold", print("Fold")),
            ("Quit", self._on_quit),
        ]

        self.buttons = []

        # Create action buttons (bottom row)
        total_width_action = (button_width * len(action_buttons)) + (spacing * (len(action_buttons) - 1))
        start_x_action = (1040 - total_width_action) // 2
        base_y_action = 720 - button_height - 50  # 50px from bottom
        
        current_x = start_x_action
        for label, callback in action_buttons:
            style = button_styles[label]
            btn = Button(
                text=label,
                x=current_x,
                y=base_y_action,
                width=button_width,
                height=button_height,
                normal_color=style["normal"],
                hover_color=style["hover"],
                pressed_color=style["pressed"],
                text_color=(255, 255, 255),
                callback=callback,
                border_radius=4,
                font=pygame.font.SysFont(None, 32)
            )
            self.buttons.append(btn)
            current_x += button_width + spacing
