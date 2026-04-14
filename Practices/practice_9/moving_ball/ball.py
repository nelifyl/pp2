import pygame
x, y=300, 200
radius=25
step=20
w, h=600, 400
def move(key):
    global x, y
    if key==pygame.K_LEFT and x-radius-step>=0:
        x-=step
    elif key==pygame.K_RIGHT and x+radius+step<=w:
        x+=step
    elif key==pygame.K_UP and y-radius-step>=0:
        y-=step
    elif key==pygame.K_DOWN and y+radius+step<=h:
        y+=step
def draw(screen):
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)