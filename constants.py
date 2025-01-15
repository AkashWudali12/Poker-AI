# Screen dimensions
SCREEN_WIDTH = 1040
SCREEN_HEIGHT = 720

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (220, 20, 60)

# Table dimensions
TABLE_WIDTH = SCREEN_WIDTH // 1.5  # Roughly 1/3 of screen
TABLE_HEIGHT = SCREEN_HEIGHT // 1.5

# Animation speeds (in milliseconds)
DEAL_SPEED = 500
CHIP_MOVE_SPEED = 300
CARD_FLIP_SPEED = 200

# Card dimensions
CARD_WIDTH = 71  # Standard poker card ratio is 2.5:3.5
CARD_HEIGHT = 96

# Chip dimensions
CHIP_SIZE = 30

# Deck position (center of table)
DECK_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Calculate seat positions in a circular arrangement
SEAT_POSITIONS = [
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100),           # Bottom center
    (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 150),           # Bottom left
    (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 150),       # Bottom right
    (100, SCREEN_HEIGHT // 2),                          # Left middle
    (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2),           # Right middle
    (200, 150),                                         # Top left
    (SCREEN_WIDTH - 200, 150),                          # Top right
    (SCREEN_WIDTH // 2, 100),                           # Top center
    (SCREEN_WIDTH // 3, 100),                           # Top left-center
    (SCREEN_WIDTH * 2 // 3, 100),                       # Top right-center
]

# Pot position
POT_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50) 