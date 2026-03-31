import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Colors
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

# Game variables
gravity = 0.5
jump_strength = -8
pipe_speed = 3
pipe_gap = 180
pipe_spacing = 280

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.vel_y = 0
        self.width = 30
        self.height = 30
        
    def jump(self):
        self.vel_y = jump_strength
        
    def update(self):
        self.vel_y += gravity
        self.y += self.vel_y
        
    def draw(self):
        # Draw bird as a yellow rectangle (easier to see)
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
        # Draw eye
        pygame.draw.circle(screen, BLACK, (self.x + 25, self.y + 10), 3)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 70
        self.gap_y = random.randint(150, SCREEN_HEIGHT - pipe_gap - 150)
        self.passed = False
        
    def update(self):
        self.x -= pipe_speed
        
    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, self.gap_y - 30, self.width + 10, 30))
        
        # Bottom pipe
        bottom_y = self.gap_y + pipe_gap
        pygame.draw.rect(screen, GREEN, (self.x, bottom_y, self.width, SCREEN_HEIGHT - bottom_y))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, bottom_y, self.width + 10, 30))
        
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        bottom_rect = pygame.Rect(self.x, self.gap_y + pipe_gap, self.width, SCREEN_HEIGHT)
        return top_rect, bottom_rect

def show_start_screen():
    screen.fill(SKY_BLUE)
    
    title = font.render("FLAPPY BIRD", True, WHITE)
    start = small_font.render("Press SPACE to Start", True, WHITE)
    controls = small_font.render("Press SPACE to Fly", True, WHITE)
    
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    # Draw a bird as example
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 50, 30, 30))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

def show_game_over(score):
    game_over = font.render("GAME OVER", True, WHITE)
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    restart = small_font.render("Press SPACE to Restart", True, WHITE)
    
    screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

def main():
    # Show start screen
    if not show_start_screen():
        return
    
    # Initialize game objects
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0
    running = True
    
    # Game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        
        # Update bird
        bird.update()
        
        # Update pipes and add new ones
        for pipe in pipes:
            pipe.update()
        
        # Add new pipe when last pipe is halfway across screen
        if pipes[-1].x < SCREEN_WIDTH - pipe_spacing:
            pipes.append(Pipe(SCREEN_WIDTH))
        
        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]
        
        # Check collisions
        bird_rect = bird.get_rect()
        
        # Check boundaries
        if bird.y <= 0 or bird.y + bird.height >= SCREEN_HEIGHT:
            if not show_game_over(score):
                running = False
            else:
                # Reset game
                bird = Bird()
                pipes = [Pipe(SCREEN_WIDTH + 100)]
                score = 0
                continue
        
        # Check pipe collisions
        for pipe in pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                if not show_game_over(score):
                    running = False
                else:
                    # Reset game
                    bird = Bird()
                    pipes = [Pipe(SCREEN_WIDTH + 100)]
                    score = 0
                    continue
            
            # Update score
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1
        
        # Draw everything
        screen.fill(SKY_BLUE)
        
        # Draw pipes
        for pipe in pipes:
            pipe.draw()
        
        # Draw bird
        bird.draw()
        
        # Draw score
        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 20, 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()