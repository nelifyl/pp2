import pygame
import datetime
import sys

# Загрузка изображений
l_hand = pygame.image.load("images/left_hand.png")
r_hand = pygame.image.load("images/right_hand.png")
mickey = pygame.image.load("images/mickey.png")

# Масштабируем под размер окна
l_hand = pygame.transform.scale(l_hand, (150, 150))
r_hand = pygame.transform.scale(r_hand, (150, 150))
mickey = pygame.transform.scale(mickey, (400, 400))

center = (400, 400)  # Центр для окна 800x800

def update_angles():
    now = datetime.datetime.now()
    sec = now.second * 6
    minute = now.minute * 6
    # Возвращаем углы с коррекцией для 12 часов
    return -sec - 90, -minute - 90

def draw_clock(screen, sec_angle, min_angle):
    # Очищаем экран
    screen.fill((255, 255, 255))
    
    # Рисуем лицо Микки
    screen.blit(mickey, mickey.get_rect(center=center))
    
    # Рисуем левую руку (секунды)
    sec_hand = pygame.transform.rotate(l_hand, sec_angle)
    screen.blit(sec_hand, sec_hand.get_rect(center=center))
    
    # Рисуем правую руку (минуты)
    min_hand = pygame.transform.rotate(r_hand, min_angle)
    screen.blit(min_hand, min_hand.get_rect(center=center))
    
    # Цифровое время
    font = pygame.font.Font(None, 36)
    now = datetime.datetime.now()
    time_text = font.render(f"{now.minute:02d}:{now.second:02d}", True, (0, 0, 0))
    screen.blit(time_text, (center[0] - 50, center[1] + 200))

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Часы Микки Мауса")
clock = pygame.time.Clock()

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Получаем углы
    sec_angle, min_angle = update_angles()
    
    # Рисуем часы
    draw_clock(screen, sec_angle, min_angle)
    
    # Обновляем экран
    pygame.display.flip()
    
    # Обновляем каждую секунду
    clock.tick(1)

pygame.quit()
sys.exit()