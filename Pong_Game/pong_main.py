import pygame
import sys
import time
from game.setup import *
from game.ball import ball_animation
from game.player import player_animation
from game.collision import ball_start, respawn_counter
from game.score import score, basic_font, endscreen_font, countdown_font, score_font
from game.countdown import countdown
from game.diamond import spawn_diamonds



# Countdown beim Spielstart anzeigen
countdown()
spawn_diamonds()

while running:

    pygame.display.set_caption("Pong Singleplayer - Playing" if playing else "Pong Singleplayer - Paused")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 10
            if event.key == pygame.K_RIGHT:
                player_speed += 10
            if event.key == pygame.K_SPACE:  # Hier innerhalb der Ereignisschleife prüfen
                playing = not playing  # Pausieren oder Fortsetzen des Spiels

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 10
            if event.key == pygame.K_RIGHT:
                player_speed -= 10
            if event.key == pygame.K_n and not playing and respawn_counter == 0:
                # Starte ein neues Spiel
                ball = pygame.Rect(screen_width / 2 - 15, screen_height - 200, 30, 30)
                respawn_counter = life
                collision_counter = 0
                diamond_counter = 0
                d_treffer_pro_level_counter = 0
                level = 1
                start_time = None  # Zurücksetzen der Startzeit für den Timer
                playing = True
                countdown()
                spawn_diamonds()

    if respawn_counter <= 0:
        respawn_counter = 0
        playing = False

    # Game Logic
    if playing:  # Führe Spiellogik nur aus, wenn das Spiel aktiv ist
        ball_animation()
        player_animation()

    # Visuals
    screen.fill(bg_color)

    # Diamanten zeichnen
    for diamond in diamonds:
        screen.blit(diamond_icon, diamond)

    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, red, (0, screen_height - 100), (screen_width, screen_height - 100))

    # Score und Timer anzeigen
    score()

    # Spielzeit anzeigen, wenn das Spiel läuft und start_time definiert ist
    if playing and start_time is not None:
        elapsed_time = round(time.time() - start_time)
        time_text = basic_font.render(f'Time: {elapsed_time}', True, light_grey)
        screen.blit(time_text, (10, 70))

    pygame.display.flip()
    clock.tick(60)
