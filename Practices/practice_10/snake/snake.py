import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE   # 30 клеток по ширине
GRID_HEIGHT = HEIGHT // CELL_SIZE # 20 клеток по высоте
FPS = 10  # базовая скорость

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
GRAY = (128, 128, 128)

# Настройки уровней
LEVEL_UP_SCORE = 3  # каждые 3 очка — новый уровень
SPEED_INCREASE = 2  # увеличение FPS за уровень

class Snake:
    """Класс змейки"""
    def __init__(self):
        # Начальная позиция: три клетки в центре
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
                     (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                     (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # движение вправо
        self.grow = False

    def move(self):
        """Движение змейки"""
        head = self.body[0]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)
        
        # Добавляем новую голову
        self.body.insert(0, new_head)
        
        # Если не нужно расти — удаляем хвост
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        """Смена направления (нельзя поворачивать назад)"""
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def check_collision(self):
        """Проверка столкновения с собой и со стенами"""
        head = self.body[0]
        
        # Столкновение со стенами (выход за границы поля)
        if (head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        
        # Столкновение с собой (голова врезалась в тело)
        if head in self.body[1:]:
            return True
        
        return False

    def eat_food(self, food_pos):
        """Проверка, съела ли змейка еду"""
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False

    def draw(self, screen):
        """Отрисовка змейки"""
        for i, segment in enumerate(self.body):
            color = DARK_GREEN if i == 0 else GREEN  # голова темнее
            rect = (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # граница клетки

class Food:
    """Класс еды"""
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.randomize_position(snake_body)

    def randomize_position(self, snake_body):
        """Генерация случайной позиции, не на стене и не на змейке"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                self.position = (x, y)
                break

    def draw(self, screen):
        """Отрисовка еды"""
        rect = (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

def show_text(screen, text, size, x, y, color=WHITE):
    """Вспомогательная функция для отображения текста"""
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка — с уровнями и скоростью")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake.body)
    
    score = 0          # счёт (съеденная еда)
    level = 1          # начальный уровень
    current_fps = FPS  # текущая скорость

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        # Логика игры
        snake.move()

        # Проверка столкновений (стены или сама с собой)
        if snake.check_collision():
            print("Игра окончена! Счёт:", score, "Уровень:", level)
            running = False
            break

        # Проверка поедания еды
        if snake.eat_food(food.position):
            score += 1
            # Увеличение уровня при достижении порога
            if score % LEVEL_UP_SCORE == 0:
                level += 1
                current_fps = FPS + (level - 1) * SPEED_INCREASE
                print(f"Уровень {level}! Скорость увеличена до {current_fps} FPS")
            
            # Генерируем новую еду (не на змейке)
            food.randomize_position(snake.body)

        # Отрисовка
        screen.fill(BLACK)
        
        # Рисуем границы (стены) для наглядности
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT), 3)
        
        snake.draw(screen)
        food.draw(screen)
        
        # Отображение счёта и уровня
        show_text(screen, f"Score: {score}", 30, 10, 10)
        show_text(screen, f"Level: {level}", 30, WIDTH - 100, 10)
        
        pygame.display.flip()
        clock.tick(current_fps)  # скорость зависит от уровня

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()