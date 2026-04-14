import pygame
from ball import move, draw
pygame.init()
screen=pygame.display.set_mode((600, 400))
clock=pygame.time.Clock()
r=True
while r:
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            r=False
        elif i.type==pygame.KEYDOWN:
            move(i.key)
    draw(screen)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()