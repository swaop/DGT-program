import pygame  # Ensure that pygame is imported correctly
import sys

# Initialize Pygame
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
        self.jump_strength = 16  # Jump height
        self.gravity = 1
        self.velocity_y = 0  # Start with no vertical velocity
        self.on_ground = False

    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity
            
        # Update vertical position
        self.rect.y += self.velocity_y
        
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # Move left
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:  # Move right
            self.rect.x += self.speed
            
        # Jumping logic
        if keys[pygame.K_UP] and self.on_ground:  # Jump only when on ground
            self.velocity_y = -self.jump_strength
            self.on_ground = False  # Player is no longer on ground after jump

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))  # Create platform surface
        self.image.fill((0, 0, 0))  # Color the platform black
        self.rect = self.image.get_rect(topleft=(x, y))  # Position the platform

class Level:
    def __init__(self, level_number):
        self.player = Player()
        self.red_cube = pygame.Surface((30, 30))  # Create a red square as the finish line
        self.red_cube.fill((255, 0, 0))  # Color the red cube
        self.level_number = level_number
        
        # Platforms Group
        self.platforms = pygame.sprite.Group()
        self.create_platforms()  # Initial platform creation
        
        # Position the red cube
        self.position_red_cube()

    def create_platforms(self):
        platform_height = 20
        platform_width = 100  # Fixed width for horizontal platforms
        vertical_platform_width = 20  # Width for vertical platforms

        # Adding a base platform at the bottom where the player spawns
        base_platform = Platform(0, HEIGHT - platform_height, WIDTH, platform_height)
        self.platforms.add(base_platform)  # Add the base platform to the platforms group

        # Define specific platform layouts for each level
        layout = {
            1: [
                (400, 500, platform_width),  # Near bottom center, first step
                (600, 400, platform_width),  # First step to the right
                (700, 300, platform_width),  # Close to the right edge
                (600, 190, vertical_platform_width)  # Vertical path up
            ],
            2: [
                (50, 500, platform_width),    # Base platform for left
                (250, 450, platform_width),   # Mid platform
                (300, 300, platform_width),   # Above the last
                (100, 200, vertical_platform_width),  # Vertical path back to left
                (10, 10, vertical_platform_width)  # Final position of red cube
            ],
            3: [
                (400, 500, platform_width),  # Base near the middle
                (200, 400, platform_width),  # First step up
                (400, 300, platform_width),  # Second step up
                (600, 200, platform_width),  # Towards higher right
                (WIDTH - 40, 100, platform_width)  # Final push to the top right
            ], 
            4: [
                (100, 500, platform_width),   # Base platform on the left
                (250, 400, platform_width),   # Mid-left step
                (400, 300, platform_width),   # Mid-right step higher up
                (600, 400, platform_width),   # Higher platform towards the right
                (WIDTH - 200, 250, platform_width),  # Near the top right corner
                (WIDTH - 130, 150, platform_width)   # Final push to reach the red cube
            ],
            5: [
                (400, 500, platform_width),  # Central base platform
                (600, 400, platform_width),  # Move upwards on the right
                (700, 300, platform_width),  # Step further upwards on right
                (800 - 100, 200, vertical_platform_width),  # Vertical elevator
                (WIDTH - 40, 10, platform_width)  # Final push to the top right
            ]
        }

        # Create platforms based on the assigned layout
        for (x, y, width) in layout[self.level_number]:
            if width == platform_width:
                platform = Platform(x, y, platform_width, platform_height)
            else:  # vertical platform
                platform = Platform(x, y, vertical_platform_width, platform_height)
            self.platforms.add(platform)

    def position_red_cube(self):
        # Position the red cube based on the level number
        if self.level_number in [1, 3, 5]:  # Levels 1, 3, 5
            self.red_cube_rect = self.red_cube.get_rect(topright=(WIDTH - 10, 10))  # Top right corner
        else:  # Levels 2, 4
            self.red_cube_rect = self.red_cube.get_rect(topleft=(10, 10))  # Top left corner

    def update(self):
        self.player.update()

        # Reset on_ground flag
        self.player.on_ground = False  # Assume the player is not on the ground

        # Check for collision with platforms
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity_y >= 0:  # Only align when falling
                    self.player.rect.bottom = platform.rect.top  # Place player on top of the platform
                    self.player.on_ground = True  # Player is on the ground
                    self.player.velocity_y = 0  # Reset vertical velocity
                break  # Stop checking after the first collision

        # Check if the player falls below the ground level
        if self.player.rect.y >= HEIGHT - 50:  # Assuming ground level
            self.player.rect.y = HEIGHT - 50
            self.player.on_ground = True
            self.player.velocity_y = 0
            
        # Check for collision with the red cube
        if self.player.rect.colliderect(self.red_cube_rect):
            return True  # Indicate that the level is completed
        return False

    def draw(self, window, elapsed_time):
        window.blit(background_image, (0, 0))  # Draw the background
        window.blit(self.red_cube, self.red_cube_rect)  # Draw the red cube
        window.blit(self.player.image, self.player.rect)  # Draw the player
        
        # Draw the platforms
        for platform in self.platforms:
            window.blit(platform.image, platform.rect)

        # Display the current level in the top right corner
        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f'Level: {self.level_number}', True, (255, 255, 255))
        window.blit(level_text, (WIDTH - 150, 10))  # Draw level text

        # Display the timer in the top left corner
        timer_text = font.render(f'Time: {elapsed_time // 1000}', True, (255, 255, 255))  # Convert ms to seconds
        window.blit(timer_text, (10, 10))  # Draw the timer text

# Game loop
running = True
level_number = 1
level = Level(level_number)

start_time = pygame.time.get_ticks()  # Start the timer

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
            level = Level(level_number)  # Move to the next level

    elapsed_time = pygame.time.get_ticks() - start_time  # Calculate elapsed time

    level.draw(window, elapsed_time)  # Pass elapsed time to draw function
    pygame.display.flip()

    # Frame Rate cap
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()