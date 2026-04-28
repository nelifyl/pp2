import pygame
import sys
import random
from config import *
from db import init_db, get_top_scores, get_all_scores
from game import run_game

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4: Snake Database Edition")

# Шрифты
font_main = pygame.font.SysFont("Verdana", 24)
font_big = pygame.font.SysFont("Verdana", 48, bold=True)
font_small = pygame.font.SysFont("Verdana", 18)

class Button:
    def __init__(self, x, y, w, h, text, color=GRAY):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=5)
        txt_img = font_main.render(self.text, True, WHITE)
        surface.blit(txt_img, txt_img.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

def draw_text(text, font, color, y_pos):
    img = font.render(text, True, color)
    screen.blit(img, img.get_rect(center=(WIDTH // 2, y_pos)))

def ask_username():
    """Экран ввода имени пользователя."""
    username = ""
    input_active = True
    
    while input_active:
        screen.fill(BLACK)
        draw_text("ENTER YOUR NAME", font_main, GREEN, 200)
        
        # Поле ввода
        input_rect = pygame.Rect(WIDTH//2 - 150, 250, 300, 50)
        pygame.draw.rect(screen, DARK_GRAY, input_rect, border_radius=5)
        
        # Текст ввода
        name_surface = font_main.render(username + ("_" if pygame.time.get_ticks() % 1000 < 500 else " "), 
                                        True, YELLOW)
        text_rect = name_surface.get_rect(center=input_rect.center)
        screen.blit(name_surface, text_rect)
        
        draw_text("Press ENTER to Start", font_small, WHITE, 350)
        draw_text("Press ESC to go back", font_small, WHITE, 380)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    return username
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 15 and event.unicode.isprintable():
                    username += event.unicode

def main_menu():
    btn_play = Button(200, 200, 200, 50, "PLAY", GREEN)
    btn_leader = Button(200, 270, 200, 50, "LEADERBOARD")
    btn_settings = Button(200, 340, 200, 50, "SETTINGS")
    btn_quit = Button(200, 410, 200, 50, "QUIT", RED)

    while True:
        screen.fill(BLACK)
        draw_text("SNAKE TSIS4", font_big, WHITE, 100)
        
        for b in [btn_play, btn_leader, btn_settings, btn_quit]: 
            b.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if btn_play.is_clicked(event):
                return "play"
            if btn_leader.is_clicked(event):
                return "leaderboard"
            if btn_settings.is_clicked(event):
                return "settings"
            if btn_quit.is_clicked(event):
                return "quit"

def leaderboard_screen():
    """Улучшенный экран лидерборда с отладкой"""
    scores = get_top_scores()
    btn_back = Button(200, 520, 200, 40, "BACK")
    btn_refresh = Button(200, 470, 200, 40, "REFRESH")
    
    # Прокрутка для длинного списка
    scroll_offset = 0
    max_visible = 10
    
    while True:
        screen.fill(BLACK)
        draw_text("TOP 10 BEST PLAYERS", font_main, YELLOW, 30)
        
        if not scores:
            draw_text("No scores yet!", font_small, WHITE, 200)
            draw_text("Play a game to save your score!", font_small, GRAY, 230)
        else:
            y = 80
            for i, (name, score, lvl, date) in enumerate(scores[:max_visible]):
                # Форматируем дату
                if date:
                    date_str = date.strftime("%d.%m %H:%M")
                else:
                    date_str = "Unknown"
                
                # Подсветка топ-3
                color = YELLOW if i == 0 else WHITE if i < 3 else GRAY
                
                # Красивое форматирование строки
                medal = ""
                if i == 0:
                    medal = "🏆 "
                elif i == 1:
                    medal = "🥈 "
                elif i == 2:
                    medal = "🥉 "
                else:
                    medal = f"{i+1}. "
                
                txt = f"{medal}{name[:15]:15} {score:4} pts  Lvl {lvl:2}"
                draw_text(txt, font_small, color, y)
                y += 35
        
        # Показываем статистику
        total_games = len(scores)
        stats_txt = f"Total games: {total_games}"
        draw_text(stats_txt, font_small, GRAY, 440)
        
        btn_refresh.draw(screen)
        btn_back.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if btn_back.is_clicked(event):
                return "menu"
            if btn_refresh.is_clicked(event):
                scores = get_top_scores()  # Обновляем данные
                print(f"Refreshed leaderboard: {len(scores)} entries")

def settings_screen():
    current = load_settings()
    btn_grid = Button(150, 200, 300, 50, f"GRID: {'ON' if current['grid'] else 'OFF'}")
    btn_color = Button(150, 270, 300, 50, "CHANGE COLOR")
    btn_back = Button(200, 400, 200, 50, "SAVE & BACK", GREEN)
    
    # Для анимации предпросмотра цвета
    color_preview = pygame.Rect(WIDTH//2 - 25, 330, 50, 50)

    while True:
        screen.fill(BLACK)
        draw_text("SETTINGS", font_main, BLUE, 100)
        
        # Предпросмотр цвета змейки
        pygame.draw.rect(screen, current['snake_color'], color_preview)
        pygame.draw.rect(screen, WHITE, color_preview, 2)
        
        for b in [btn_grid, btn_color, btn_back]: 
            b.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if btn_grid.is_clicked(event):
                current['grid'] = not current['grid']
                btn_grid.text = f"GRID: {'ON' if current['grid'] else 'OFF'}"
            if btn_color.is_clicked(event):
                current['snake_color'] = [random.randint(50, 255) for _ in range(3)]
            if btn_back.is_clicked(event):
                save_settings(current)
                return "menu"

def game_over_screen(res):
    btn_retry = Button(100, 400, 180, 50, "RETRY", GREEN)
    btn_menu = Button(320, 400, 180, 50, "MENU")

    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", font_big, RED, 150)
        draw_text(f"SCORE: {res['score']}", font_main, WHITE, 230)
        draw_text(f"LEVEL: {res['level']}", font_main, WHITE, 270)
        draw_text(f"PERSONAL BEST: {res['best']}", font_main, YELLOW, 320)
        
        btn_retry.draw(screen)
        btn_menu.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if btn_retry.is_clicked(event):
                return "retry"
            if btn_menu.is_clicked(event):
                return "menu"

def debug_database():
    """Отладочная функция для проверки БД"""
    print("\n=== DATABASE DEBUG ===")
    all_scores = get_all_scores()
    if all_scores:
        print(f"Всего записей в БД: {len(all_scores)}")
        for name, score, lvl, date in all_scores[:5]:
            print(f"  {name}: {score} очков, уровень {lvl}, {date}")
    else:
        print("Нет записей в БД")
    
    top10 = get_top_scores()
    print(f"Топ-10 записей: {len(top10)}")
    print("===================\n")

def main():
    # Инициализируем БД при запуске
    try:
        init_db()
        debug_database()  # Отладка
    except Exception as e:
        print(f"Database error: {e}")
        print("Продолжаем без сохранения результатов в БД")

    while True:
        state = main_menu()
        
        if state == "quit":
            break
        elif state == "leaderboard":
            leaderboard_screen()
        elif state == "settings":
            settings_screen()
        elif state == "play":
            user = ask_username()
            if not user:
                continue
            
            print(f"\n=== НАЧАЛО ИГРЫ для игрока: {user} ===")
            
            # Игровой цикл (retry/menu)
            while True:
                result = run_game(screen, user, load_settings())
                
                print(f"Результат игры: {result}")
                
                if result[0] == "quit":
                    pygame.quit()
                    sys.exit()
                
                if result[0] == "game_over":
                    print(f"Игра окончена! Счет: {result[1]['score']}, Уровень: {result[1]['level']}")
                    print(f"Личный рекорд: {result[1]['best']}")
                    debug_database()  # Проверяем БД после сохранения
                    
                    after_action = game_over_screen(result[1])
                    if after_action == "retry":
                        print("Повтор игры...")
                        continue
                    elif after_action == "menu":
                        print("Возврат в меню...")
                        break
                    elif after_action == "quit":
                        pygame.quit()
                        sys.exit()
                    else:
                        break
                else:
                    break

    pygame.quit()

if __name__ == "__main__":
    main()