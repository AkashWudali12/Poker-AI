import pygame
import math
from constants import CARD_WIDTH, CARD_HEIGHT, DEAL_SPEED, CARD_FLIP_SPEED

class Card:
    def __init__(self, value, suit, back_image, front_image):
        self.value = value
        self.suit = suit
        self.back_image = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))
        self.front_image = pygame.transform.scale(front_image, (CARD_WIDTH, CARD_HEIGHT))
        self.current_image = self.back_image
        self.rect = self.current_image.get_rect()
        self.start_pos = (0, 0)
        self.target_pos = (0, 0)
        self.current_pos = (0, 0)
        self.is_moving = False
        self.is_flipping = False
        self.flip_progress = 0
        self.deal_progress = 0
        self.revealed = False

    def start_deal(self, start_pos, target_pos):
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.current_pos = start_pos
        self.is_moving = True
        self.deal_progress = 0

    def start_flip(self):
        if not self.revealed:
            self.is_flipping = True
            self.flip_progress = 0

    def update(self, dt):
        if self.is_moving:
            self.deal_progress = min(1.0, self.deal_progress + (dt / DEAL_SPEED))
            
            # Use easing function for smooth movement
            progress = self._ease_out_quad(self.deal_progress)
            
            self.current_pos = (
                self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * progress,
                self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * progress
            )
            
            if self.deal_progress >= 1.0:
                self.is_moving = False
                self.current_pos = self.target_pos

        if self.is_flipping:
            self.flip_progress = min(1.0, self.flip_progress + (dt / CARD_FLIP_SPEED))
            
            # Calculate scale factor for flip animation
            scale = abs(math.cos(self.flip_progress * math.pi))
            
            # Switch image halfway through flip
            if self.flip_progress >= 0.5 and not self.revealed:
                self.current_image = self.front_image
                self.revealed = True
            
            # Scale image for flip effect
            scaled_width = int(CARD_WIDTH * scale)
            if scaled_width > 0:
                self.current_image = pygame.transform.scale(
                    self.current_image,
                    (scaled_width, CARD_HEIGHT)
                )
            
            if self.flip_progress >= 1.0:
                self.is_flipping = False
                self.current_image = self.front_image
    
    def draw(self, screen, alpha=255):
        """Draw the card with optional transparency"""
        if alpha < 255:
            # Create a copy of the image with transparency
            temp_surface = self.current_image.copy()
            temp_surface.set_alpha(alpha)
            screen.blit(temp_surface, self.current_pos)
        else:
            screen.blit(self.current_image, self.current_pos)

    @staticmethod
    def _ease_out_quad(t):
        return t * (2 - t) 