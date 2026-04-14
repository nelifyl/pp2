# Импорт необходимых библиотек
import pygame
import sys
import random
import time
import os
from pygame.locals import *

# Устанавливаем правильную рабочую директорию
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Рабочая директория: {os.getcwd()}")

# Инициализация Pygame
pygame.init()

# Настройка частоты кадров (FPS)
FPS = 60
FramePerSec = pygame.time.Clock()

# Определение цветов в формате RGB
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Константы экрана и игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 2          # Начальная скорость врага
COINS_COLLECTED = 0 # Счётчик собранных монет

# Коэффициент уменьшения размера (чем меньше число, тем меньше объект)
SCALE_FACTOR = 0.125  # Уменьшаем в 2 раза (0.5 = 50% от оригинального размера)

# Настройка шрифтов для отображения текста
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Проверяем существование папки images
if not os.path.exists("images"):
    print("ОШИБКА: Папка 'images' не найдена!")
    print(f"Текущая директория: {os.getcwd()}")
    print("Файлы в директории:", os.listdir('.'))
    sys.exit()

print("Файлы в папке images:", os.listdir("images"))

# Функция для загрузки и масштабирования изображений
def load_and_scale_image(path, scale):
    """Загружает изображение и масштабирует его"""
    try:
        original_image = pygame.image.load(path)
        # Получаем оригинальный размер
        original_width = original_image.get_width()
        original_height = original_image.get_height()
        # Вычисляем новый размер
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        # Масштабируем изображение
        scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
        print(f"Загружено {path}: {original_width}x{original_height} -> {new_width}x{new_height}")
        return scaled_image
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None

# Загрузка и масштабирование изображений
background = pygame.image.load("images/road.png")     # Фон не масштабируем
player_img = load_and_scale_image("images/car1.png", SCALE_FACTOR)    # Уменьшенная машина игрока
enemy_img = load_and_scale_image("images/car2.png", SCALE_FACTOR)     # Уменьшенная вражеская машина
coin_img = load_and_scale_image("images/coin.png", SCALE_FACTOR)      # Уменьшенная монета

# Проверка, что все изображения загружены
if None in [player_img, enemy_img, coin_img]:
    print("Ошибка: не удалось загрузить некоторые изображения")
    sys.exit()

print("Все изображения загружены и масштабированы успешно!")

# Создание окна игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer - Collect Coins!")


class Enemy(pygame.sprite.Sprite):
    """
    Класс вражеского автомобиля.
    Двигается сверху вниз с увеличивающейся скоростью.
    """
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        # Случайное начальное положение по горизонтали, сверху экрана
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Перемещает врага вниз. Если враг ушёл за экран, возрождает его сверху."""
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    """
    Класс игрока (машина игрока).
    Управляется стрелками влево/вправо, не может выйти за границы экрана.
    """
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Фиксированное положение по вертикали внизу

    def move(self):
        """Обрабатывает нажатия клавиш и перемещает игрока."""
        pressed_keys = pygame.key.get_pressed()
        # Движение влево с проверкой границы
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        # Движение вправо с проверкой границы
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    """
    Класс монеты, которую собирает игрок.
    Появляется в случайном месте дороги.
    """
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        # Случайное появление монеты на дороге (с отступами от краёв)
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-100, -40)  # Появляется сверху за экраном
        )

    def move(self):
        """
        Перемещает монету вниз.
        Если монета уходит за экран, она возрождается в новом случайном месте.
        """
        self.rect.move_ip(0, SPEED - 2)  # Монета движется чуть медленнее врага
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

    def respawn(self):
        """Возрождает монету в случайном месте сверху."""
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-100, -40)
        )


# Создание объектов игрока, врага и монеты
P1 = Player()
E1 = Enemy()
coin = Coin()

# Создание групп спрайтов для удобного управления
enemies = pygame.sprite.Group()
enemies.add(E1)

coins_group = pygame.sprite.Group()
coins_group.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin)

# Пользовательское событие для увеличения скорости врага каждую секунду
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# --- Основной игровой цикл ---
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5   # Плавное увеличение сложности
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона (дороги)
    DISPLAYSURF.blit(background, (0, 0))

    # Отображение текущего количества собранных монет в правом верхнем углу
    coin_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    text_width = coin_text.get_width()
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - text_width - 10, 10))

    # Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # --- Проверка сбора монет ---
    if pygame.sprite.collide_rect(P1, coin):
        COINS_COLLECTED += 1
        coin.respawn()  # Возрождаем монету в новом месте

    # --- Проверка столкновения с врагом (конец игры) ---
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)  # Небольшая пауза для эффекта

        # Отображение экрана "Game Over"
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        # Также показываем финальный счёт монет
        final_score_text = font_small.render(f"Coins collected: {COINS_COLLECTED}", True, BLACK)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
        DISPLAYSURF.blit(final_score_text, final_score_rect)
        pygame.display.update()

        # Удаляем все спрайты и ждём перед выходом
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Обновление экрана и тактирование
    pygame.display.update()
    FramePerSec.tick(FPS)