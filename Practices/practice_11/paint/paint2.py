import pygame
import math  # Добавляем math для тригонометрических расчётов

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))
    
    # Параметры рисования
    radius = 10
    mode = "brush"          # Текущий режим: brush, rect, circle, eraser, square, right_triangle, equilateral_triangle, rhombus
    color = (0, 0, 255)     # Цвет по умолчанию - синий
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
                
                # Выбор режимов рисования
                if event.key == pygame.K_1:
                    mode = "brush"
                elif event.key == pygame.K_2:
                    mode = "rect"
                elif event.key == pygame.K_3:
                    mode = "circle"
                elif event.key == pygame.K_4:
                    mode = "eraser"
                elif event.key == pygame.K_5:
                    mode = "square"           # Квадрат
                elif event.key == pygame.K_6:
                    mode = "right_triangle"   # Прямоугольный треугольник
                elif event.key == pygame.K_7:
                    mode = "equilateral_triangle"  # Равносторонний треугольник
                elif event.key == pygame.K_8:
                    mode = "rhombus"          # Ромб
                
                # Выбор цвета
                elif event.key == pygame.K_r:
                    color = (255, 0, 0)       # Красный
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)       # Зелёный
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)       # Синий
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)   # Белый
                elif event.key == pygame.K_k:
                    color = (0, 0, 0)         # Чёрный (для ластика)
            
            # Нажатие кнопки мыши - начало рисования фигуры
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
            
            # Отпускание кнопки мыши - завершение рисования фигуры
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos
                    
                    # Рисование прямоугольника
                    if mode == "rect":
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(canvas, color, rect, 2)
                    
                    # Рисование круга
                    elif mode == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, 2)
                    
                    # Рисование квадрата (ширина = высоте)
                    elif mode == "square":
                        width = end_pos[0] - start_pos[0]
                        height = end_pos[1] - start_pos[1]
                        size = max(abs(width), abs(height))  # Берём максимальную сторону
                        if width < 0:
                            size = -size
                        rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
                        pygame.draw.rect(canvas, color, rect, 2)
                    
                    # Рисование прямоугольного треугольника
                    elif mode == "right_triangle":
                        # Треугольник с прямым углом между start_pos и end_pos
                        points = [
                            start_pos,
                            (end_pos[0], start_pos[1]),  # Точка по горизонтали
                            end_pos
                        ]
                        pygame.draw.polygon(canvas, color, points, 2)
                    
                    # Рисование равностороннего треугольника
                    elif mode == "equilateral_triangle":
                        # Вычисляем сторону и высоту
                        side = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
                        height = side * math.sqrt(3) / 2
                        
                        # Находим центр отрезка между start и end
                        center_x = (start_pos[0] + end_pos[0]) / 2
                        center_y = (start_pos[1] + end_pos[1]) / 2
                        
                        # Вектор направления
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        
                        # Перпендикулярный вектор (поворот на 90 градусов)
                        perp_x = -dy
                        perp_y = dx
                        
                        # Нормализуем перпендикуляр
                        length = math.hypot(perp_x, perp_y)
                        if length != 0:
                            perp_x /= length
                            perp_y /= length
                        
                        # Вершина треугольника (третья точка)
                        third_x = center_x + perp_x * height
                        third_y = center_y + perp_y * height
                        
                        points = [start_pos, end_pos, (third_x, third_y)]
                        pygame.draw.polygon(canvas, color, points, 2)
                    
                    # Рисование ромба
                    elif mode == "rhombus":
                        # Центр ромба - середина между start и end
                        center_x = (start_pos[0] + end_pos[0]) / 2
                        center_y = (start_pos[1] + end_pos[1]) / 2
                        
                        # Половина диагоналей
                        dx = (end_pos[0] - start_pos[0]) / 2
                        dy = (end_pos[1] - start_pos[1]) / 2
                        
                        # 4 вершины ромба
                        points = [
                            (center_x, center_y - dy),  # Верхняя
                            (center_x + dx, center_y),  # Правая
                            (center_x, center_y + dy),  # Нижняя
                            (center_x - dx, center_y)   # Левая
                        ]
                        pygame.draw.polygon(canvas, color, points, 2)
            
            # Рисование кистью или ластиком при движении мыши
            if event.type == pygame.MOUSEMOTION:
                if drawing and (mode == "brush" or mode == "eraser"):
                    draw_color = (0, 0, 0) if mode == "eraser" else color
                    pygame.draw.line(canvas, draw_color, last_pos, event.pos, radius)
                    last_pos = event.pos
        
        # Отрисовка экрана
        screen.fill((0, 0, 0))
        screen.blit(canvas, (0, 0))
        pygame.display.flip()
        clock.tick(60)

main()