import pygame
from persistence import load_scores, save_settings, get_all_scores

class MainMenu:
    def __init__(self): 
        self.name = "Player"
        self.font = pygame.font.SysFont("Verdana", 40)
        self.small_font = pygame.font.SysFont("Verdana", 24)
        
    def get_name(self): 
        return self.name
        
    def run(self, screen):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: 
                    pygame.quit(); exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN: 
                        return "play"
                    elif e.key == pygame.K_UP:
                        return "leaderboard"
                    elif e.key == pygame.K_DOWN:
                        return "settings"
                    elif e.key == pygame.K_ESCAPE:
                        return "quit"
            
            screen.fill((30, 30, 30))
            title = self.font.render("RACER TSIS3", True, (255, 255, 0))
            play_txt = self.small_font.render("ENTER - Play", True, (255, 255, 255))
            lb_txt = self.small_font.render("UP - Leaderboard", True, (255, 255, 255))
            set_txt = self.small_font.render("DOWN - Settings", True, (255, 255, 255))
            quit_txt = self.small_font.render("ESC - Quit", True, (255, 255, 255))
            
            screen.blit(title, (200, 150))
            screen.blit(play_txt, (250, 300))
            screen.blit(lb_txt, (240, 350))
            screen.blit(set_txt, (240, 400))
            screen.blit(quit_txt, (250, 450))
            
            pygame.display.update()


class NameInputScreen:
    def __init__(self):
        self.font = pygame.font.SysFont("Verdana", 36)
        self.small_font = pygame.font.SysFont("Verdana", 24)
        
    def run(self, screen):
        name = ""
        active = True
        
        while active:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN and name.strip():
                        return name.strip()
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif e.key == pygame.K_ESCAPE:
                        return None
                    elif len(name) < 20 and e.unicode.isprintable():
                        name += e.unicode
            
            screen.fill((30, 30, 30))
            
            prompt = self.font.render("Enter Your Name:", True, (255, 255, 255))
            name_text = self.font.render(name + "_", True, (255, 255, 0))
            info = self.small_font.render("Press ENTER to start, ESC to cancel", True, (150, 150, 150))
            
            screen.blit(prompt, (200, 250))
            screen.blit(name_text, (200, 320))
            screen.blit(info, (150, 450))
            
            pygame.display.update()


class LeaderboardScreen:
    def run(self, screen):
        all_scores = get_all_scores()  # получаем все результаты из БД
        font = pygame.font.SysFont("Verdana", 24)
        title_font = pygame.font.SysFont("Verdana", 36)
        
        scroll_offset = 0
        max_scroll = max(0, len(all_scores) - 12) * 28
        
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN:
                        return
                    if e.key == pygame.K_DOWN:
                        scroll_offset = min(max_scroll, scroll_offset + 28)
                    if e.key == pygame.K_UP:
                        scroll_offset = max(0, scroll_offset - 28)
            
            screen.fill((0, 0, 0))
            
            title = title_font.render("LEADERBOARD", True, (255, 255, 0))
            screen.blit(title, (220, 20))
            
            # заголовки таблицы
            headers = ["#", "Name", "Score", "Distance", "Coins"]
            colors = [(200,200,200), (255,215,0), (192,192,192), (205,127,50)]
            
            for i, header in enumerate(headers):
                x = 50 + i * 120
                text = font.render(header, True, (255, 255, 255))
                screen.blit(text, (x, 80))
            
            y = 120
            for idx, score in enumerate(all_scores):
                y_pos = y + idx * 28 - scroll_offset
                if 100 < y_pos < 650:  # только видимые строки
                    color = colors[idx] if idx < 4 else (255, 255, 255)
                    
                    rank_text = font.render(str(idx + 1), True, color)
                    name_text = font.render(score['name'][:15], True, color)
                    score_text = font.render(str(score['score']), True, color)
                    dist_text = font.render(str(score['distance']), True, color)
                    coin_text = font.render(str(score['coins']), True, color)
                    
                    screen.blit(rank_text, (55, y_pos))
                    screen.blit(name_text, (160, y_pos))
                    screen.blit(score_text, (280, y_pos))
                    screen.blit(dist_text, (400, y_pos))
                    screen.blit(coin_text, (520, y_pos))
            
            info = pygame.font.SysFont("Verdana", 18).render("UP/DOWN to scroll, ESC to return", True, (150,150,150))
            screen.blit(info, (200, 660))
            
            pygame.display.update()


class SettingsScreen:
    def __init__(self, settings):
        self.settings = settings
        self.font = pygame.font.SysFont("Verdana", 28)
        self.selected = 0
        self.options = ["Difficulty", "Sound", "Back"]
        self.difficulties = ["easy", "normal", "hard"]
        
    def run(self, screen):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        save_settings(self.settings)
                        return self.settings
                    if e.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    if e.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    if e.key == pygame.K_RIGHT:
                        if self.selected == 0:  # Difficulty
                            idx = self.difficulties.index(self.settings["difficulty"])
                            idx = (idx + 1) % len(self.difficulties)
                            self.settings["difficulty"] = self.difficulties[idx]
                        elif self.selected == 1:  # Sound
                            self.settings["sound"] = not self.settings["sound"]
                    if e.key == pygame.K_LEFT:
                        if self.selected == 0:  # Difficulty
                            idx = self.difficulties.index(self.settings["difficulty"])
                            idx = (idx - 1) % len(self.difficulties)
                            self.settings["difficulty"] = self.difficulties[idx]
                        elif self.selected == 1:  # Sound
                            self.settings["sound"] = not self.settings["sound"]
                    if e.key == pygame.K_RETURN and self.selected == 2:
                        save_settings(self.settings)
                        return self.settings
            
            screen.fill((30, 30, 30))
            
            title = self.font.render("SETTINGS", True, (255, 255, 0))
            screen.blit(title, (260, 100))
            
            for i, option in enumerate(self.options):
                y = 200 + i * 60
                color = (255, 255, 0) if i == self.selected else (255, 255, 255)
                
                if i == 0:  # Difficulty
                    value = self.settings["difficulty"].upper()
                    text = self.font.render(f"{option}: {value}", True, color)
                elif i == 1:  # Sound
                    value = "ON" if self.settings["sound"] else "OFF"
                    text = self.font.render(f"{option}: {value}", True, color)
                else:
                    text = self.font.render(option, True, color)
                
                screen.blit(text, (200, y))
            
            info = pygame.font.SysFont("Verdana", 18).render("ARROWS to change, ENTER/ESC to save", True, (150,150,150))
            screen.blit(info, (180, 650))
            
            pygame.display.update()


class GameOverScreen:
    def __init__(self):
        self.res = None
        self.font = pygame.font.SysFont("Verdana", 48)
        self.small_font = pygame.font.SysFont("Verdana", 28)
        
    def set_result(self, res):
        self.res = res
        
    def run(self, screen):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return "menu"
                    if e.key == pygame.K_SPACE:
                        return "restart"
            
            screen.fill((0, 0, 0))
            
            game_over = self.font.render("GAME OVER", True, (255, 0, 0))
            score_txt = self.small_font.render(f"Score: {self.res['score']}", True, (255, 255, 255))
            dist_txt = self.small_font.render(f"Distance: {self.res['distance']}m", True, (255, 255, 255))
            coins_txt = self.small_font.render(f"Coins: {self.res['coins']}", True, (255, 255, 0))
            restart_txt = self.small_font.render("SPACE - Restart", True, (150, 150, 150))
            menu_txt = self.small_font.render("ENTER - Menu", True, (150, 150, 150))
            
            screen.blit(game_over, (180, 150))
            screen.blit(score_txt, (260, 280))
            screen.blit(dist_txt, (250, 330))
            screen.blit(coins_txt, (270, 380))
            screen.blit(restart_txt, (210, 480))
            screen.blit(menu_txt, (220, 520))
            
            pygame.display.update()