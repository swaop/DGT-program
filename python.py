import pygame
import sys

# Installing Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platformer')

# Load and resize the background image
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Create a black square as the player
        self.image.fill((0, 0, 0))  # Color the player black
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)  # Start position

        # Player attributes
        self.speed = 5
        self.jump_strength = 15
        self.gravity = 1
        self.velocity_y = 1
        self.on_ground = False

    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Ground collision
        if self.rect.y >= HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.on_ground = True
            self.velocity_y = 1

        # movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # Move left
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:  # Move right
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.on_ground:  # Jump
            self.velocity_y = -self.jump_strength
            self.on_ground = False

class Level:
    def __init__(self, level_number):
        self.player = Player()
        self.red_cube = pygame.Surface((30, 30))  # Create a red square as the finish line
        self.red_cube.fill((255, 0, 0))  # Color the red cube
        self.red_cube_rect = self.red_cube.get_rect()
        self.red_cube_rect.bottomleft = (WIDTH - 40, HEIGHT - 40)  # Position the red cube in the bottom right corner
        self.level_number = level_number

    def update(self):
        self.player.update()

        # Check for collision with the red cube
        if self.player.rect.colliderect(self.red_cube_rect):
            return True  # Indicate that the level is completed
        return False

    def draw(self, window):
        window.blit(background_image, (0, 0))  # Draw the background
        window.blit(self.red_cube, self.red_cube_rect)  # Draw the red cube
        window.blit(self.player.image, self.player.rect)  # Draw the player
        # Display the current level in the top right corner
        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f'Level: {self.level_number}', True, (255, 255, 255))
        window.blit(level_text, (WIDTH - 150, 10))  # Draw level text

# Game loop
running = True
level_number = 1
level = Level(level_number)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if the level is completed
    if level.update():
        level_number += 1
        if level_number > 5:  # Only 5 levels
            print("You've completed all levels!")
            running = False
        else:
            level = Level(level_number)  # code to move to the next level

    level.draw(window)
    pygame.display.flip()

    # Frame Rate cap
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()