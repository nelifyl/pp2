import pygame
import sys
from game import SnakeGame
from db import Database

class MainMenu:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 400
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (50, 50, 200)
        self.GREEN = (50, 200, 50)
        self.RED = (200, 50, 50)
        self.GRAY = (100, 100, 100)
        self.YELLOW = (200, 200, 50)
        
        self.font_title = pygame.font.SysFont("Verdana", 48)
        self.font_medium = pygame.font.SysFont("Verdana", 32)
        self.font_small = pygame.font.SysFont("Verdana", 24)
        
        self.db = Database()
        self.username = ""
        self.input_active = False
        self.current_screen = "menu"  # menu, leaderboard, settings, game_over
        
    def draw_button(self, text, x, y, width, height, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if click[0] == 1 and action:
                action()
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))
        
        text_surface = self.font_small.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
        self.screen.blit(text_surface, text_rect)
    
    def draw_settings_button(self):
        """Маленькая квадратная кнопка настроек в правом нижнем углу"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        btn_size = 40
        btn_x = self.WIDTH - btn_size - 10
        btn_y = self.HEIGHT - btn_size - 10
        
        # Иконка шестеренки
        if btn_x + btn_size > mouse[0] > btn_x and btn_y + btn_size > mouse[1] > btn_y:
            pygame.draw.rect(self.screen, self.YELLOW, (btn_x, btn_y, btn_size, btn_size), border_radius=5)
            if click[0] == 1:
                self.show_settings()
        else:
            pygame.draw.rect(self.screen, self.GRAY, (btn_x, btn_y, btn_size, btn_size), border_radius=5)
        
        # Рисуем простую иконку шестеренки
        pygame.draw.circle(self.screen, self.WHITE, (btn_x + btn_size//2, btn_y + btn_size//2), 8, 2)
        pygame.draw.circle(self.screen, self.WHITE, (btn_x + btn_size//2, btn_y + btn_size//2), 4)
    
    def main_menu(self):
        self.current_screen = "menu"
        
        while self.current_screen == "menu":
            self.screen.fill(self.BLACK)
            
            # Title
            title = self.font_title.render("SNAKE GAME", True, self.GREEN)
            title_rect = title.get_rect(center=(self.WIDTH/2, 60))
            self.screen.blit(title, title_rect)
            
            # Username input
            input_box = pygame.Rect(self.WIDTH/2 - 150, 120, 300, 40)
            color = self.GREEN if self.input_active else self.GRAY
            pygame.draw.rect(self.screen, color, input_box, 2)
            
            username_text = self.font_small.render(self.username if self.username else "Enter username", True, self.WHITE)
            self.screen.blit(username_text, (input_box.x + 5, input_box.y + 10))
            
            # Buttons
            play_btn = pygame.Rect(self.WIDTH/2 - 100, 190, 200, 50)
            leaderboard_btn = pygame.Rect(self.WIDTH/2 - 100, 260, 200, 50)
            quit_btn = pygame.Rect(self.WIDTH/2 - 100, 330, 200, 50)
            
            self.draw_button("PLAY", play_btn.x, play_btn.y, play_btn.width, play_btn.height, self.BLUE, (100, 100, 255), self.start_game)
            self.draw_button("LEADERBOARD", leaderboard_btn.x, leaderboard_btn.y, leaderboard_btn.width, leaderboard_btn.height, self.GREEN, (100, 255, 100), self.show_leaderboard)
            
            if self.username:
                self.draw_button("QUIT", quit_btn.x, quit_btn.y, quit_btn.width, quit_btn.height, self.RED, (255, 100, 100), self.quit_game)
            
            # Маленькая кнопка настроек в правом нижнем углу
            self.draw_settings_button()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        if len(self.username) < 20:
                            self.username += event.unicode
            
            pygame.display.update()
            self.clock.tick(60)
    
    def start_game(self):
        if self.username:
            game = SnakeGame(self.username)
            game_over = game.game_loop()
            if game_over:
                self.show_game_over(game.score, game.level)
    
    def show_game_over(self, score, level):
        self.current_screen = "game_over"
        personal_best = self.db.get_personal_best(self.username)
        
        while self.current_screen == "game_over":
            self.screen.fill(self.BLACK)
            
            # Game over text
            game_over_text = self.font_title.render("GAME OVER", True, self.RED)
            game_over_rect = game_over_text.get_rect(center=(self.WIDTH/2, 80))
            self.screen.blit(game_over_text, game_over_rect)
            
            # Stats
            score_text = self.font_medium.render(f"Final Score: {score}", True, self.WHITE)
            score_rect = score_text.get_rect(center=(self.WIDTH/2, 160))
            self.screen.blit(score_text, score_rect)
            
            level_text = self.font_medium.render(f"Level Reached: {level}", True, self.WHITE)
            level_rect = level_text.get_rect(center=(self.WIDTH/2, 200))
            self.screen.blit(level_text, level_rect)
            
            best_text = self.font_medium.render(f"Personal Best: {personal_best}", True, self.GREEN)
            best_rect = best_text.get_rect(center=(self.WIDTH/2, 240))
            self.screen.blit(best_text, best_rect)
            
            # Buttons
            retry_btn = pygame.Rect(self.WIDTH/2 - 100, 300, 200, 50)
            menu_btn = pygame.Rect(self.WIDTH/2 - 100, 360, 200, 50)
            
            # Временно сохраняем username для retry
            current_username = self.username
            
            def retry_action():
                game = SnakeGame(current_username)
                game_over = game.game_loop()
                if game_over:
                    self.show_game_over(game.score, game.level)
            
            def menu_action():
                self.current_screen = "menu"
            
            self.draw_button("RETRY", retry_btn.x, retry_btn.y, retry_btn.width, retry_btn.height, self.GREEN, (100, 255, 100), retry_action)
            self.draw_button("MAIN MENU", menu_btn.x, menu_btn.y, menu_btn.width, menu_btn.height, self.BLUE, (100, 100, 255), menu_action)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
            
            pygame.display.update()
            self.clock.tick(60)
    
    def show_leaderboard(self):
        self.current_screen = "leaderboard"
        top_scores = self.db.get_top_scores()
        
        while self.current_screen == "leaderboard":
            self.screen.fill(self.BLACK)
            
            title = self.font_title.render("LEADERBOARD", True, self.GREEN)
            title_rect = title.get_rect(center=(self.WIDTH/2, 50))
            self.screen.blit(title, title_rect)
            
            # Table headers
            headers = ["Rank", "Username", "Score", "Level", "Date"]
            x_positions = [50, 120, 280, 380, 460]
            for i, header in enumerate(headers):
                text = self.font_small.render(header, True, self.WHITE)
                self.screen.blit(text, (x_positions[i], 100))
            
            # Table rows
            y = 140
            for i, score in enumerate(top_scores[:10], 1):
                username, score_val, level, date = score
                date_str = date.strftime("%Y-%m-%d")
                
                texts = [str(i), username[:15], str(score_val), str(level), date_str]
                for j, text in enumerate(texts):
                    color = self.GREEN if j == 2 else self.WHITE
                    text_surface = self.font_small.render(text, True, color)
                    self.screen.blit(text_surface, (x_positions[j], y))
                y += 30
                if y > 350:
                    break
            
            # Back button
            back_btn = pygame.Rect(self.WIDTH/2 - 60, 360, 120, 30)
            
            def back_action():
                self.current_screen = "menu"
            
            self.draw_button("BACK", back_btn.x, back_btn.y, back_btn.width, back_btn.height, self.GRAY, (150, 150, 150), back_action)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
            
            pygame.display.update()
            self.clock.tick(60)
    
    def show_settings(self):
        self.current_screen = "settings"
        from config import Settings
        settings = Settings()
        
        colors = [(0, 200, 0), (255, 100, 100), (100, 100, 255), (255, 255, 100)]
        color_names = ["Green", "Red", "Blue", "Yellow"]
        selected_color = 0
        
        # Find current color index
        current_color = settings.get_snake_color()
        for i, color in enumerate(colors):
            if color == current_color:
                selected_color = i
                break
        
        grid_on = settings.get_grid_overlay()
        sound_on = settings.get_sound()
        
        while self.current_screen == "settings":
            self.screen.fill(self.BLACK)
            
            title = self.font_title.render("SETTINGS", True, self.GREEN)
            title_rect = title.get_rect(center=(self.WIDTH/2, 50))
            self.screen.blit(title, title_rect)
            
            # Snake color selection
            color_text = self.font_medium.render("Snake Color:", True, self.WHITE)
            self.screen.blit(color_text, (50, 120))
            
            for i, (color, name) in enumerate(zip(colors, color_names)):
                color_rect = pygame.Rect(250 + i * 80, 120, 50, 30)
                pygame.draw.rect(self.screen, color, color_rect)
                if i == selected_color:
                    pygame.draw.rect(self.screen, self.WHITE, color_rect, 3)
                
                if color_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    selected_color = i
                    settings.set_snake_color(colors[selected_color])
            
            # Grid toggle
            grid_btn = pygame.Rect(self.WIDTH/2 - 100, 180, 200, 40)
            grid_color = self.GREEN if grid_on else self.GRAY
            grid_text = "Grid: ON" if grid_on else "Grid: OFF"
            
            def toggle_grid():
                nonlocal grid_on
                grid_on = not grid_on
                settings.set_grid_overlay(grid_on)
            
            self.draw_button(grid_text, grid_btn.x, grid_btn.y, grid_btn.width, grid_btn.height, grid_color, (100, 255, 100), toggle_grid)
            
            # Sound toggle
            sound_btn = pygame.Rect(self.WIDTH/2 - 100, 240, 200, 40)
            sound_color = self.GREEN if sound_on else self.GRAY
            sound_text = "Sound: ON" if sound_on else "Sound: OFF"
            
            def toggle_sound():
                nonlocal sound_on
                sound_on = not sound_on
                settings.set_sound(sound_on)
            
            self.draw_button(sound_text, sound_btn.x, sound_btn.y, sound_btn.width, sound_btn.height, sound_color, (100, 255, 100), toggle_sound)
            
            # Save and back button
            save_btn = pygame.Rect(self.WIDTH/2 - 60, 320, 120, 40)
            
            def save_and_back():
                self.current_screen = "menu"
            
            self.draw_button("SAVE", save_btn.x, save_btn.y, save_btn.width, save_btn.height, self.BLUE, (100, 100, 255), save_and_back)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
            
            pygame.display.update()
            self.clock.tick(60)
    
    def quit_game(self):
        self.db.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    menu = MainMenu()
    menu.main_menu()