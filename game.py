import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Player settings
PLAYER_SIZE = 30
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 15
GRAVITY = 0.8

# Game settings
COLLECTIBLE_SIZE = 20
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 40
SPAWN_RATE = 0.02

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.color = BLUE
        
    def update(self, keys, obstacles):
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x *= 0.8  # Friction
            
        # Jumping
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = -PLAYER_JUMP_POWER
            self.on_ground = False
            
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        new_x = self.x + self.vel_x
        new_y = self.y + self.vel_y
        
        # Check horizontal collision
        if not self.check_collision(new_x, self.y, obstacles):
            self.x = new_x
        else:
            self.vel_x = 0
            
        # Check vertical collision
        if not self.check_collision(self.x, new_y, obstacles):
            self.y = new_y
            self.on_ground = False
        else:
            if self.vel_y > 0:  # Falling
                self.on_ground = True
            self.vel_y = 0
            
        # Keep player on screen
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
    def check_collision(self, x, y, obstacles):
        player_rect = pygame.Rect(x, y, self.width, self.height)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.rect):
                return True
        return False
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw eyes
        eye_size = 4
        pygame.draw.circle(screen, WHITE, (self.x + 8, self.y + 8), eye_size)
        pygame.draw.circle(screen, WHITE, (self.x + 22, self.y + 8), eye_size)
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y + 8), eye_size // 2)
        pygame.draw.circle(screen, BLACK, (self.x + 22, self.y + 8), eye_size // 2)

class Collectible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = COLLECTIBLE_SIZE
        self.height = COLLECTIBLE_SIZE
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = YELLOW
        self.collected = False
        self.animation_offset = 0
        
    def update(self):
        self.animation_offset = (self.animation_offset + 0.2) % (2 * math.pi)
        
    def draw(self, screen):
        if not self.collected:
            # Animated collectible
            bounce = math.sin(self.animation_offset) * 3
            pygame.draw.circle(screen, self.color, 
                             (self.x + self.width // 2, self.y + self.height // 2 + bounce), 
                             self.width // 2)
            # Sparkle effect
            sparkle_size = 2
            pygame.draw.circle(screen, WHITE, 
                             (self.x + 5, self.y + 5), sparkle_size)
            pygame.draw.circle(screen, WHITE, 
                             (self.x + 15, self.y + 10), sparkle_size)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = RED
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Adventure Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.collectibles = []
        self.obstacles = []
        self.score = 0
        self.lives = 3
        
        # Spawn initial collectibles
        for _ in range(5):
            self.spawn_collectible()
            
        # Spawn initial obstacles
        for _ in range(3):
            self.spawn_obstacle()
            
        # Font
        self.font = pygame.font.Font(None, 36)
        
    def spawn_collectible(self):
        x = random.randint(0, SCREEN_WIDTH - COLLECTIBLE_SIZE)
        y = random.randint(50, SCREEN_HEIGHT - COLLECTIBLE_SIZE - 50)
        self.collectibles.append(Collectible(x, y))
        
    def spawn_obstacle(self):
        x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        y = random.randint(50, SCREEN_HEIGHT - OBSTACLE_HEIGHT - 50)
        width = random.randint(OBSTACLE_WIDTH, OBSTACLE_WIDTH * 2)
        height = random.randint(OBSTACLE_HEIGHT, OBSTACLE_HEIGHT * 2)
        self.obstacles.append(Obstacle(x, y, width, height))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()
                    
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.obstacles)
        
        # Update collectibles
        for collectible in self.collectibles:
            collectible.update()
            
        # Check collisions with collectibles
        for collectible in self.collectibles[:]:
            if not collectible.collected and self.player.check_collision(
                collectible.x, collectible.y, [collectible]):
                collectible.collected = True
                self.score += 10
                self.collectibles.remove(collectible)
                # Spawn new collectible
                if random.random() < 0.7:
                    self.spawn_collectible()
                    
        # Check collisions with obstacles
        for obstacle in self.obstacles:
            if self.player.check_collision(obstacle.x, obstacle.y, [obstacle]):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                else:
                    # Reset player position
                    self.player.x = SCREEN_WIDTH // 2
                    self.player.y = SCREEN_HEIGHT - 100
                    self.player.vel_x = 0
                    self.player.vel_y = 0
                    
        # Randomly spawn new obstacles
        if random.random() < SPAWN_RATE:
            self.spawn_obstacle()
            
        # Remove obstacles that are off-screen
        self.obstacles = [obs for obs in self.obstacles if obs.x > -obs.width]
        
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.player.draw(self.screen)
        
        for collectible in self.collectibles:
            collectible.draw(self.screen)
            
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        
        # Draw instructions
        instructions = [
            "Use WASD or Arrow Keys to move",
            "Space to jump",
            "Collect yellow items",
            "Avoid red obstacles",
            "R to restart, ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 120 + i * 25))
            
        pygame.display.flip()
        
    def game_over(self):
        game_over_text = self.font.render("GAME OVER!", True, RED)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press R to restart or ESC to quit", True, WHITE)
        
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(final_score_text, 
                        (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
                        
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.collectibles = []
        self.obstacles = []
        self.score = 0
        self.lives = 3
        
        for _ in range(5):
            self.spawn_collectible()
            
        for _ in range(3):
            self.spawn_obstacle()
            
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
