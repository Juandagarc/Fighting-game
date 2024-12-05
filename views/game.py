import pygame
import os
from models.player import Player, DiagonalPlatform

# Load background image for the game
current_dir = os.path.dirname(__file__)
game_background_path = os.path.join(current_dir, "../assets/game/background.png")
game_background = pygame.image.load(game_background_path)
game_background = pygame.transform.scale(game_background, (1280, 720))

# Define key bindings for each player
player1_controls = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "defend": pygame.K_o,
    "attack": pygame.K_p,
}

player2_controls = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "defend": pygame.K_g,
    "attack": pygame.K_h,
}

# Create players
player1 = Player(100, 300, 50, 100, (255, 0, 0), player1_controls)
player2 = Player(1130, 300, 50, 100, (0, 0, 255), player2_controls)

# Define walls, floors, and diagonal platforms
colliders = [
    pygame.Rect(0, 680, 1280, 40),  # Floor
    pygame.Rect(200, 500, 200, 20),  # Platform 1
    pygame.Rect(800, 400, 200, 20),  # Platform 2
    pygame.Rect(600, 300, 100, 20),  # Small platform
    pygame.Rect(0, 0, 10, 720),  # Left wall
    pygame.Rect(1270, 0, 10, 720),  # Right wall
]

diagonal_platforms = [
    DiagonalPlatform(400, 600, 600, 500),  # Example diagonal platform
    DiagonalPlatform(800, 200, 1000, 300),  # Another diagonal platform
]


def render_colliders(screen, colliders, diagonal_platforms):
    """
    Render colliders for debugging purposes.
    """
    for collider in colliders:
        pygame.draw.rect(screen, (0, 255, 0), collider, 1)

    for platform in diagonal_platforms:
        pygame.draw.line(screen, (0, 255, 255), (platform.x1, platform.y1), (platform.x2, platform.y2), 1)


def render_game(screen):
    # Draw the background
    screen.blit(game_background, (0, 0))

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Update players
    player1.move(keys, colliders)
    player1.jump(keys)
    player1.apply_gravity(colliders, diagonal_platforms)
    player1.defend(keys)
    player1.attack(keys)

    player2.move(keys, colliders)
    player2.jump(keys)
    player2.apply_gravity(colliders, diagonal_platforms)
    player2.defend(keys)
    player2.attack(keys)

    # Draw players
    player1.draw(screen)
    player2.draw(screen)

    # Draw colliders (debugging)
    render_colliders(screen, colliders, diagonal_platforms)


def draw_text(screen, text, color, x, y, font_size):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
