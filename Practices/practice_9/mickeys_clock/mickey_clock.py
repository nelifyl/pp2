import pygame
import datetime
import os

# Получаем путь к папке mickeys_clock
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, "mickeys_clock", "images")

# Проверяем, существует ли папка
if not os.path.exists(images_dir):
    # Если нет, пробуем другой путь
    images_dir = os.path.join(current_dir, "images")

print(f"Загрузка изображений из: {images_dir}")

# Загружаем изображения
l_hand = pygame.image.load(os.path.join(images_dir, "left_hand.png"))
r_hand = pygame.image.load(os.path.join(images_dir, "right_hand.png"))
mickey = pygame.image.load(os.path.join(images_dir, "mickey.png"))

center = (300, 300)

def update_angles():
    now = datetime.datetime.now()
    sec = now.second * 6
    minute = now.minute * 6
    return -sec - 90, -minute - 90

def draw_clock(screen, sec_angle, min_angle):
    screen.blit(mickey, mickey.get_rect(center=center))
    
    sec_hand = pygame.transform.rotate(l_hand, sec_angle)
    screen.blit(sec_hand, sec_hand.get_rect(center=center))
    
    min_hand = pygame.transform.rotate(r_hand, min_angle)
    screen.blit(min_hand, min_hand.get_rect(center=center))

# Запуск часов
def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        sec_angle, min_angle = update_angles()
        draw_clock(screen, sec_angle, min_angle)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()