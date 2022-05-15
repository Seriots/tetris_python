import pygame
import os
from game import Game
from windows import Menu, Leaderboard, GameOver, Pause

pygame.init()

pygame.display.set_caption("Tetris")  # la base
screen_size = 580, 1000


screen = pygame.display.set_mode(screen_size)

all_windows = {'game': Game(20, screen_size), 'menu': Menu(screen_size), 'leaderboard': Leaderboard(screen_size), 'gameover': GameOver(screen_size), 'pause': Pause(screen_size)}
window = all_windows['menu']
window_pause = all_windows['pause']
pause = False
running = True
while running:

    window.update(screen)
    running = window.running

    if window != all_windows[window.window]:
        new_window = window.window
        window_before = window
        window = all_windows[new_window]
        window.window = new_window

        if window.window_name == 'pause':
            window.window_before = window_before.window_name

        if window.window_name == 'gameover':
            window.last_puntos = all_windows['game'].puntos

        if window_before.window_name != 'pause' and window.window == 'game':
            window.reset()

    if not running:
        pygame.quit()
        print("Fermeture")
