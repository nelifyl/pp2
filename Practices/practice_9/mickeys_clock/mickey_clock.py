import pygame
import datetime

l_hand = pygame.image.load("images/left_hand.png")
r_hand = pygame.image.load("images/right_hand.png")
mickey = pygame.image.load("images/mickey.png")

center = (300, 300)

def update_angles():
    now = datetime.datetime.now()
    sec = now.second * 6          # 6 градусов на секунду
    minute = now.minute * 6        # 6 градусов на минуту
    # Добавляем -90 градусов чтобы стрелка указывала на 12 часов
    return -sec - 90, -minute - 90  # Возвращаем оба угла

def draw_clock(screen, sec_angle, min_angle):
    screen.blit(mickey, mickey.get_rect(center=center))
    
    sec_hand = pygame.transform.rotate(l_hand, sec_angle)
    screen.blit(sec_hand, sec_hand.get_rect(center=center))
    
    min_hand = pygame.transform.rotate(r_hand, min_angle)
    screen.blit(min_hand, min_hand.get_rect(center=center))