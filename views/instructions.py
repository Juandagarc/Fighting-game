import pygame
import os

# Setup colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
pygame.font.init()

# Load font
current_dir = os.path.dirname(__file__)
font_path = os.path.join(current_dir, "../assets/fonts/Tiny5/Tiny5-Regular.ttf")
instruction_font = pygame.font.Font(font_path, 36)
title_font = pygame.font.Font(font_path, 50)


def draw_text(surface, text, font, color, x, y):
    """
    Draw text on the screen at a specific position.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def render_instructions(screen):
    """
    Renders the instructions view.
    """
    # Fill the screen with a gray background
    screen.fill(GRAY)

    # Draw the title
    draw_text(screen, "Instrucciones", title_font, BLACK, 640, 100)

    # Display instructions for player.py 1
    draw_text(screen, "Jugador 1:", instruction_font, BLACK, 320, 200)
    draw_text(screen, "- \u2191, \u2190, \u2193, \u2192: Moverse", instruction_font, BLACK, 320, 250)
    draw_text(screen, "- O: Defenderse", instruction_font, BLACK, 320, 300)
    draw_text(screen, "- P: Atacar", instruction_font, BLACK, 320, 350)

    # Display instructions for player.py 2
    draw_text(screen, "Jugador 2:", instruction_font, BLACK, 960, 200)
    draw_text(screen, "- W, A, S, D: Moverse", instruction_font, BLACK, 960, 250)
    draw_text(screen, "- G: Defenderse", instruction_font, BLACK, 960, 300)
    draw_text(screen, "- H: Atacar", instruction_font, BLACK, 960, 350)

    # Draw a "Back" button
    back_button = pygame.Rect(540, 500, 200, 50)
    pygame.draw.rect(screen, BLACK, back_button)
    draw_text(screen, "Volver", instruction_font, WHITE, back_button.centerx, back_button.centery)

    return back_button
