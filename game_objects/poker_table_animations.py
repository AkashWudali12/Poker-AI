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

    def add_player(self, player_id, seat_num, name, folded):
        """Add visual representation of a player"""
        if seat_num < len(SEAT_POSITIONS):
            self.players[player_id] = {
                'seat': seat_num,
                'position': SEAT_POSITIONS[seat_num],
                'chips': [],
                'cards': [],
                'current_bet': 0,
                'name': name,
                'folded': folded
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
    
    def fold_player(self, player_id):
        """Animate folding a player's cards"""
        for card_id, card in self.cards.items():
            if card_id.startswith(f"{player_id}_card_"):
                card.start_flip()
        self.players[player_id]['folded'] = True
        
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
        
       # Draw cards with folded status
        for card_id, card in self.cards.items():
            player_id = card_id.split('_card_')[0]
            if player_id in self.players and self.players[player_id]['folded']:
                # Create a dark overlay for folded players' cards
                card.draw(screen, alpha=128)  # 128 is half transparency
            else:
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
        
        # Draw player names and bet amounts
        font = pygame.font.Font(None, 28)
        for player_id, player_data in self.players.items():
            # Determine text color based on fold status
            text_color = WHITE
            if player_data['folded']:
                text_color = tuple(c // 2 for c in WHITE)  # Darker version of white
            
            # Draw player name
            name_text = font.render(player_data['name'], True, text_color)
            name_pos = (player_data['position'][0], player_data['position'][1] - 50)
            screen.blit(name_text, name_pos)
            
            # Draw bet amount if exists
            if 'current_bet' in player_data and player_data['current_bet'] > 0:
                bet_text = font.render(f"${player_data['current_bet']}", True, text_color)
                text_pos = (player_data['position'][0], player_data['position'][1] - 30)
                screen.blit(bet_text, text_pos)
    
    def update_pot(self, amount):
        """Update the pot amount displayed on screen"""
        self.pot = amount 

    def reset_board_state(self):
        """Reset all visual elements on the board"""
        self.pot = 0
        self.cards.clear()
        self.chips.clear()
        # Reset all player bets
        for player in self.players.values():
            player['current_bet'] = 0
            player['folded'] = False 