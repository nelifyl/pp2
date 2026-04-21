import pygame
import sys
import random
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
font = pygame.font.SysFont("Verdana", 24)
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
def generate_food():
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)
food = generate_food()
score = 0
level = 1
foods_to_next_level = 3
speed = 12
def draw_snake():
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL_SIZE, CELL_SIZE))
def draw_food():
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
def check_wall_collision(head):
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    return False
def check_self_collision(head):
    if head in snake[1:]:
        return True
    return False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    if check_wall_collision(new_head):
        print("Game Over: Wall Collision")
        pygame.quit()
        sys.exit()
    if check_self_collision(new_head):
        print("Game Over: Self Collision")
        pygame.quit()
        sys.exit()
    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        foods_to_next_level -= 1
        food = generate_food()
    else:
        snake.pop()
    if foods_to_next_level == 0:
        level += 1
        foods_to_next_level = 3
        speed += 2
    screen.fill(BLACK)
    draw_snake()
    draw_food()
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (10, 40))
    pygame.display.update()
    clock.tick(speed)