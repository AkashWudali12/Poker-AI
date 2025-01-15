import pygame
from components.button import Button
from game_objects.poker_game_animations import PokerGameAnimations, GameState

def game(screen):
    """
    A poker game scene optimized for 1040x720 display with game control buttons.
    """
    clock = pygame.time.Clock()
    running = True
    next_scene = "game"

    # Initialize game animations
    game_animations = PokerGameAnimations(screen)
    
    # Add test players
    game_animations.add_player("player_1", 0)  # Bottom center
    game_animations.add_player("player_2", 3)  # Left middle
    game_animations.add_player("player_3", 7)  # Top center
    game_animations.add_player("player_4", 4)  # Right middle
    game_animations.add_player("player_5", 1)  # Left middle

    # Load and scale the background
    background = pygame.image.load('assets/poker_table.jpg')
    background = pygame.transform.scale(background, (1040, 720))

    # Button callbacks
    def on_deal_players():
        # Example player hands (in real game, this would come from game logic)
        player_hands = {
            "player_1": [(2, "hearts"), (3, "clubs")],
            "player_2": [(4, "diamonds"), (5, "spades")],
            "player_3": [(6, "hearts"), (7, "diamonds")],
            "player_4": [(8, "clubs"), (9, "spades")],
            "player_5": [(10, "hearts"), (11, "diamonds")],
        }
        game_animations.deal_player_cards(player_hands)

    def on_deal_flop():
        if game_animations.state == GameState.PRE_FLOP:
            # Example flop cards
            flop_cards = [(10, "hearts"), (11, "diamonds"), (12, "clubs")]
            game_animations.deal_community_cards(flop_cards, "flop")

    def on_deal_turn():
        if game_animations.state == GameState.FLOP:
            # Example turn card
            turn_card = [(13, "spades")]
            game_animations.deal_community_cards(turn_card, "turn")

    def on_deal_river():
        if game_animations.state == GameState.TURN:
            # Example river card
            river_card = [(1, "hearts")]
            game_animations.deal_community_cards(river_card, "river")

    def on_check():
        print("Check button pressed!")

    def on_fold():
        print("Fold button pressed!")

    def on_call():
        print("Call button pressed!")

    def on_raise():
        print("Raise button pressed!")

    def on_quit():
        nonlocal running, next_scene
        running = False
        next_scene = "main_menu"

    # Button styling with colors matching React version
    button_styles = {
        "Deal Players": {
            "normal": (75, 0, 130),     # Purple
            "hover": (85, 26, 139),
            "pressed": (65, 0, 120),
        },
        "Deal Flop": {
            "normal": (0, 100, 0),      # Dark Green
            "hover": (0, 120, 0),
            "pressed": (0, 80, 0),
        },
        "Deal Turn": {
            "normal": (139, 69, 19),    # Brown
            "hover": (160, 82, 45),
            "pressed": (119, 59, 9),
        },
        "Deal River": {
            "normal": (25, 25, 112),    # Midnight Blue
            "hover": (45, 45, 132),
            "pressed": (15, 15, 92),
        },
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
    
    # Calculate positions for two rows of buttons
    # Top row for dealing buttons
    deal_buttons = [
        ("Deal Players", on_deal_players),
        ("Deal Flop", on_deal_flop),
        ("Deal Turn", on_deal_turn),
        ("Deal River", on_deal_river),
    ]
    
    # Bottom row for action buttons
    action_buttons = [
        ("Check", on_check),
        ("Call", on_call),
        ("Raise", on_raise),
        ("Fold", on_fold),
        ("Quit", on_quit),
    ]

    buttons = []
    
    # Create dealing buttons (top row)
    total_width_deal = (button_width * len(deal_buttons)) + (spacing * (len(deal_buttons) - 1))
    start_x_deal = (1040 - total_width_deal) // 2
    base_y_deal = 720 - button_height * 2 - spacing - 50  # 50px from bottom, above action buttons
    
    current_x = start_x_deal
    for label, callback in deal_buttons:
        style = button_styles[label]
        btn = Button(
            text=label,
            x=current_x,
            y=base_y_deal,
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
        buttons.append(btn)
        current_x += button_width + spacing

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
        buttons.append(btn)
        current_x += button_width + spacing

    # Main game loop
    while running:
        dt = clock.tick(60)
        event_list = pygame.event.get()
        
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
                next_scene = "quit"

        # Update animations
        game_animations.update(dt)

        # Update button states
        for btn in buttons:
            btn.update(event_list)

        # Draw everything
        screen.blit(background, (0, 0))
        
        # Draw game animations
        game_animations.draw()
        
        # Draw buttons
        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()

    return next_scene
