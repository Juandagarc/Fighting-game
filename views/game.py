import pygame
import os
from models.player import Player
from models.DiagonalPlatform import DiagonalPlatform

# Cargar fondo del juego
current_dir = os.path.dirname(__file__)
game_background_path = os.path.join(current_dir, "../assets/game/background.png")
game_background = pygame.image.load(game_background_path)
game_background = pygame.transform.scale(game_background, (1280, 720))

game_active = True

font_path = os.path.join(current_dir, "../assets/fonts/Tiny5/Tiny5-Regular.ttf")
title_font = pygame.font.Font(font_path, 80)

# Definir controles para los jugadores
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

# Definir paredes, pisos y plataformas diagonales
colliders = [
    pygame.Rect(200, 600, 119, 20),
    pygame.Rect(450, 550, 219, 20),
    pygame.Rect(60, 630, 26, 20),
    pygame.Rect(800, 500, 260, 20),
    pygame.Rect(1200, 550, 10, 20),
    pygame.Rect(0, 0, 10, 720),  # Pared izquierda
    pygame.Rect(1270, 0, 10, 720),  # Pared derecha
]

diagonal_platforms = [
    DiagonalPlatform(70, 730, 200, 600),
    DiagonalPlatform(350, 650, 450, 550),
    DiagonalPlatform(570, 730, 800, 500),
    DiagonalPlatform(0, 700, 60, 630),
    DiagonalPlatform(1060, 500, 1170, 600),
]


def handle_combat(player1, player2):
    """
    Manejar las interacciones de combate entre los dos jugadores.
    """
    if player1.is_attacking and player1.rect.colliderect(player2.rect):
        player2.take_damage(10)  # Reduce la salud del jugador 2

    if player2.is_attacking and player2.rect.colliderect(player1.rect):
        player1.take_damage(10)  # Reduce la salud del jugador 1



def render_colliders(screen, colliders, diagonal_platforms):
    """
    Renderizar colisionadores para propósitos de depuración.
    """
    for collider in colliders:
        pygame.draw.rect(screen, (0, 255, 0), collider, 1)

    for platform in diagonal_platforms:
        pygame.draw.line(screen, (0, 255, 255), (platform.x1, platform.y1), (platform.x2, platform.y2), 1)


def render_game(screen, player1_sprites, player2_sprites):
    """
    Renderizar la vista del juego.
    """
    global game_active  # Acceder a la variable global

    player1 = Player(
        x=1130,
        y=300,
        sprite_sheets=player1_sprites,
        controls=player1_controls,
        frame_width=96,  # Ancho de un fotograma
        frame_height=96,  # Alto de un fotograma
        animation_speed=5  # Velocidad de animación
    )

    player2 = Player(
        x=100,
        y=300,
        sprite_sheets=player2_sprites,
        controls=player2_controls,
        frame_width=96,  # Ancho de un fotograma
        frame_height=96,  # Alto de un fotograma
        animation_speed=5  # Velocidad de animación
    )

    clock = pygame.time.Clock()
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Dibujar el fondo
        screen.blit(game_background, (0, 0))

        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()

        # Actualizar jugadores
        player1.update_state(keys)
        player1.attack(keys)  # Detectar ataque
        player1.jump(keys)
        player1.move(keys, colliders)
        player1.apply_gravity(colliders, diagonal_platforms)

        player1.update_animation()
        player2.update_animation()

        player2.update_state(keys)
        player2.attack(keys)  # Detectar ataque
        player2.jump(keys)
        player2.move(keys, colliders)
        player2.apply_gravity(colliders, diagonal_platforms)

        # Manejar combate
        handle_combat(player1, player2)

        # Dibujar jugadores
        player1.draw(screen)
        player2.draw(screen)

        # Dibujar colisionadores (depuración)
        render_colliders(screen, colliders, diagonal_platforms)

        # Verificar si alguno de los jugadores ha sido derrotado
        if player1.is_defeated():
            game_active = False
            draw_text(screen, "Player 2 Wins!", title_font, (0, 0, 255), 640, 360)

        elif player2.is_defeated():
            game_active = False
            draw_text(screen, "Player 1 Wins!", title_font, (255, 0, 0), 640, 360)

        pygame.display.flip()
        clock.tick(60)


def draw_text(screen, text, font, color, x, y):
    """
    Dibujar texto en la pantalla.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
