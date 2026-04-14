import pygame
import sys

def drawLineBetween(screen, index, start, end, width, color_mode):
    """Рисует линию между двумя точками (для свободного рисования)"""
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    elif color_mode == 'black':
        color = (0, 0, 0)
    elif color_mode == 'yellow':
        color = (255, 255, 0)
    elif color_mode == 'purple':
        color = (255, 0, 255)
    else:  # white for eraser
        color = (255, 255, 255)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

def draw_rectangle(screen, start_pos, end_pos, color, width):
    """Рисует прямоугольник от start_pos до end_pos"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    # Определяем координаты прямоугольника (левый верхний угол, ширина, высота)
    rect_x = min(x1, x2)
    rect_y = min(y1, y2)
    rect_width = abs(x1 - x2)
    rect_height = abs(y1 - y2)
    pygame.draw.rect(screen, color, (rect_x, rect_y, rect_width, rect_height), width)

def draw_circle(screen, start_pos, end_pos, color, width):
    """Рисует круг от start_pos до end_pos (радиус = расстояние между точками)"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    # Вычисляем центр и радиус
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) // 2
    if radius > 0:  # Рисуем только если радиус положительный
        pygame.draw.circle(screen, color, (center_x, center_y), radius, width)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Рисовалка - Прямоугольники, Круги, Ластик")
    clock = pygame.time.Clock()
    
    # Переменные для рисования
    radius = 15  # Толщина кисти/ластика
    mode = 'draw'  # Режимы: 'draw', 'rect', 'circle', 'eraser'
    color_mode = 'black'  # Текущий цвет
    drawing = False  # Нажата ли кнопка мыши
    start_pos = (0, 0)  # Начальная позиция для фигур
    points = []  # Точки для свободного рисования
    
    # Цветовая палитра (кнопки выбора цвета)
    colors = {
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (255, 0, 255)
    }
    
    # Панель инструментов (простые кнопки)
    toolbar_rects = {
        'draw': pygame.Rect(10, 10, 60, 30),
        'rect': pygame.Rect(80, 10, 60, 30),
        'circle': pygame.Rect(150, 10, 60, 30),
        'eraser': pygame.Rect(220, 10, 60, 30),
        'clear': pygame.Rect(290, 10, 60, 30)
    }
    
    # Кнопки цветов
    color_rects = {}
    x_offset = 370
    for i, (color_name, color_value) in enumerate(colors.items()):
        rect = pygame.Rect(x_offset + i * 40, 10, 30, 30)
        color_rects[color_name] = rect
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            # Выход из программы
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                
                # Горячие клавиши для выбора режимов
                if event.key == pygame.K_d:
                    mode = 'draw'
                elif event.key == pygame.K_r:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                
                # Горячие клавиши для выбора цвета
                if event.key == pygame.K_1:
                    color_mode = 'black'
                elif event.key == pygame.K_2:
                    color_mode = 'red'
                elif event.key == pygame.K_3:
                    color_mode = 'green'
                elif event.key == pygame.K_4:
                    color_mode = 'blue'
                elif event.key == pygame.K_5:
                    color_mode = 'yellow'
                elif event.key == pygame.K_6:
                    color_mode = 'purple'
                
                # Изменение толщины кисти
                if event.key == pygame.K_UP:
                    radius = min(200, radius + 5)
                elif event.key == pygame.K_DOWN:
                    radius = max(1, radius - 5)
            
            # Обработка нажатий мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка
                    pos = event.pos
                    
                    # Проверяем нажатие на кнопки панели инструментов
                    for tool_name, rect in toolbar_rects.items():
                        if rect.collidepoint(pos):
                            if tool_name == 'clear':
                                # Очищаем экран
                                screen.fill((255, 255, 255))
                                points = []
                            else:
                                mode = tool_name
                            break
                    else:
                        # Проверяем нажатие на кнопки цветов
                        for color_name, rect in color_rects.items():
                            if rect.collidepoint(pos):
                                color_mode = color_name
                                break
                        else:
                            # Начало рисования на холсте
                            drawing = True
                            start_pos = event.pos
                            if mode == 'draw' or mode == 'eraser':
                                # Для свободного рисования добавляем точку
                                points = [event.pos]
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    end_pos = event.pos
                    
                    # Рисуем фигуру при отпускании кнопки
                    if mode == 'rect':
                        draw_rectangle(screen, start_pos, end_pos, colors[color_mode], radius)
                    elif mode == 'circle':
                        draw_circle(screen, start_pos, end_pos, colors[color_mode], radius)
                    elif mode == 'draw' or mode == 'eraser':
                        # Дорисовываем последний сегмент линии
                        if len(points) > 1:
                            for i in range(len(points) - 1):
                                drawLineBetween(screen, i, points[i], points[i + 1], 
                                              radius, 'white' if mode == 'eraser' else color_mode)
                    points = []  # Очищаем точки
            
            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'draw' or mode == 'eraser':
                    # Для свободного рисования добавляем точки и рисуем линии
                    position = event.pos
                    points.append(position)
                    points = points[-256:]  # Ограничиваем длину списка
                    
                    # Рисуем линию между последними двумя точками
                    if len(points) > 1:
                        drawLineBetween(screen, len(points) - 2, points[-2], points[-1], 
                                      radius, 'white' if mode == 'eraser' else color_mode)
        
        # Рисуем панель инструментов
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, 800, 50))
        
        # Рисуем кнопки режимов
        for tool_name, rect in toolbar_rects.items():
            color = (150, 150, 150) if mode == tool_name else (100, 100, 100)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            # Добавляем текст на кнопки
            font = pygame.font.Font(None, 20)
            text = font.render(tool_name[:4], True, (255, 255, 255))
            screen.blit(text, (rect.x + 5, rect.y + 5))
        
        # Рисуем кнопки цветов
        for color_name, rect in color_rects.items():
            pygame.draw.rect(screen, colors[color_name], rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            if color_mode == color_name:
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)
        
        # Отображаем текущую толщину
        font = pygame.font.Font(None, 24)
        thickness_text = font.render(f"Size: {radius}", True, (0, 0, 0))
        screen.blit(thickness_text, (600, 15))
        
        # Отображаем подсказки
        help_text = font.render("D:Draw R:Rect C:Circle E:Eraser | 1-6:Colors | UP/DOWN:Size", True, (50, 50, 50))
        screen.blit(help_text, (10, 570))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()