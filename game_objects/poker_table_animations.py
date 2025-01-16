import pygame
import random
from constants import *
from .card import Card
from .chip import Chip

class PokerTableAnimations:
    def __init__(self):
        self.players = {}  # Dictionary to store player visual data
        self.cards = {}    # Dictionary to store card objects
        self.chips = {}    # Dictionary to store chip objects
        self.pot = 0
        self.deck_pos = DECK_POSITION
        self.is_dealing = False
        
        # Load card images
        self.card_back = pygame.image.load('assets/playing-cards-assets/png/back.png')
        self.chip_image = pygame.image.load('assets/playing-cards-assets/png/red_joker.png')
        
        # Load card fronts
        self.card_fronts = self._load_card_fronts()

    def _load_card_fronts(self):
        # Implement loading of card front images
        # Return dictionary of card images keyed by value+suit
        pass

    def add_player(self, player_id, seat_num):
        """Add visual representation of a player"""
        if seat_num < len(SEAT_POSITIONS):
            self.players[player_id] = {
                'seat': seat_num,
                'position': SEAT_POSITIONS[seat_num],
                'chips': [],
                'cards': [],
                'current_bet': 0
            }

    def deal_cards(self, player_hands):
        """Animate dealing cards to players"""
        self.is_dealing = True
        self.cards.clear()
        
        for player_id, cards in player_hands.items():
            if player_id in self.players:
                for i, (value, suit) in enumerate(cards):
                    card = Card(
                        value,
                        suit,
                        self.card_back,
                        pygame.image.load('assets/playing-cards-assets/png/2_of_hearts.png')
                    )
                    
                    offset = i * 20
                    target_pos = (
                        self.players[player_id]['position'][0] + offset,
                        self.players[player_id]['position'][1]
                    )
                    
                    card.start_deal(self.deck_pos, target_pos)
                    self.cards[f"{player_id}_card_{i}"] = card

    def deal_community_cards(self, cards, stage):
        """
        Animate dealing community cards
        Different positioning based on stage (flop, turn, river)
        """
        if stage == "flop":
            print("Dealing flop cards")
            # Position flop cards more to the right
            start_x = SCREEN_WIDTH // 2  # Start from center
            for i, (value, suit) in enumerate(cards):
                card = Card(
                    value,
                    suit,
                    self.card_back,
                    pygame.image.load('assets/playing-cards-assets/png/2_of_hearts.png')
                )
                # Space cards with 60px gap
                target_pos = (start_x + i * 60, SCREEN_HEIGHT // 2)
                card.start_deal(self.deck_pos, target_pos)
                self.cards[f"community_card_{len(self.cards)}"] = card
        
        elif stage == "turn":
            print("Dealing turn card")
            # Position turn card to the left of the flop
            card = Card(
                cards[0][0],  # value
                cards[0][1],  # suit
                self.card_back,
                pygame.image.load('assets/playing-cards-assets/png/2_of_hearts.png')
            )
            # Place turn card 60px to the left of the first flop card
            target_pos = ((SCREEN_WIDTH // 2) - 60, SCREEN_HEIGHT // 2)
            card.start_deal(self.deck_pos, target_pos)
            self.cards[f"community_card_{len(self.cards)}"] = card
            
        elif stage == "river":
            print("Dealing river card")
            # Position river card to the left of the turn
            card = Card(
                cards[0][0],  # value
                cards[0][1],  # suit
                self.card_back,
                pygame.image.load('assets/playing-cards-assets/png/2_of_hearts.png')
            )
            # Place river card 60px to the left of the turn card
            target_pos = ((SCREEN_WIDTH // 2) - 120, SCREEN_HEIGHT // 2)
            card.start_deal(self.deck_pos, target_pos)
            self.cards[f"community_card_{len(self.cards)}"] = card

    def place_bet(self, player_id, amount, current_bet):
        """Animate moving a chip to the pot"""
        if player_id in self.players:
            chip = Chip(amount, self.chip_image, self.players[player_id]['position'])
            chip.move_to(POT_POSITION)
            self.chips[f"{player_id}_chip_{len(self.chips)}"] = chip
            self.pot += amount
            self.players[player_id]['current_bet'] = current_bet

    def move_pot_to_player(self, winner_id):
        """Animate moving pot chips to winner"""
        if winner_id in self.players:
            for chip in self.chips.values():
                chip.move_to(self.players[winner_id]['position'])

    def reveal_cards(self, player_id):
        """Animate flipping player's cards"""
        for card_id, card in self.cards.items():
            if card_id.startswith(f"{player_id}_card_"):
                card.start_flip()

    def update(self, dt):
        """Update all animations"""
        any_card_moving = False
        for card in self.cards.values():
            card.update(dt)
            if card.is_moving:
                any_card_moving = True
        
        self.is_dealing = any_card_moving
        
        for chip in self.chips.values():
            chip.update(dt)

    def draw(self, screen, started: bool):
        """Draw all visual elements on the provided screen"""
        # Draw chips
        for chip in self.chips.values():
            chip.draw(screen)
        
        # Draw cards
        for card in self.cards.values():
            card.draw(screen)
        
        # Draw pot amount
        if started:
            font = pygame.font.Font(None, 36)
            pot_text = font.render(f"Pot: ${self.pot}", True, WHITE)
            screen.blit(pot_text, (POT_POSITION[0] - pot_text.get_width()//2, POT_POSITION[1] - 30)) 
        else:
            font = pygame.font.Font(None, 36)
            pot_text = font.render(f"Press Space to Start", True, WHITE)
            screen.blit(pot_text, (POT_POSITION[0] - pot_text.get_width()//2, POT_POSITION[1] - 30)) 
        
        # Draw player bet amounts
        font = pygame.font.Font(None, 28)  # Smaller font for bet amounts
        for player_data in self.players.values():
            if 'current_bet' in player_data and player_data['current_bet'] > 0:
                bet_text = font.render(f"${player_data['current_bet']}", True, WHITE)
                # Position the text slightly above the player's position
                text_pos = (player_data['position'][0], player_data['position'][1] - 30)
                screen.blit(bet_text, text_pos)
    
    def update_pot(self, amount):
        """Update the pot amount displayed on screen"""
        self.pot = amount 