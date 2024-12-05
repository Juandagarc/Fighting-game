import pygame
from views.menu import render_menu
from views.instructions import render_instructions
from views.game import render_game

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Fighting Game")  # Set the window title
clock = pygame.time.Clock()
running = True

# Control state (menu, instructions, or game)
current_view = "menu"

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # Handle button clicks
            mouse_pos = event.pos

            if current_view == "menu":
                buttons = render_menu(screen)  # Get the buttons from the menu
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):  # Check if a button is clicked
                        if button["text"] == "Jugar":
                            current_view = "game"  # Switch to game view
                        elif button["text"] == "Cómo se juega":
                            current_view = "instructions"  # Switch to instructions view
                        elif button["text"] == "Salir":
                            running = False  # Exit the game

            elif current_view == "instructions":
                back_button = render_instructions(screen)  # Get the back button
                if back_button.collidepoint(mouse_pos):  # Check if the back button is clicked
                    current_view = "menu"  # Return to the menu

    # Render the current view
    if current_view == "menu":
        render_menu(screen)
    elif current_view == "instructions":
        render_instructions(screen)
    elif current_view == "game":
        render_game(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
