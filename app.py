import pygame
from main_menu import main_menu
from game_scene import game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1040, 900))
    pygame.display.set_caption("Poker Game")

    current_scene = "main_menu"
    while current_scene != "quit":
        if current_scene == "main_menu":
            current_scene = main_menu(screen)
        elif current_scene == "game":
            print("Starting game, going to game scene")
            current_scene = game(screen)
        else:
            # If something unexpected is returned
            current_scene = "quit"

    pygame.quit()

if __name__ == "__main__":
    main()
