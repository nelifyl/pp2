import json
import pygame

class Settings:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.default_settings = {
            "snake_color": [0, 200, 0],
            "grid_overlay": False,
            "sound": True
        }
        self.load_settings()
    
    def load_settings(self):
        try:
            with open(self.filename, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = self.default_settings.copy()
            self.save_settings()
    
    def save_settings(self):
        with open(self.filename, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get_snake_color(self):
        return tuple(self.settings["snake_color"])
    
    def set_snake_color(self, color):
        self.settings["snake_color"] = list(color)
        self.save_settings()
    
    def get_grid_overlay(self):
        return self.settings["grid_overlay"]
    
    def set_grid_overlay(self, value):
        self.settings["grid_overlay"] = value
        self.save_settings()
    
    def get_sound(self):
        return self.settings["sound"]
    
    def set_sound(self, value):
        self.settings["sound"] = value
        self.save_settings()