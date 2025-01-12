import random
import utils
from itertools import combinations

# remove active players in list when folded, iterating over less players each time 
# -> more efficient way of implementing this.

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
        for agent in self.agents:
            agent.stack = buy_in
        
        self.game_state = {
            "community_cards": [], # current community cards (i.e. cards in the middle)
            "pot": 0,
            "current_bet": 0,
            "deck": self._create_deck(),
            "total_players": len(agents), # don't need to loop every time during is_game_over
            "buy_in": buy_in,
            "small_blind": buy_in // 10,
            "big_blind": buy_in // 5,
            "active_players": [agent for agent in self.agents], # should be a deep copy
            "folded_players": [],
            "started": False
        }
        # Initialize deck, pot, etc.

    def reset(self):
        """
        Reset or start a new round of poker. Shuffle deck, deal cards, reset pots, etc.
        """
        current_players = []
        for agent in self.agents:
            # if agent gambled stack, give them buy_in
            if agent.stack <= 0:
                agent.stack = self.game_state["buy_in"]
            agent.hand = []
            agent.folded = False
            current_players.append(agent)
        # ...
        self.game_state["community_cards"] = []
        self.game_state["pot"] = 0
        self.game_state["current_bet"] = 0
        self.game_state["active_players"] = current_players # is just saying self.agents a deep copy?
        self.game_state["folded_players"] = []
        self.game_state["total_players"] = len(self.agents)
        self.game_state["deck"] = self._create_deck()
            
    
    def play(self):
        """
        Play a complete poker game from start to finish.
        Deals hands, reveals community cards, and manages betting rounds.
        """
        # Reset the game state if started
        if self.game_state["started"]:
            self.reset()
        else:
            self.game_state["started"] = True
        
        # Deal initial hands to all players
        self._deal_hand()
        
        # Pre-flop betting round
        self.step()
        
        # Flop (reveal first 3 community cards)
        if not self.is_game_over():
            self.game_state["community_cards"].extend([self.game_state["deck"].pop() for _ in range(3)])
            self.step()
        
        # Turn (4th community card)
        if not self.is_game_over():
            self.game_state["community_cards"].append(self.deck.pop())
            self.step()
            
        # River (5th community card)
        if not self.is_game_over():
            self.game_state["community_cards"].append(self.deck.pop())
            self.step()
            
        # End the game and determine the winner
        self._end_game()
        
            
        return self.game_state

    def step(self):
        """
        Progress one betting round. Query each agent in turn for an action.
        """
        for agent in self.game_state["active_players"]:
            agent_state = {
                "hand": agent.hand,
                "community_cards": self.game_state["community_cards"],
                "pot": self.game_state["pot"],
                "current_bet": self.game_state["current_bet"],
                "buy_in": self.game_state["buy_in"],
                "small_blind": self.game_state["small_blind"],
                "big_blind": self.game_state["big_blind"]
            }
            action, amount = agent.decide_action(agent_state)
            self._apply_action(agent, action, amount)

    def _end_game(self):
        winner, hand_type = self._determine_winner()
        if hand_type == "Last Man Standing":
            print(f"{winner.name} won because they did not fold")
        else:
            print(f"{winner.name} won with a {hand_type}")

    def _deal_hand(self):
        # Deal 2 cards to each agent
        for _ in range(2):  # Deal 2 cards per agent
            for agent in self.game_state["active_players"]:
                agent.hand.append(self.deck.pop())


    def _apply_action(self, agent, action, amount):
        # Logic for applying agent's action to the environment
        if action == "fold":
            agent.folded = True
            self.game_state["total_players"] -= 1
            self.game_state["folded_players"].append(agent)
            self.game_state["active_players"].remove(agent)
        elif action == "call":
            if agent.stack >= self.game_state["current_bet"]:
                # Agent matches the current bet
                agent.stack -= self.game_state["current_bet"]
                agent.net_profit -= self.game_state["current_bet"]
                self.game_state["pot"] += self.game_state["current_bet"]
            else:
                # Agent goes all-in
                self.game_state["pot"] += agent.stack
                agent.net_profit -= agent.stack
                agent.stack = 0
        elif action == "raise":
            if amount <= agent.stack:
                # Agent raises the pot
                agent.stack -= amount
                agent.net_profit -= amount
                self.game_state["pot"] += amount
                self.game_state["current_bet"] = amount
            else:
                # Agent goes all-in
                self.game_state["current_bet"] = agent.stack
                agent.net_profit -= agent.stack
                self.game_state["pot"] += agent.stack
                agent.stack = 0

    def is_game_over(self):
        return self.game_state["total_players"] == 1 or len(self.game_state["community_cards"]) == 5

    def _create_deck(self):
        # Define the cards and suits
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['hearts', 'clubs', 'diamonds', 'spades']
        # Create and shuffle the deck
        deck = [(card, suit) for card in cards for suit in suits]
        random.shuffle(deck)
        return deck
    
    def _determine_winner(self):
        """
        Determines the winner of the current hand and awards them the pot.
        Returns the winning player and their hand type.
        """
        # If only one player hasn't folded, they win automatically
        
        if self.game_state["total_players"] == 1:
            winner = self.game_state["active_players"][0]
            winner.stack += self.game_state["pot"]
            winner.net_gain += self.game_state["pot"]
            return winner, "Last Man Standing"
            
        # Compare hands of all active players
        player_hands = []
        for player in self.game_state["active_players"]:
            # Combine community cards with player's hole cards
            all_cards = self.community_cards + player.hand
            # Find best 5-card hand from 7 cards
            best_hand = None
            best_hand_value = None
            
            # Try all possible 5-card combinations
            for five_cards in combinations(all_cards, 5):
                if not best_hand:
                    best_hand = five_cards
                    best_hand_value = utils.evaluate_hand(five_cards)
                else:
                    current_hand_value = utils.evaluate_hand(five_cards)
                    # Compare with current best hand
                    if utils.compare_hands(five_cards, best_hand) == 1:
                        best_hand = five_cards
                        best_hand_value = current_hand_value
            
            player_hands.append((player, best_hand, best_hand_value))
        
        # Find the winner(s)
        winners = [player_hands[0]]
        for hand in player_hands[1:]:
            comparison = utils.compare_hands(hand[1], winners[0][1])
            if comparison > 0:  # This hand is better
                winners = [hand]
            elif comparison == 0:  # This hand ties
                winners.append(hand)
        
        # Split pot among winners
        split_amount = self.game_state["pot"] // len(winners)
        for winner, _, hand_value in winners:
            winner.stack += split_amount
            winner.net_gain += split_amount
        self.game_state["pot"] = 0
        
        return winners[0][0], winners[0][2][0]  # Return first winner and their hand type
