import pygame
from components.button import Button

def main_menu(screen):
    """
    Displays the main menu with a background image
    and a 'Start' button. Returns the name of the
    next scene to run when the user clicks Start
    or chooses to quit.
    """
    # Load the background image
    background = pygame.image.load('assets/poker_table.jpg')
    background = pygame.transform.scale(background, (1040, 720))
    
    # Create the Start button - positioned in the middle bottom area
    button_width = 200
    button_height = 50
    button_x = (1040 - button_width) // 2  # Center horizontally
    button_y = 720 - button_height - 100   # 100px from bottom
    
    # Initialize the button with custom colors matching our React styling
    start_button = Button(
        text="Start Game",
        x=button_x,
        y=button_y,
        width=button_width,
        height=button_height,
        normal_color=(74, 144, 226),    # #4a90e2
        hover_color=(53, 122, 189),     # #357abd
        pressed_color=(45, 100, 160),   # Slightly darker
        text_color=(255, 255, 255),
        font=pygame.font.SysFont(None, 36),
        border_radius=4
    )

    clock = pygame.time.Clock()
    running = True
    next_scene = "main_menu"  # default, stay here

    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
                next_scene = "quit"

        # Update button state
        start_button.update(event_list)
        
        # If button was clicked, change scene
        if start_button.is_pressed:
            running = False
            next_scene = "game"

        # Draw everything
        screen.blit(background, (0, 0))
        start_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    return next_scene
