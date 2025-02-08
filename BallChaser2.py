import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
BASKET_COLOR = (255, 0, 0)
BASKET_RADIUS = 40
BALL_RADIUS = 15
FONT_COLOR = (255, 255, 255)
FPS = 60
SPEED = 5
GRAVITY = 0.5

# Colors
YELLOW = (255, 255, 0)
OBJECT_COLOR = (0, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball Game")

# Load assets
font = pygame.font.Font(None, 40)

# Game Variables
score = 0
ball_x, ball_y = WIDTH // 2, HEIGHT - 50
ball_velocity = [0, 0]
basket_x = random.randint(100, WIDTH - 100)
basket_y = random.randint(100, HEIGHT - 200)
game_over = False
ball_speed = 5
basket_timer = 0
basket_move_interval = 100  # Moves every 100 frames

# Object List
objects = []

def draw_basket():
    pygame.draw.circle(screen, BASKET_COLOR, (basket_x, basket_y), BASKET_RADIUS)

def draw_ball():
    pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), BALL_RADIUS)

def draw_objects():
    for obj in objects:
        pygame.draw.rect(screen, OBJECT_COLOR, obj)

def display_score():
    score_text = font.render(f"Score: {score}", True, FONT_COLOR)
    screen.blit(score_text, (10, 10))

def move_basket():
    global basket_x, basket_y
    basket_x = random.randint(100, WIDTH - 100)
    basket_y = random.randint(100, HEIGHT - 200)

def check_collision():
    global score
    distance = math.sqrt((ball_x - basket_x) ** 2 + (ball_y - basket_y) ** 2)
    if distance < BASKET_RADIUS + BALL_RADIUS:
        score += 1
        add_object()
        move_basket()
        return True
    return False

def check_object_collision():
    global game_over
    ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
    for obj in objects:
        if ball_rect.colliderect(obj):
            game_over = True
            return True
    return False

def add_object():
    object_width = random.randint(20, 50)
    object_height = random.randint(20, 50)
    object_x = random.randint(0, WIDTH - object_width)
    object_y = random.randint(0, HEIGHT - object_height)
    new_object = pygame.Rect(object_x, object_y, object_width, object_height)
    objects.append(new_object)

def game_loop():
    global ball_x, ball_y, ball_velocity, basket_x, basket_y, game_over, basket_timer
    clock = pygame.time.Clock()

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_basket()
        draw_ball()
        draw_objects()
        display_score()

        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, FONT_COLOR)
            screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 2))
            pygame.display.update()
            waiting_for_restart()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Handle movement with arrow keys only
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ball_x -= ball_speed
        if keys[pygame.K_RIGHT]:
            ball_x += ball_speed
        if keys[pygame.K_UP]:
            ball_y -= ball_speed
        if keys[pygame.K_DOWN]:
            ball_y += ball_speed

        # Prevent the ball from leaving the screen
        ball_x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, ball_x))
        ball_y = max(BALL_RADIUS, min(HEIGHT - BALL_RADIUS, ball_y))

        # Move basket at intervals
        basket_timer += 1
        if basket_timer >= basket_move_interval:
            move_basket()
            basket_timer = 0

        # Check collisions
        check_collision()
        check_object_collision()

        pygame.display.update()
        clock.tick(FPS)

def waiting_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    global score, ball_x, ball_y, ball_velocity, game_over, objects
                    score = 0
                    ball_x, ball_y = WIDTH // 2, HEIGHT - 50
                    ball_velocity = [0, 0]
                    game_over = False
                    objects = []
                    game_loop()

if __name__ == "__main__":
    game_loop()
