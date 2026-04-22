import pygame
import sys
import random
import os
from pygame.locals import *

pygame.init()

# ================= ПУТИ К ФАЙЛАМ =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# ================= НАСТРОЙКИ =================
FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

font = pygame.font.SysFont("Verdana", 30)

score = 0
coins_collected = 0
speed = 5


# ================= ENEMY =================
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(IMAGES_DIR, "enemy.png"))
        self.image = pygame.transform.smoothscale(img, (90, 140))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -150

    def move(self):
        global score, speed
        self.rect.move_ip(0, speed)

        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            speed += 0.2
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ================= PLAYER =================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(IMAGES_DIR, "car.png"))
        self.image = pygame.transform.smoothscale(img, (90, 140))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-7, 0)

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(7, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ================= COIN =================
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(IMAGES_DIR, "coin.png"))
        self.base_image = pygame.transform.smoothscale(img, (40, 40))
        self.reset()

    def reset(self):
        # случайная позиция
        self.rect = self.base_image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-300, -50)

        # случайная ценность монеты (1–3)
        self.value = random.randint(1, 3)

        # делаем размер монеты зависимым от ценности
        size = 30 + self.value * 10   # 40 / 50 / 60 px
        self.image = pygame.transform.smoothscale(self.base_image, (size, size))
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ================= СОЗДАЕМ ОБЪЕКТЫ =================
P1 = Player()
E1 = Enemy()
C1 = Coin()


# ================= GAME LOOP =================
while True:

    # события
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # обновление
    P1.update()
    E1.move()
    C1.move()

    # столкновение с врагом
    if pygame.sprite.collide_rect(P1, E1):
        text = font.render("GAME OVER", True, BLACK)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        DISPLAYSURF.blit(text, rect)
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # сбор монет
    if pygame.sprite.collide_rect(P1, C1):
        coins_collected += C1.value   # добавляем ценность монеты
        C1.reset()

    # рисование
    DISPLAYSURF.fill(GRAY)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    C1.draw(DISPLAYSURF)

    score_text = font.render(f"Score: {score}", True, WHITE)
    coin_text = font.render(f"Coins: {coins_collected}", True, WHITE)

    DISPLAYSURF.blit(score_text, (20, 20))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 200, 20))

    pygame.display.update()
    FramePerSec.tick(FPS)