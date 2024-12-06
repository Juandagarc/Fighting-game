import pygame
import os
from models.player import Player, DiagonalPlatform

# Load background image for the game
current_dir = os.path.dirname(__file__)
game_background_path = os.path.join(current_dir, "../assets/game/background.png")
game_background = pygame.image.load(game_background_path)
game_background = pygame.transform.scale(game_background, (1280, 720))

game_active = True

font_path = os.path.join(current_dir, "../assets/fonts/Tiny5/Tiny5-Regular.ttf")
title_font = pygame.font.Font(font_path, 80)

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
player1 = Player(1130, 300, 50, 100, (0, 0, 255), player1_controls)
player2 = Player(100, 300, 50, 100, (255, 0, 0), player2_controls)



# Define walls, floors, and diagonal platforms
colliders = [
    pygame.Rect(200, 600, 150, 20),
    pygame.Rect(450, 550, 250, 20),
    pygame.Rect(60, 630, 60, 20),
    pygame.Rect(800, 500, 270, 20),
    pygame.Rect(1170, 550, 10, 20),
    pygame.Rect(0, 0, 10, 720),  # Left wall
    pygame.Rect(1270, 0, 10, 720),  # Right wall
]

diagonal_platforms = [
    DiagonalPlatform(70, 730, 200, 600),
    DiagonalPlatform(350, 650, 450, 550),
    DiagonalPlatform(570, 730, 800, 500),
    DiagonalPlatform(0, 700, 60, 630),
    DiagonalPlatform(1070, 500, 1170, 600),
    DiagonalPlatform(1180, 550, 1270, 650),
]


def handle_combat(player1, player2):
    """
    Handle combat interactions between two players.
    """
    if player1.is_attacking and player1.rect.colliderect(player2.rect):
        player2.take_damage(10)  # Reduce la salud del jugador 2

    if player2.is_attacking and player2.rect.colliderect(player1.rect):
        player1.take_damage(10)  # Reduce la salud del jugador 1


def render_colliders(screen, colliders, diagonal_platforms):
    """
    Render colliders for debugging purposes.
    """
    for collider in colliders:
        pygame.draw.rect(screen, (0, 255, 0), collider, 1)

    for platform in diagonal_platforms:
        pygame.draw.line(screen, (0, 255, 255), (platform.x1, platform.y1), (platform.x2, platform.y2), 1)


def render_game(screen):
    global game_active  # Accedemos a la variable global

    # Dibujar el fondo
    screen.blit(game_background, (0, 0))

    # Obtener teclas presionadas
    keys = pygame.key.get_pressed()

    if game_active:
        # Actualizar jugadores
        player1.move(keys, colliders)  # Movimiento horizontal
        player1.apply_gravity(colliders, diagonal_platforms)  # Maneja gravedad y plataformas diagonales
        player1.jump(keys)
        player1.defend(keys)
        player1.attack(keys)

        player2.move(keys, colliders)  # Movimiento horizontal
        player2.apply_gravity(colliders, diagonal_platforms)  # Maneja gravedad y plataformas diagonales
        player2.jump(keys)
        player2.defend(keys)
        player2.attack(keys)

        # Manejar combate
        handle_combat(player1, player2)

    # Dibujar jugadores
    player1.draw(screen)
    player2.draw(screen)

    # Dibujar colisionadores (depuración)
    render_colliders(screen, colliders, diagonal_platforms)

    # Verificar si alguno de los jugadores ha sido derrotado
    if player1.is_defeated():
        game_active = False  # Desactivar el juego
        draw_text(screen, "Player 2 Wins!", title_font, (0, 0, 255), 640, 360)

    elif player2.is_defeated():
        game_active = False  # Desactivar el juego
        draw_text(screen, "Player 1 Wins!", title_font, (255, 0, 0), 640, 360)



def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
