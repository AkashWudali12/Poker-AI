import random
import time
from itertools import combinations
from utils.utils import evaluate_hand, compare_hands
from .poker_table import PokerTable

class PokerEnv:
    """
    A simple environment to manage a multi-agent poker game.
    """

    def __init__(self, agents, buy_in):
        """
        :param agents: List of agent instances (e.g. [ConservativeAgent(...), AggressiveAgent(...), ...])
        :param buy_in: starting amount in dollars for each player
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
        
        # Deal initial hands to all players
        self._deal_hand()
        print("\n=== Starting New Poker Game ===")
        print("Initial hands dealt to players")
        time.sleep(1)

        self._blinds()
        print("\n=== Handling Blinds ===")
        print(f"Small blind pays {self.small_blind}")
        print(f"Big blind pays {self.big_blind}")
        time.sleep(1)
        
        # Pre-Flop betting round
        print("\n=== Pre-Flop Betting Round ===")
        self.round_stage = "Pre-Flop"
        self.step()
        
        # Flop (first 3 community cards)
        if not self.is_game_over():
            flop_cards = [self.deck.pop() for _ in range(3)]
            self.community_cards.extend(flop_cards)
            self.round_stage = "Flop"
            print(f"\n=== Flop ===\nCommunity Cards: {', '.join(map(str, self.community_cards))}")
            time.sleep(1)
            self.step()
        
        # Turn (4th community card)
        if not self.is_game_over():
            turn_card = self.deck.pop()
            self.community_cards.append(turn_card)
            self.round_stage = "Turn"
            print(f"\n=== Turn ===\nCommunity Cards: {', '.join(map(str, self.community_cards))}")
            time.sleep(1)
            self.step()
        
        # River (5th community card)
        if not self.is_game_over():
            river_card = self.deck.pop()
            self.community_cards.append(river_card)
            self.round_stage = "River"
            print(f"\n=== River ===\nCommunity Cards: {', '.join(map(str, self.community_cards))}")
            time.sleep(1)
            self.step()
        
        # Determine the winner and end the round
        self._end_game()
        
        return {
            "community_cards": self.community_cards,
            "pot": self.pot
        }

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
        for _ in range(2):
            curr = self.table.get_head()
            for _ in range(self.table.size()):
                curr.agent.hand.append(self.deck.pop())
                curr = curr.next

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

        # Big Blind
        big_blind_agent = self.table.get_big_blind()
        print(f"Agent {big_blind_agent.agent.name} posts big blind (${self.big_blind})")
        time.sleep(0.5)
        big_blind_agent.agent.stack -= self.big_blind
        big_blind_agent.agent.current_bet += self.big_blind
        big_blind_agent.agent.net_profit -= self.big_blind
        self.pot += self.big_blind
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
            time.sleep(0.5)

        elif action == "raise":
            # If the raise amount is within the agent's stack
            print(f"\nAgent {agent.name} raises by ${amount}")
            time.sleep(0.5)
            agent.stack -= amount
            agent.net_profit -= amount
            self.current_bet = (amount + agent.current_bet)
            agent.current_bet += amount
            self.pot += amount

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
        
        # Return the first winner and their hand type (e.g., "Flush", "Straight", etc.)
        return winners[0][0], winners[0][2][0]
