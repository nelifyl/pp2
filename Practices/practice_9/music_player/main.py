import pygame
import sys
from player import MusicPlayer

# Константы
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (30, 30, 40)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (100, 200, 100)
FPS = 30

class MusicPlayerApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Music Player")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        self.player = MusicPlayer()
        self.running = True
        
    def draw_ui(self):
        """Отрисовывает интерфейс"""
        self.screen.fill(BACKGROUND_COLOR)
        
        # Заголовок
        title = self.font.render("MUSIC PLAYER", True, HIGHLIGHT_COLOR)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
        
        # Текущий трек
        track_text = f"Track: {self.player.get_current_track_name()}"
        track_surface = self.font.render(track_text, True, TEXT_COLOR)
        self.screen.blit(track_surface, (50, 80))
        
        # Статус
        if self.player.is_playing:
            status = "Status: PLAYING"
            status_color = HIGHLIGHT_COLOR
        elif self.player.is_paused:
            status = "Status: PAUSED"
            status_color = (200, 200, 100)
        else:
            status = "Status: STOPPED"
            status_color = (150, 150, 150)
        
        status_surface = self.font.render(status, True, status_color)
        self.screen.blit(status_surface, (50, 130))
        
        # Плейлист
        playlist_y = 190
        playlist_title = self.small_font.render("Playlist:", True, HIGHLIGHT_COLOR)
        self.screen.blit(playlist_title, (50, playlist_y))
        
        playlist_info = self.player.get_playlist_info()
        for i, track in enumerate(playlist_info):
            if i < 5:
                track_surface = self.small_font.render(track, True, TEXT_COLOR)
                self.screen.blit(track_surface, (70, playlist_y + 25 + i * 25))
        
        # Управление
        controls_y = SCREEN_HEIGHT - 100
        controls = [
            "P - Play/Pause",
            "S - Stop",
            "N - Next",
            "B - Previous",
            "Q - Quit"
        ]
        
        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, TEXT_COLOR)
            self.screen.blit(control_surface, (50, controls_y + i * 22))
        
        pygame.display.flip()
    
    def handle_events(self):
        """Обрабатывает нажатия клавиш"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Play/Pause
                    if not self.player.is_playing and not self.player.is_paused:
                        self.player.play()
                    elif self.player.is_paused:
                        self.player.play()
                    elif self.player.is_playing:
                        self.player.pause()
                
                elif event.key == pygame.K_s:  # Stop
                    self.player.stop()
                
                elif event.key == pygame.K_n:  # Next
                    self.player.next_track()
                
                elif event.key == pygame.K_b:  # Previous
                    self.player.previous_track()
                
                elif event.key == pygame.K_q:  # Quit
                    self.running = False
                
                elif event.key == pygame.K_ESCAPE:  # ESC тоже выход
                    self.running = False
    
    def run(self):
        """Главный цикл"""
        while self.running:
            self.handle_events()
            self.draw_ui()
            self.clock.tick(FPS)
        
        self.player.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = MusicPlayerApp()
    app.run()