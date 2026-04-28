import pygame
from racer import RacerGame
from ui import MainMenu, LeaderboardScreen, SettingsScreen, GameOverScreen, NameInputScreen
from persistence import load_settings

pygame.init()
SCREEN = pygame.display.set_mode((700,700))
pygame.display.set_caption("Racer TSIS3")
clock = pygame.time.Clock()

settings = load_settings()
state = "menu"
player_name = "Player"
game = RacerGame(settings)

menu = MainMenu()
leaderboard = LeaderboardScreen()
settings_screen = SettingsScreen(settings)
over = GameOverScreen()
name_input = NameInputScreen()

while True:
    if state == "menu":
        action = menu.run(SCREEN)
        if action == "play":
            state = "get_name"
        elif action == "leaderboard": 
            state = "leaderboard"
        elif action == "settings": 
            state = "settings"
        elif action == "quit": 
            pygame.quit(); exit()

    elif state == "get_name":
        player_name = name_input.run(SCREEN)
        if player_name:  # если имя введено
            game.reset(player_name)
            state = "game"
        else:  # если нажали ESC
            state = "menu"

    elif state == "game":
        result = game.run(SCREEN)
        if result:
            over.set_result(result)
            state = "gameover"

    elif state == "leaderboard": 
        leaderboard.run(SCREEN)
        state = "menu"
        
    elif state == "settings": 
        settings = settings_screen.run(SCREEN)
        game.apply_settings(settings)
        state = "menu"
        
    elif state == "gameover": 
        state = "menu" if over.run(SCREEN)=="menu" else "game"

    clock.tick(60)