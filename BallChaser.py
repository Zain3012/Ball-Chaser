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

# Colors
WHITE = (255, 255, 255)
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
basket_y = 100
game_over = False
gravity = 0.5
ball_speed = 5

# Object List (for objects added when scoring)
objects = []


# Functions
def draw_basket():
    pygame.draw.circle(screen, BASKET_COLOR, (basket_x, basket_y), BASKET_RADIUS)


def draw_ball(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), BALL_RADIUS)


def draw_objects():
    for obj in objects:
        pygame.draw.rect(screen, OBJECT_COLOR, obj)


def display_score():
    score_text = font.render(f"Score: {score}", True, FONT_COLOR)
    screen.blit(score_text, (10, 10))


def check_collision():
    global score
    distance = math.sqrt((ball_x - basket_x) ** 2 + (ball_y - basket_y) ** 2)
    if distance < BASKET_RADIUS + BALL_RADIUS:
        score += 1
        # Add a new object when a point is scored
        add_object()
        return True
    return False


def check_object_collision():
    global game_over
    ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
    for obj in objects:
        if ball_rect.colliderect(obj):  # Check if the ball collides with any object
            game_over = True
            return True
    return False


def add_object():
    # Add a new random object to the list
    object_width = random.randint(20, 50)
    object_height = random.randint(20, 50)
    object_x = random.randint(0, WIDTH - object_width)
    object_y = random.randint(0, HEIGHT - object_height)
    new_object = pygame.Rect(object_x, object_y, object_width, object_height)
    objects.append(new_object)


def game_loop():
    global ball_x, ball_y, ball_velocity, basket_x, basket_y, game_over
    clock = pygame.time.Clock()

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_basket()
        draw_ball(ball_x, ball_y)
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
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:  # shoot the ball
                    ball_velocity = [random.randint(-5, 5), -10]

        # Move the ball with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ball_x -= ball_speed
        if keys[pygame.K_RIGHT]:
            ball_x += ball_speed
        if keys[pygame.K_UP]:
            ball_y -= ball_speed
        if keys[pygame.K_DOWN]:
            ball_y += ball_speed

        # Prevent the ball from moving outside the screen
        if ball_x <= BALL_RADIUS:
            ball_x = BALL_RADIUS
        if ball_x >= WIDTH - BALL_RADIUS:
            ball_x = WIDTH - BALL_RADIUS
        if ball_y <= BALL_RADIUS:
            ball_y = BALL_RADIUS
        if ball_y >= HEIGHT - BALL_RADIUS:
            ball_y = HEIGHT - BALL_RADIUS

        # Apply gravity to the ball when it's not moving upwards
        if ball_velocity[1] < 0:
            ball_velocity[1] += gravity  # Apply gravity only if the ball is not being shot upwards

        # Move the ball with velocity
        ball_x += ball_velocity[0]
        ball_y += ball_velocity[1]

        # Check for wall collisions
        if ball_x <= BALL_RADIUS or ball_x >= WIDTH - BALL_RADIUS:
            ball_velocity[0] = -ball_velocity[0]  # Bounce off walls

        if ball_y <= BALL_RADIUS:
            ball_velocity[1] = -ball_velocity[1]  # Bounce off ceiling

        # If the ball falls to the ground
        if ball_y >= HEIGHT - BALL_RADIUS:
            ball_y = HEIGHT - BALL_RADIUS
            ball_velocity = [0, 0]
            if not game_over:
                game_over = True  # Game over if the ball hits the ground

        # Check basket collision
        if check_collision():
            basket_x = random.randint(100, WIDTH - 100)  # Randomize basket position

        # Check if the ball touches any object
        if check_object_collision():
            game_over = True

        pygame.display.update()
        clock.tick(FPS)


def waiting_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    global score, ball_x, ball_y, ball_velocity, game_over, objects
                    score = 0
                    ball_x, ball_y = WIDTH // 2, HEIGHT - 50
                    ball_velocity = [0, 0]
                    game_over = False
                    objects = []  # Clear the objects list when restarting
                    game_loop()


if __name__ == "__main__":
    game_loop()
