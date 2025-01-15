import pygame

class Button:
    def __init__(
        self, text, x, y, width, height,
        normal_color=(70, 70, 70),
        hover_color=(100, 100, 100),
        pressed_color=(50, 50, 50),
        text_color=(255, 255, 255),
        font=None,
        callback=None,
        border_radius=10
    ):
        """
        A simple Button class for Pygame with rounded corners and hover/pressed animations.
        :param text: Button label
        :param x, y: Top-left coordinates
        :param width, height: Button size
        :param normal_color: Default background color
        :param hover_color: Background color on mouse hover
        :param pressed_color: Background color when clicked
        :param text_color: Color of the button label
        :param font: A pygame.font.Font object to render the text
        :param callback: A function to call when the button is clicked
        :param border_radius: How round the corners are
        """
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.text_color = text_color
        self.font = font
        self.callback = callback
        self.border_radius = border_radius

        self.is_hovered = False
        self.is_pressed = False

        # Render text once; store it so we don’t recreate every frame
        if not self.font:
            self.font = pygame.font.SysFont(None, 28)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def update(self, event_list):
        """
        Update the button state based on mouse events.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered:
                    self.is_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.is_pressed and self.is_hovered:
                    # Click occurred
                    if self.callback:
                        self.callback()
                self.is_pressed = False

    def draw(self, surface):
        """
        Draw the button onto the given surface with different colors
        depending on the current state (normal, hover, pressed).
        """
        if self.is_pressed:
            color = self.pressed_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.normal_color

        # Draw rounded rectangle (available in newer Pygame versions)
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)

        # Recompute text_rect center in case the button moved (not typical here, but good practice)
        self.text_rect.center = self.rect.center
        surface.blit(self.text_surface, self.text_rect)