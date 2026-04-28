import pygame
import sys
import random
from config import Settings
from db import Database

class SnakeGame:
    def __init__(self, username):
        pygame.init()
        
        self.WIDTH, self.HEIGHT = 600, 400
        self.CELL_SIZE = 20
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.YELLOW = (200, 200, 0)
        self.BLUE = (0, 0, 200)
        self.DARK_RED = (139, 0, 0)
        self.GRAY = (128, 128, 128)
        self.PURPLE = (128, 0, 128)
        self.CYAN = (0, 255, 255)
        
        self.font_large = pygame.font.SysFont("Verdana", 36)
        self.font_medium = pygame.font.SysFont("Verdana", 24)
        self.font_small = pygame.font.SysFont("Verdana", 18)
        
        # Game variables
        self.username = username
        self.settings = Settings()
        self.db = Database()
        self.personal_best = self.db.get_personal_best(username)
        
        self.reset_game()
    
    def reset_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (self.CELL_SIZE, 0)
        self.score = 0
        self.level = 1
        self.foods_to_next_level = 3
        self.speed = 12
        self.base_speed = 12
        self.obstacles = []
        
        # Power-up variables
        self.power_up = None
        self.power_up_timer = 0
        self.active_power_ups = {}
        
        # Food variables - СНАЧАЛА создаем poison_food
        self.poison_food = None  # Отдельная ядовитая еда
        self.food = self.generate_food()  # Потом генерируем обычную еду
        
        # Generate obstacles for level 3+
        if self.level >= 3:
            self.generate_obstacles()
    
    def generate_food(self):
        """Генерация только обычной еды (красная, желтая, синяя)"""
        while True:
            x = random.randint(0, (self.WIDTH - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
            y = random.randint(0, (self.HEIGHT - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
            pos = (x, y)
            
            if pos not in self.snake and pos not in self.obstacles:
                # Проверяем, чтобы не было коллизии с ядовитой едой
                if self.poison_food and pos == (self.poison_food[0], self.poison_food[1]):
                    continue
                
                # Только полезная еда
                rand = random.random()
                if rand < 0.6:  # 60% красная (+1)
                    return (x, y, 1, self.RED, "normal")
                elif rand < 0.9:  # 30% желтая (+3)
                    return (x, y, 3, self.YELLOW, "normal")
                else:  # 10% синяя (+5)
                    return (x, y, 5, self.BLUE, "normal")
    
    def generate_poison_food(self):
        """Генерация ядовитой еды как отдельного объекта"""
        # 2% шанс каждый кадр появиться, если нет ядовитой еды
        if self.poison_food is None and random.random() < 0.02:
            while True:
                x = random.randint(0, (self.WIDTH - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
                y = random.randint(0, (self.HEIGHT - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
                pos = (x, y)
                
                # Проверяем, что позиция свободна
                if (pos not in self.snake and 
                    pos not in self.obstacles and 
                    pos != (self.food[0], self.food[1])):
                    # Сохраняем время появления для таймера
                    self.poison_food = (x, y, -2, self.DARK_RED, "poison", pygame.time.get_ticks())
                    break
    
    def generate_power_up(self):
        if self.power_up is None and random.random() < 0.02:  # 2% chance per frame
            while True:
                x = random.randint(0, (self.WIDTH - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
                y = random.randint(0, (self.HEIGHT - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
                pos = (x, y)
                
                if (pos not in self.snake and 
                    pos not in self.obstacles and 
                    pos != (self.food[0], self.food[1])):
                    if self.poison_food and pos == (self.poison_food[0], self.poison_food[1]):
                        continue
                    power_type = random.choice(["speed", "slow", "shield"])
                    colors = {"speed": self.CYAN, "slow": self.PURPLE, "shield": self.YELLOW}
                    self.power_up = (pos, power_type, colors[power_type], pygame.time.get_ticks())
                    break
    
    def generate_obstacles(self):
        self.obstacles = []
        num_obstacles = min(5 + self.level, 15)
        
        for _ in range(num_obstacles):
            while True:
                x = random.randint(0, (self.WIDTH - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
                y = random.randint(0, (self.HEIGHT - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
                pos = (x, y)
                
                # Check if obstacle doesn't trap the snake
                if pos not in self.snake and pos not in self.obstacles:
                    # Check if snake has at least one adjacent free cell
                    head = self.snake[0]
                    neighbors = [
                        (head[0] + self.CELL_SIZE, head[1]),
                        (head[0] - self.CELL_SIZE, head[1]),
                        (head[0], head[1] + self.CELL_SIZE),
                        (head[0], head[1] - self.CELL_SIZE)
                    ]
                    if pos not in neighbors:
                        self.obstacles.append(pos)
                        break
    
    def draw_button(self, text, x, y, width, height, color, hover_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))
        
        text_surface = self.font_medium.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
        self.screen.blit(text_surface, text_rect)
        return False
    
    def draw_grid(self):
        if self.settings.get_grid_overlay():
            for x in range(0, self.WIDTH, self.CELL_SIZE):
                pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, self.HEIGHT))
            for y in range(0, self.HEIGHT, self.CELL_SIZE):
                pygame.draw.line(self.screen, (50, 50, 50), (0, y), (self.WIDTH, y))
    
    def draw_snake(self):
        color = self.settings.get_snake_color()
        for block in self.snake:
            pygame.draw.rect(self.screen, color, (block[0], block[1], self.CELL_SIZE, self.CELL_SIZE))
    
    def draw_food(self):
        pygame.draw.rect(self.screen, self.food[3], (self.food[0], self.food[1], self.CELL_SIZE, self.CELL_SIZE))
    
    def draw_poison_food(self):
        """Отрисовка ядовитой еды"""
        if self.poison_food:
            pygame.draw.rect(self.screen, self.poison_food[3], 
                           (self.poison_food[0], self.poison_food[1], self.CELL_SIZE, self.CELL_SIZE))
            # Добавляем белый крестик для обозначения яда
            center_x = self.poison_food[0] + self.CELL_SIZE // 2
            center_y = self.poison_food[1] + self.CELL_SIZE // 2
            pygame.draw.line(self.screen, self.WHITE, 
                           (center_x - 5, center_y - 5), 
                           (center_x + 5, center_y + 5), 2)
            pygame.draw.line(self.screen, self.WHITE, 
                           (center_x + 5, center_y - 5), 
                           (center_x - 5, center_y + 5), 2)
    
    def draw_power_up(self):
        if self.power_up:
            pygame.draw.rect(self.screen, self.power_up[2], 
                           (self.power_up[0][0], self.power_up[0][1], self.CELL_SIZE, self.CELL_SIZE))
    
    def draw_obstacles(self):
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, self.GRAY, (obs[0], obs[1], self.CELL_SIZE, self.CELL_SIZE))
    
    def check_collision(self, head):
        # Wall collision
        if head[0] < 0 or head[0] >= self.WIDTH or head[1] < 0 or head[1] >= self.HEIGHT:
            if "shield" in self.active_power_ups:
                del self.active_power_ups["shield"]
                return False
            return True
        
        # Self collision
        if head in self.snake[1:]:
            if "shield" in self.active_power_ups:
                del self.active_power_ups["shield"]
                return False
            return True
        
        # Obstacle collision
        if head in self.obstacles:
            if "shield" in self.active_power_ups:
                del self.active_power_ups["shield"]
                return False
            return True
        
        return False
    
    def apply_power_up(self, power_type):
        current_time = pygame.time.get_ticks()
        if power_type == "speed":
            self.active_power_ups["speed"] = current_time
            self.speed = self.base_speed + 5
        elif power_type == "slow":
            self.active_power_ups["slow"] = current_time
            self.speed = max(5, self.base_speed - 5)
        elif power_type == "shield":
            self.active_power_ups["shield"] = current_time
    
    def update_power_ups(self):
        current_time = pygame.time.get_ticks()
        
        # Update speed
        if "speed" in self.active_power_ups:
            if current_time - self.active_power_ups["speed"] > 5000:
                del self.active_power_ups["speed"]
                self.speed = self.base_speed
        
        if "slow" in self.active_power_ups:
            if current_time - self.active_power_ups["slow"] > 5000:
                del self.active_power_ups["slow"]
                self.speed = self.base_speed
        
        # Update power-up timer
        if self.power_up:
            if current_time - self.power_up[3] > 8000:
                self.power_up = None
    
    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, self.CELL_SIZE):
                        self.direction = (0, -self.CELL_SIZE)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -self.CELL_SIZE):
                        self.direction = (0, self.CELL_SIZE)
                    elif event.key == pygame.K_LEFT and self.direction != (self.CELL_SIZE, 0):
                        self.direction = (-self.CELL_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-self.CELL_SIZE, 0):
                        self.direction = (self.CELL_SIZE, 0)
            
            # Update power-ups
            self.update_power_ups()
            
            # Generate power-up
            self.generate_power_up()
            
            # Generate poison food (отдельно)
            self.generate_poison_food()
            
            # Update poison food timer (исчезает через 5 секунд)
            if self.poison_food:
                if pygame.time.get_ticks() - self.poison_food[5] > 5000:
                    self.poison_food = None
            
            # Move snake
            head_x, head_y = self.snake[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])
            
            # Check collision
            if self.check_collision(new_head):
                self.db.save_game_result(self.username, self.score, self.level)
                return False
            
            self.snake.insert(0, new_head)
            
            # Check food collision (обычная еда)
            food_eaten = False
            if new_head == (self.food[0], self.food[1]):
                self.score += self.food[2]
                self.foods_to_next_level -= 1
                self.food = self.generate_food()
                food_eaten = True
            
            # Check poison food collision (ядовитая еда)
            if self.poison_food and new_head == (self.poison_food[0], self.poison_food[1]):
                self.score += self.poison_food[2]  # -2 очка
                # Уменьшаем змейку на 2 сегмента
                for _ in range(2):
                    if len(self.snake) > 1:
                        self.snake.pop()
                if len(self.snake) <= 1:
                    self.db.save_game_result(self.username, self.score, self.level)
                    return False
                self.poison_food = None
                food_eaten = True
            
            # Если еда не была съедена, убираем хвост
            if not food_eaten:
                self.snake.pop()
            
            # Check power-up collision
            if self.power_up and new_head == self.power_up[0]:
                self.apply_power_up(self.power_up[1])
                self.power_up = None
            
            # Level progression
            if self.foods_to_next_level == 0:
                self.level += 1
                self.foods_to_next_level = 3
                self.base_speed += 2
                self.speed = self.base_speed
                if self.level >= 3:
                    self.generate_obstacles()
            
            # Drawing
            self.screen.fill(self.BLACK)
            self.draw_grid()
            self.draw_obstacles()
            self.draw_snake()
            self.draw_food()
            self.draw_poison_food()  # Отрисовка ядовитой еды
            self.draw_power_up()
            
            # UI Text
            score_text = self.font_small.render(f"Score: {self.score}", True, self.WHITE)
            self.screen.blit(score_text, (10, 10))
            level_text = self.font_small.render(f"Level: {self.level}", True, self.WHITE)
            self.screen.blit(level_text, (10, 35))
            best_text = self.font_small.render(f"Best: {self.personal_best}", True, self.WHITE)
            self.screen.blit(best_text, (10, 60))
            
            pygame.display.update()
            self.clock.tick(self.speed)
        
        return True