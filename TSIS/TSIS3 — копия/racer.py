import pygame
import random
import os
from persistence import save_score

LANES = [150, 300, 450]
WIDTH, HEIGHT = 700, 700
BASE = os.path.dirname(__file__)

def IMG(name):
    path = os.path.join(BASE, "images", name)
    if os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    
    alt_exts = [name.lower(), name.upper(), name.replace('.png','.PNG')]
    for alt in alt_exts:
        alt_path = os.path.join(BASE, "images", alt)
        if os.path.exists(alt_path):
            return pygame.image.load(alt_path).convert_alpha()
    
    print("⚠️ Image not found:", path, "-> using fallback rectangle")
    surf = pygame.Surface((80,120))
    surf.fill((255,0,255))
    return surf

class BaseSprite(pygame.sprite.Sprite):
    def move_down(self, speed):
        self.rect.y += speed

class Traffic(BaseSprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(IMG("enemy.png"), (70,120))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))

class Obstacle(BaseSprite):
    TYPES = ["pothole", "barrier"]
    def __init__(self):
        super().__init__()
        self.type = random.choice(self.TYPES)
        if self.type == "pothole":
            img = "pothole.png"
        else:
            img = "border.png"
        self.image = pygame.transform.scale(IMG(img), (50,50))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -80))

class PowerUp(BaseSprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro", "shield"])
        img = "nitro.png" if self.type == "nitro" else "shield.png"
        self.image = pygame.transform.scale(IMG(img), (50,50))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -80))

class Coin(BaseSprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(IMG("coin.png"), (40,40))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -80))

class Background:
    def __init__(self):
        self.image = pygame.transform.scale(IMG("road.png"), (WIDTH, HEIGHT))
        self.y1 = 0
        self.y2 = -HEIGHT
        self.speed = 5
        
    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        
        if self.y1 >= HEIGHT:
            self.y1 = -HEIGHT
        if self.y2 >= HEIGHT:
            self.y2 = -HEIGHT
            
    def draw(self, screen):
        screen.blit(self.image, (0, self.y1))
        screen.blit(self.image, (0, self.y2))

class RacerGame:
    def __init__(self, settings):
        self.settings = settings
        self.font = pygame.font.SysFont("Verdana", 24)
        self.background = Background()
        self.reset("Player")
        
    def apply_settings(self, settings):
        self.settings = settings
        # обновляем скорость фона в зависимости от сложности
        if settings["difficulty"] == "easy":
            self.background.speed = 3
        elif settings["difficulty"] == "hard":
            self.background.speed = 7
        else:
            self.background.speed = 5

    def reset(self, name):
        self.player_name = name
        self.player_img = pygame.transform.scale(IMG("car.png"), (70,120))
        self.player = self.player_img.get_rect(center=(350, 580))
        self.speed = 5
        self.distance = 0
        self.coins = 0
        self.active_power = None
        self.power_timer = 0
        self.traffic = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        
        # сброс фона
        self.background.y1 = 0
        self.background.y2 = -HEIGHT
        
        # устанавливаем скорость фона по сложности
        if self.settings["difficulty"] == "easy":
            self.background.speed = 3
        elif self.settings["difficulty"] == "hard":
            self.background.speed = 7
        else:
            self.background.speed = 5

    def lane_free(self, rect):
        if rect.colliderect(self.player.inflate(40,40)):
            return False
        for g in [self.traffic, self.obstacles, self.powerups, self.coins_group]:
            for obj in g:
                if rect.colliderect(obj.rect):
                    return False
        return True

    def try_spawn(self, sprite_cls, group, attempts=5):
        for _ in range(attempts):
            obj = sprite_cls()
            if self.lane_free(obj.rect):
                group.add(obj)
                return

    def spawn_objects(self):
        # частота спавна зависит от сложности
        if self.settings["difficulty"] == "easy":
            traffic_chance = 0.015
            obstacle_chance = 0.015
            coin_chance = 0.015
        elif self.settings["difficulty"] == "hard":
            traffic_chance = 0.03
            obstacle_chance = 0.03
            coin_chance = 0.01
        else:
            traffic_chance = 0.02
            obstacle_chance = 0.02
            coin_chance = 0.02
            
        if random.random() < traffic_chance:
            self.try_spawn(Traffic, self.traffic)
        if random.random() < obstacle_chance:
            self.try_spawn(Obstacle, self.obstacles)
        if random.random() < 0.01 and not self.powerups:
            self.try_spawn(PowerUp, self.powerups)
        if random.random() < coin_chance:
            self.try_spawn(Coin, self.coins_group)

    def run(self, screen):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x -= 7
        if keys[pygame.K_RIGHT]:
            self.player.x += 7
        
        # keep car on screen
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > WIDTH:
            self.player.right = WIDTH

        # обновляем фон
        self.background.update()
        
        self.spawn_objects()
        self.distance += self.speed / 10

        for group in [self.traffic, self.obstacles, self.powerups, self.coins_group]:
            for obj in group:
                obj.move_down(self.speed)
                if obj.rect.top > HEIGHT:
                    obj.kill()

        # собираем монеты
        for coin in self.coins_group:
            if coin.rect.colliderect(self.player):
                self.coins += 1
                coin.kill()

        # столкновение с врагами
        for t in self.traffic:
            if t.rect.colliderect(self.player):
                if self.active_power == "shield":
                    self.active_power = None
                    t.kill()
                else:
                    return self.finish()

        # препятствия
        for o in self.obstacles:
            if o.rect.colliderect(self.player):
                if self.active_power == "shield":
                    self.active_power = None
                    o.kill()
                    continue
                if o.type == "barrier":
                    return self.finish()
                if o.type == "pothole":
                    self.speed = max(3, self.speed - 1)
                o.kill()

        # бонусы
        for p in self.powerups:
            if p.rect.colliderect(self.player):
                self.active_power = p.type
                self.power_timer = 300
                p.kill()

        if self.active_power == "nitro":
            self.speed = 8
        if self.power_timer > 0:
            self.power_timer -= 1
        else:
            self.speed = 5
            self.active_power = None

        # отрисовка
        self.background.draw(screen)
        
        # линии дороги поверх фона (опционально)
        for lane in LANES:
            pygame.draw.line(screen, (255, 255, 255), (lane, 0), (lane, HEIGHT), 3)
        
        screen.blit(self.player_img, self.player)
        self.traffic.draw(screen)
        self.obstacles.draw(screen)
        self.powerups.draw(screen)
        self.coins_group.draw(screen)
        
        # HUD с фоном для читаемости
        hud_text = f"Distance: {int(self.distance)}m  Coins: {self.coins}  Power: {self.active_power or 'None'}"
        hud_surface = self.font.render(hud_text, True, (255, 255, 255))
        
        # добавляем полупрозрачный фон для текста
        text_rect = hud_surface.get_rect(topleft=(10, 10))
        pygame.draw.rect(screen, (0, 0, 0, 128), text_rect.inflate(10, 5))
        
        screen.blit(hud_surface, (10, 10))
        
        pygame.display.update()
        return None

    def finish(self):
        """Игра окончена - сохраняем результат в БД"""
        score = int(self.distance * 10 + self.coins * 20)
        save_score(self.player_name, score, int(self.distance), self.coins)
        return {"score": score, "distance": int(self.distance), "coins": self.coins}