import time
import pygame
import random

from Pong_Game.game import ball, player
from Pong_Game.game.countdown import score
from Pong_Game.game.setup import screen_width, screen_height, bg_color, light_grey, diamonds, countdown_font, screen, \
    diamond_icon


def ball_start():
    global ball_speed_x, ball_speed_y, respawn_counter, collision_counter, playing, start_time

    ball.center = (screen_width / 2, screen_height - 200)
    ball_speed_y *= -1
    ball_speed_x *= random.choice((1, -1))
    player.center = (screen_width / 2, screen_height - 20)

    if respawn_counter > 0:
        countdown()


def countdown():
    global playing, start_time
    for i in range(3, 0, -1):
        screen.fill(bg_color)
        score()
        # Ball und Spieler zeichnen
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.ellipse(screen, light_grey, ball)
        # Diamanten zeichnen
        for diamond in diamonds:
            screen.blit(diamond_icon, diamond)
        # Countdown anzeigen
        countdown_text = countdown_font.render(str(i), True, light_grey)
        countdown_text_rect = countdown_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(countdown_text, countdown_text_rect)
        if i < 3:
            pygame.time.delay(1000)

        pygame.display.flip()

    playing = True
    start_time = time.time()  # Startzeit festlegen

