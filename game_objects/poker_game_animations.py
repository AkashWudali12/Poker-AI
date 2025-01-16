import pygame
import random
from enum import Enum
from constants import *
from .poker_table_animations import PokerTableAnimations

class GameState(Enum):
    WAITING_FOR_PLAYERS = 0
    DEALING_CARDS = 1
    PRE_FLOP = 2
    FLOP = 3
    TURN = 4
    RIVER = 5
    SHOWDOWN = 6
    GAME_OVER = 7

class PokerGameAnimations:
    def __init__(self, screen):
        self.screen = screen
        self.table = PokerTableAnimations()
        self.state = GameState.WAITING_FOR_PLAYERS
        self.animation_in_progress = False
        self.community_cards = []
        
    def add_player(self, player_id, seat_num):
        """Add a player visual representation at the specified seat"""
        self.table.add_player(player_id, seat_num)

    def deal_player_cards(self, player_hands):
        """
        Animate dealing cards to players
        player_hands: dict of player_id -> [(value, suit), (value, suit)]
        """
        self.state = GameState.DEALING_CARDS
        self.animation_in_progress = True
        self.table.deal_cards(player_hands)

    def deal_community_cards(self, cards, stage):
        """
        Animate dealing community cards
        cards: list of (value, suit) tuples
        stage: 'flop', 'turn', or 'river'
        """
        self.state = getattr(GameState, stage.upper())
        self.table.deal_community_cards(cards, stage)
        self.community_cards.extend(cards)

    def animate_player_bet(self, player_id, amount):
        """Animate a chip moving from player position to pot"""
        self.table.place_bet(player_id, amount)

    def reveal_player_cards(self, player_id):
        """Animate flipping a player's cards face up"""
        self.table.reveal_cards(player_id)

    def collect_pot(self, winner_id):
        """Animate moving chips from pot to winner"""
        self.table.move_pot_to_player(winner_id)

    def update(self, dt):
        """Update all ongoing animations"""
        self.table.update(dt)
        
        # Check if dealing animation is complete
        if self.state == GameState.DEALING_CARDS and not self.table.is_dealing:
            self.animation_in_progress = False
            self.state = GameState.PRE_FLOP

    def draw(self):
        """Draw the current state of the game"""
        self.table.draw(self.screen) 
    
    def update_pot(self, amount):
        """Update the pot amount in the animations"""
        self.table.update_pot(amount) 