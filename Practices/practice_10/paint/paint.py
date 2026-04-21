import pygame
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))
    radius = 10
    mode = "brush"
    color = (0, 0, 255)
    drawing = False
    start_pos = None
    last_pos = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_1:
                    mode = "brush"
                elif event.key == pygame.K_2:
                    mode = "rect"
                elif event.key == pygame.K_3:
                    mode = "circle"
                elif event.key == pygame.K_4:
                    mode = "eraser"
                elif event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos
                    if mode == "rect":
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(canvas, color, rect, 2)
                    elif mode == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, 2)
            if event.type == pygame.MOUSEMOTION:
                if drawing and (mode == "brush" or mode == "eraser"):
                    draw_color = (0, 0, 0) if mode == "eraser" else color
                    pygame.draw.line(canvas, draw_color, last_pos, event.pos, radius)
                    last_pos = event.pos
        screen.fill((0, 0, 0))
        screen.blit(canvas, (0, 0))
        pygame.display.flip()
        clock.tick(60)
main()