import pygame
import os
from views.menu import render_menu
from views.instructions import render_instructions
from views.game import render_game

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Fighting Game")
clock = pygame.time.Clock()

# Cargar recursos (sprites, sonidos, etc.)
current_dir = os.path.dirname(__file__)

player1_sprite_sheet = pygame.image.load(os.path.join(current_dir, "assets/game/samurai/IDLE.png")).convert_alpha()
player2_sprite_sheet = pygame.image.load(os.path.join(current_dir, "assets/game/samurai/IDLE.png")).convert_alpha()

# Control del estado del juego
running = True
current_view = "menu"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if current_view == "menu":
                buttons = render_menu(screen)
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["text"] == "Jugar":
                            current_view = "game"
                        elif button["text"] == "Cómo se juega":
                            current_view = "instructions"
                        elif button["text"] == "Salir":
                            running = False

            elif current_view == "instructions":
                back_button = render_instructions(screen)
                if back_button.collidepoint(mouse_pos):
                    current_view = "menu"

    # Renderizar la vista actual
    if current_view == "menu":
        render_menu(screen)
    elif current_view == "instructions":
        render_instructions(screen)
    elif current_view == "game":
        # Pasar las hojas de sprites a render_game
        render_game(screen, player1_sprite_sheet, player2_sprite_sheet)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
