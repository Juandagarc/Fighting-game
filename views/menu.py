import pygame
import os

# Setup
pygame.font.init()

# Load font and set paths
current_dir = os.path.dirname(__file__)
font_path = os.path.join(current_dir, "../assets/fonts/Tiny5/Tiny5-Regular.ttf")
title_font = pygame.font.Font(font_path, 80)
button_font = pygame.font.Font(font_path, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Load background image
background_image_path = os.path.join(current_dir, "../assets/menu/background.png")
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (1280, 720))


def draw_text(surface, text, font, color, x, y):
    """
    Draw text on the screen at a specific position.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def create_button(x, y, width, height, text, font, bg_color, text_color):
    """
    Create a button dictionary with scalable size and position.
    """
    button_rect = pygame.Rect(x, y, width, height)
    return {
        "rect": button_rect,
        "text": text,
        "font": font,
        "bg_color": bg_color,
        "text_color": text_color,
    }


def render_button(surface, button):
    """
    Render a single button on the screen.
    """
    pygame.draw.rect(surface, button["bg_color"], button["rect"])  # Draw button background
    draw_text(
        surface,
        button["text"],
        button["font"],
        button["text_color"],
        button["rect"].centerx,
        button["rect"].centery,
    )


def render_menu(screen):
    """
    Renders the view with a background image, a title, and buttons.
    """
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the title
    draw_text(screen, "SAMURAIS vs KNIGHTS", title_font, WHITE, 600, 140)  # Centered title

    # Define buttons
    buttons = [
        create_button(480, 300, 300, 70, "Jugar", button_font, GRAY, BLACK),
        create_button(480, 400, 300, 70, "Cómo se juega", button_font, GRAY, BLACK),
        create_button(480, 500, 300, 70, "Salir", button_font, GRAY, BLACK),
    ]

    # Draw all buttons
    for button in buttons:
        render_button(screen, button)

    return buttons  # Return the buttons for interaction
