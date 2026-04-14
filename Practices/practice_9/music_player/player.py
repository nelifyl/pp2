import pygame
import os
from typing import List

class MusicPlayer:
    def __init__(self, music_folder=None):
        # Путь к папке music
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if music_folder is None:
            self.music_folder = os.path.join(current_dir, "music")
        else:
            self.music_folder = music_folder
        
        self.playlist: List[str] = []
        self.current_track_index = 0
        self.is_playing = False
        self.is_paused = False
        
        # Загружаем треки
        self.load_playlist()
        
        # Инициализация звука
        pygame.mixer.init()
    
    def load_playlist(self):
        """Загружает все WAV файлы из папки music"""
        if os.path.exists(self.music_folder):
            for file in os.listdir(self.music_folder):
                if file.lower().endswith(('.wav', '.mp3', '.ogg')):
                    self.playlist.append(os.path.join(self.music_folder, file))
        
        if not self.playlist:
            print("Нет аудиофайлов в папке 'music'")
    
    def play(self):
        """Воспроизводит трек"""
        if not self.playlist:
            return
            
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            track_path = self.playlist[self.current_track_index]
            try:
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Ошибка: {e}")
                return
        
        self.is_playing = True
    
    def stop(self):
        """Останавливает"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
    
    def pause(self):
        """Пауза"""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
    
    def next_track(self):
        """Следующий трек"""
        if not self.playlist:
            return
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.play()
    
    def previous_track(self):
        """Предыдущий трек"""
        if not self.playlist:
            return
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play()
    
    def get_current_track_name(self):
        """Имя текущего трека"""
        if not self.playlist:
            return "No tracks"
        return os.path.basename(self.playlist[self.current_track_index])
    
    def get_playlist_info(self):
        """Список треков"""
        if not self.playlist:
            return []
        
        result = []
        for i, track in enumerate(self.playlist):
            name = os.path.basename(track)
            if i == self.current_track_index:
                result.append(f"> {name}")
            else:
                result.append(f"  {name}")
        return result