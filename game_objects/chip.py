import pygame
from constants import CHIP_SIZE, CHIP_MOVE_SPEED

class Chip:
    def __init__(self, value, image, start_pos):
        self.value = value
        self.original_image = pygame.transform.scale(image, (CHIP_SIZE, CHIP_SIZE))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.start_pos = start_pos
        self.target_pos = start_pos
        self.current_pos = start_pos
        self.is_moving = False
        self.move_progress = 0

    def move_to(self, target_pos):
        self.start_pos = self.current_pos
        self.target_pos = target_pos
        self.is_moving = True
        self.move_progress = 0

    def update(self, dt):
        if self.is_moving:
            self.move_progress = min(1.0, self.move_progress + (dt / CHIP_MOVE_SPEED))
            
            # Use easing function for smooth movement
            progress = self._ease_out_quad(self.move_progress)
            
            self.current_pos = (
                self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * progress,
                self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * progress
            )
            
            if self.move_progress >= 1.0:
                self.is_moving = False
                self.current_pos = self.target_pos

    def draw(self, screen):
        screen.blit(self.image, self.current_pos)

    @staticmethod
    def _ease_out_quad(t):
        return t * (2 - t) 