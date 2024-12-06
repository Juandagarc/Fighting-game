import pygame

class Player:
    def __init__(self, x, y, sprite_sheets, controls, frame_width, frame_height, animation_speed):
        """
        Initialize the player object with animations for different states.
        """
        self.rect = pygame.Rect(x, y, frame_width - 10, frame_height)
        self.controls = controls
        self.health = 100
        self.is_attacking = False  # Asegúrate de definirlo aquí
        self.is_defending = False
        self.attack_cooldown = 500  # En milisegundos (0.5 segundos)
        self.last_attack_time = 0  # Marca de tiempo del último ataque
        self.velocity = 5
        self.y_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -15
        self.on_ground = False

        self.facing_left = False  # Nueva bandera para determinar la dirección

        # Animations for different states
        self.sprite_sheets = sprite_sheets
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.animations = {state: self._load_frames(sheet) for state, sheet in sprite_sheets.items()}

        # Validar que cada animación tiene fotogramas
        for state, frames in self.animations.items():
            if len(frames) == 0:
                raise ValueError(f"No frames loaded for animation state '{state}'")

        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = animation_speed
        self.frame_counter = 0


    def _load_frames(self, sprite_sheet):
        """
        Extract individual frames from a sprite sheet and scale them up to twice their size.
        """
        sheet_width = sprite_sheet.get_width()
        frames = []

        for x in range(0, sheet_width, self.frame_width):
            # Extract the frame
            frame = sprite_sheet.subsurface((x, 0, self.frame_width, self.frame_height))

            # Scale the frame to twice its size
            scaled_frame = pygame.transform.scale(frame, (self.frame_width * 2, self.frame_height * 2))

            frames.append(scaled_frame)

        return frames

    def update_animation(self):
        """
        Update the animation frame based on the current state.
        Handles cyclic animations (e.g., running) and one-time animations (e.g., attacking).
        """
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0

            # Validar que la animación actual tiene fotogramas
            if len(self.animations[self.current_animation]) > 0:
                if self.current_animation in ["attacking", "jumping"]:
                    # Animaciones no cíclicas
                    if self.current_frame + 1 >= len(self.animations[self.current_animation]):
                        self.current_frame = 0
                        self.current_animation = "idle"  # Cambiar a "idle" al finalizar
                    else:
                        self.current_frame += 1
                else:
                    # Animaciones cíclicas (idle, running)
                    self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            else:
                self.current_frame = 0  # Reiniciar fotograma si no hay fotogramas disponibles

    def update_state(self, keys):
        """
        Update the player's state based on input and conditions.
        Handle transitions between animations.
        """
        new_animation = None
        if keys[self.controls["attack"]]:
            new_animation = "attacking"
        elif keys[self.controls["left"]] or keys[self.controls["right"]]:
            new_animation = "running"
        elif not self.on_ground:
            new_animation = "jumping"
        else:
            new_animation = "idle"

        # Cambiar animación solo si es diferente
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0  # Reiniciar al primer fotograma de la nueva animación

    def move(self, keys, colliders):
        """
        Handles player movement and wall collision.
        """
        if keys[self.controls["left"]]:
            self.rect.x -= self.velocity
            self.facing_left = True  # Actualiza la dirección del jugador
            for collider in colliders:
                if self.rect.colliderect(collider):
                    self.rect.left = collider.right
                    break

        if keys[self.controls["right"]]:
            self.rect.x += self.velocity
            self.facing_left = False  # Actualiza la dirección del jugador
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
        Draw the current animation frame at the player's position.
        """
        self.update_animation()

        # Verificar que hay fotogramas para la animación actual
        if len(self.animations[self.current_animation]) > 0:
            frame = self.animations[self.current_animation][self.current_frame]
        else:
            print(f"Warning: No frames available for animation state '{self.current_animation}'")
            return  # Evitar dibujar si no hay fotogramas disponibles

        # Hacer espejo si el jugador está mirando hacia la izquierda
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)

        # Dibujar el fotograma
        sprite_x = self.rect.centerx - frame.get_width() // 2
        sprite_y = self.rect.bottom - frame.get_height() + 40
        screen.blit(frame, (sprite_x, sprite_y))

        # Dibujar barra de vida
        health_bar_width = 50
        health_bar_height = 8
        health_ratio = self.health / 100
        bar_x = self.rect.centerx - health_bar_width // 2
        bar_y = self.rect.top - health_bar_height - 5
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))
        # Dibujar la hitbox (opcional, para depuración)
        #  pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Borde rojo
