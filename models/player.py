import pygame


class Player:
    def __init__(self, x, y, width, height, color, controls):
        """
        Initialize the player object.
        """
        self.rect = pygame.Rect(x, y, width, height)
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
            # Check bottom-left corner
            platform_y_left = platform.get_y_at_x(self.rect.left)
            if platform.contains_x(self.rect.left) and platform_y_left is not None:
                if self.rect.bottom >= platform_y_left - 1:  # Slight tolerance for touch
                    self.rect.bottom = platform_y_left - 1  # Align to the ramp
                    self.y_velocity = 0
                    self.on_ground = True
                    return

            # Check bottom-right corner
            platform_y_right = platform.get_y_at_x(self.rect.right)
            if platform.contains_x(self.rect.right) and platform_y_right is not None:
                if self.rect.bottom >= platform_y_right - 1:  # Slight tolerance for touch
                    self.rect.bottom = platform_y_right - 1  # Align to the ramp
                    self.y_velocity = 0
                    self.on_ground = True
                    return

        # If no collisions, player is in the air
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
        Handles the player's attack action.
        """
        self.is_attacking = keys[self.controls["attack"]]

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
        Draw the player and their health bar on the screen.
        """
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw the health bar
        health_bar_width = 50
        health_bar_height = 10
        health_ratio = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 15, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 15, health_bar_width * health_ratio, health_bar_height))

class DiagonalPlatform:
    def __init__(self, x1, y1, x2, y2):
        """
        Initialize a diagonal platform defined by two points.
        """
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.slope = (y2 - y1) / (x2 - x1)  # Calculate the slope
        self.y_intercept = y1 - self.slope * x1  # Calculate the y-intercept

    def get_y_at_x(self, x):
        """
        Get the y-coordinate on the platform for a given x-coordinate.
        """
        if not self.contains_x(x):
            return None  # Return None if x is out of bounds
        return self.slope * x + self.y_intercept

    def contains_x(self, x):
        """
        Check if the x-coordinate is within the bounds of the platform.
        """
        return self.x1 <= x <= self.x2
