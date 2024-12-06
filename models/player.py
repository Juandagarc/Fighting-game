import pygame
import os

class Player:
    def __init__(self, x, y, width, height, color, controls):
        """
        Initialize the player object.
        """
        self.rect = pygame.Rect(x, y, width-100, height)
        self.color = color
        self.velocity = 5
        self.y_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -15
        self.on_ground = False
        self.controls = controls
        self.health = 100
        self.is_attacking = False
        self.is_defending = False
        self.attack_cooldown = 500  # En milisegundos (0.5 segundos)
        self.last_attack_time = 0  # Marca de tiempo del último ataque

    def move(self, keys, colliders):
        """
        Handles player movement and wall collision.
        """
        if keys[self.controls["left"]]:
            self.rect.x -= self.velocity
            for collider in colliders:
                if self.rect.colliderect(collider):
                    self.rect.left = collider.right
                    break

        if keys[self.controls["right"]]:
            self.rect.x += self.velocity
            for collider in colliders:
                if self.rect.colliderect(collider):
                    self.rect.right = collider.left
                    break

    def apply_gravity(self, colliders, diagonal_platforms):
        """
        Applies gravity and handles collision with floors and diagonal platforms.
        """
        # Aplicar gravedad
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity

        # Verificar colisión con plataformas normales
        for collider in colliders:
            if self.rect.colliderect(collider) and self.y_velocity > 0:
                self.rect.bottom = collider.top
                self.y_velocity = 0
                self.on_ground = True
                return

        # Verificar interacción con plataformas diagonales
        for platform in diagonal_platforms:
            # Calcular las alturas en las esquinas de la hitbox
            platform_y_left = platform.get_y_at_x(self.rect.left)
            platform_y_right = platform.get_y_at_x(self.rect.right)

            # Verificar si la hitbox del jugador está en el rango horizontal de la rampa
            if platform.contains_x(self.rect.left) or platform.contains_x(self.rect.right):
                # Caso: la esquina izquierda está en la rampa
                if (
                        platform_y_left is not None
                        and self.rect.bottom >= platform_y_left - 5
                        and self.rect.bottom <= platform_y_left + 10
                ):
                    self.rect.bottom = platform_y_left
                    self.y_velocity = 0
                    self.on_ground = True
                    return

                # Caso: la esquina derecha está en la rampa
                if (
                        platform_y_right is not None
                        and self.rect.bottom >= platform_y_right - 5
                        and self.rect.bottom <= platform_y_right + 10
                ):
                    self.rect.bottom = platform_y_right
                    self.y_velocity = 0
                    self.on_ground = True
                    return

        # Si no está tocando ninguna plataforma, el jugador está en el aire
        self.on_ground = False

    def collides_with_diagonal(self, platform):
        """
        Check if the player is close enough to interact with a diagonal platform.
        """
        player_bottom = self.rect.bottom
        platform_y = platform.get_y_at_x(self.rect.centerx)

        # Ensure the player is slightly above the platform
        tolerance = 5  # Pixels of tolerance for smoother interaction

        return (
            platform.contains_x(self.rect.centerx)
            and platform_y - tolerance <= player_bottom <= platform_y + tolerance
        )

    def jump(self, keys):
        """
        Allows the player to jump if on the ground.
        """
        if keys[self.controls["up"]] and self.on_ground:
            self.y_velocity = self.jump_strength

    def attack(self, keys):
        """
        Handles the player's attack action with cooldown.
        """
        current_time = pygame.time.get_ticks()  # Tiempo actual en milisegundos
        if keys[self.controls["attack"]] and current_time - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = True
            self.last_attack_time = current_time
        else:
            self.is_attacking = False

    def defend(self, keys):
        """
        Handles the player's defend action.
        """
        self.is_defending = keys[self.controls["defend"]]

    def take_damage(self, amount):
        """
        Reduces the player's health when taking damage.
        """
        if not self.is_defending:
            self.health -= amount
            if self.health < 0:  # Asegura que no sea negativo
                self.health = 0

    def is_defeated(self):
        """
        Checks if the player is defeated.
        """
        return self.health <= 0

    def draw(self, screen):
        """
        Draw the player and their health bar on the screen.
        """
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw the health bar
        health_bar_width = 50
        health_bar_height = 10
        health_ratio = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 15, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 15, health_bar_width * health_ratio, health_bar_height))



import pygame
import os
from models.DiagonalPlatform import DiagonalPlatform


class Player:
    def __init__(self, x, y, sprite_sheet, controls, frame_width, frame_height, animation_speed):
        """
        Initialize the player object with animation.
        """
        self.rect = pygame.Rect(x, y, frame_width-10, frame_height)
        self.controls = controls
        self.health = 100
        self.is_attacking = False
        self.is_defending = False
        self.attack_cooldown = 500  # En milisegundos (0.5 segundos)
        self.last_attack_time = 0  # Marca de tiempo del último ataque
        self.velocity = 5
        self.y_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -15
        self.on_ground = False

        # Use the preloaded sprite sheet
        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = self._load_frames()
        self.current_frame = 0
        self.animation_speed = animation_speed
        self.frame_counter = 0

    def _load_frames(self):
        """
        Extract individual frames from the sprite sheet and resize them to be 5 times larger than the hitbox.
        """
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()
        frames = []

        # Dimensiones escaladas
        scaled_width = self.rect.width * 3
        scaled_height = self.rect.height * 3

        for x in range(0, sheet_width, self.frame_width):
            # Extraer el fotograma original
            frame = self.sprite_sheet.subsurface((x, 0, self.frame_width, self.frame_height))

            # Redimensionar el fotograma al tamaño escalado
            resized_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
            frames.append(resized_frame)

        return frames

    def update_animation(self):
        """
        Update the animation frame.
        """
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def move(self, keys, colliders):
        """
        Handles player movement and wall collision.
        """
        if keys[self.controls["left"]]:
            self.rect.x -= self.velocity
            for collider in colliders:
                if self.rect.colliderect(collider):
                    self.rect.left = collider.right
                    break

        if keys[self.controls["right"]]:
            self.rect.x += self.velocity
            for collider in colliders:
                if self.rect.colliderect(collider):
                    self.rect.right = collider.left
                    break

    def apply_gravity(self, colliders, diagonal_platforms):
        """
        Applies gravity and handles collision with floors and diagonal platforms.
        """
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity

        # Check for collisions with floors (only when falling)
        for collider in colliders:
            if self.rect.colliderect(collider) and self.y_velocity > 0:
                self.rect.bottom = collider.top
                self.y_velocity = 0
                self.on_ground = True
                return

        # Check for interactions with diagonal platforms
        for platform in diagonal_platforms:
            platform_y_left = platform.get_y_at_x(self.rect.left)
            if (
                platform.contains_x(self.rect.left)
                and platform_y_left is not None
                and self.rect.bottom >= platform_y_left - 5
                and self.rect.bottom <= platform_y_left + 10
            ):
                self.rect.bottom = platform_y_left
                self.y_velocity = 0
                self.on_ground = True
                return

            platform_y_right = platform.get_y_at_x(self.rect.right)
            if (
                platform.contains_x(self.rect.right)
                and platform_y_right is not None
                and self.rect.bottom >= platform_y_right - 5
                and self.rect.bottom <= platform_y_right + 10
            ):
                self.rect.bottom = platform_y_right
                self.y_velocity = 0
                self.on_ground = True
                return

        self.on_ground = False

    def jump(self, keys):
        """
        Allows the player to jump if on the ground.
        """
        if keys[self.controls["up"]] and self.on_ground:
            self.y_velocity = self.jump_strength

    def attack(self, keys):
        """
        Handles the player's attack action with cooldown.
        """
        current_time = pygame.time.get_ticks()
        if keys[self.controls["attack"]] and current_time - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = True
            self.last_attack_time = current_time
        else:
            self.is_attacking = False

    def defend(self, keys):
        """
        Handles the player's defend action.
        """
        self.is_defending = keys[self.controls["defend"]]

    def take_damage(self, amount):
        """
        Reduces the player's health when taking damage.
        """
        if not self.is_defending:
            self.health -= amount
            if self.health < 0:
                self.health = 0

    def is_defeated(self):
        """
        Checks if the player is defeated.
        """
        return self.health <= 0

    def draw(self, screen):
        """
        Draw the current animation frame at the player's position, scaled 5x larger than the hitbox.
        """
        # Actualizar la animación
        self.update_animation()

        # Obtener el fotograma actual
        frame = self.frames[self.current_frame]

        # Calcular posición para centrar el sprite con respecto a la hitbox
        sprite_x = self.rect.centerx - frame.get_width() // 2
        sprite_y = self.rect.bottom - (frame.get_height() - 50)

        # Dibujar el sprite escalado
        screen.blit(frame, (sprite_x, sprite_y))

        # Dibujar la hitbox (opcional, para depuración)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Borde rojo

        # Dibujar barra de vida
        health_bar_width = 50  # Ancho de la barra de vida
        health_bar_height = 8  # Alto de la barra de vida
        health_ratio = self.health / 100  # Proporción de salud actual

        # Coordenadas de la barra de vida
        bar_x = self.rect.centerx - health_bar_width // 2
        bar_y = self.rect.top - health_bar_height - 5  # Posición encima del jugador

        # Fondo de la barra (rojo)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_bar_width, health_bar_height))

        # Salud actual (verde)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))
