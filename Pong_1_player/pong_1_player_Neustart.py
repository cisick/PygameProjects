import pygame
import random
import sys


def ball_animation():
    global ball_speed_x, ball_speed_y, collision_counter, respawn_counter

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height:
        respawn_counter -= 1
        ball_start()
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    if ball.colliderect(player):
        ball_speed_y *= -1
        # ball_speed_x *= -1
        collision_counter += 1


def player_animation():
    player.x += player_speed

    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width


def ball_start():
    global ball_speed_x, ball_speed_y, respawn_counter, collision_counter, playing
    ball.center = (screen_width / 2, screen_height - 200)
    ball_speed_y *= -1
    ball_speed_x *= random.choice((1, -1))
    player.center = (screen_width / 2, screen_height - 20)
    if respawn_counter > 0:
        countdown()


def score():
    # Laden der Bilder für die Symbole
    gefangene_baelle_icon = pygame.image.load('gefangene_baelle_01.png')
    gefangene_baelle_icon = pygame.transform.scale(gefangene_baelle_icon, (40, 40))
    verlorene_baelle_icon = pygame.image.load('left_life_01.png')
    verlorene_baelle_icon = pygame.transform.scale(verlorene_baelle_icon, (40, 40))

    # Platzieren der Bilder für die Symbole auf dem Bildschirm
    screen.blit(gefangene_baelle_icon, (10, 550))
    screen.blit(verlorene_baelle_icon, (10, 600))

    # Rendern und Anzeigen des Texts mit Bezeichnungen
    gefangene_baelle_text = score_font.render('Gefangene Bälle:', True, light_grey)
    leben_text = score_font.render('Verbliebene Leben:', True, light_grey)
    screen.blit(gefangene_baelle_text, (80, 550))
    screen.blit(leben_text, (80, 600))

    # Anzeigen der Variablen
    catch_counter = score_font.render(f'{collision_counter}', True, light_grey)
    lost_balls_counter = score_font.render(f'{respawn_counter}', True, light_grey)
    screen.blit(catch_counter, (300, 550))  # Position des gefangenen Bälle Texts und Bilds
    screen.blit(lost_balls_counter, (300, 600))  # Position des verlorenen Bälle Texts und Bilds

    if not playing and respawn_counter == 0:
        # Texte rendern
        died_text = endscreen_font.render('You died!', True, red)
        newGame_text = basic_font.render('Start New Game? Press N', True, red)

        # Breite und Höhe der Texte abrufen
        died_text_rect = died_text.get_rect()
        newGame_text_rect = newGame_text.get_rect()

        # Zentrale Position für die Texte berechnen
        died_text_rect.center = (screen_width // 2, screen_height // 2)
        newGame_text_rect.center = (screen_width // 2, screen_height // 2 + 100)

        # Texte auf dem Bildschirm platzieren
        screen.blit(died_text, died_text_rect)
        screen.blit(newGame_text, newGame_text_rect)


def countdown():
    global playing
    for i in range(3, 0, -1):
        screen.fill(bg_color)
        pygame.draw.aaline(screen, red, (0, screen_height - 100), (screen_width, screen_height - 100))
        # Ball und Spieler zeichnen
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.ellipse(screen, light_grey, ball)
        # Score anzeigen
        score()
        # Countdown anzeigen
        countdown_text = countdown_font.render(str(i), True, light_grey)
        countdown_text_rect = countdown_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(countdown_text, countdown_text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.fill(bg_color)
        pygame.draw.aaline(screen, red, (0, screen_height - 100), (screen_width, screen_height - 100))
        pygame.display.flip()
    playing = True


# General setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
light_grey = (200, 200, 200)
red = (255, 0, 0)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height - 200, 30, 30)
player = pygame.Rect(screen_width / 2 - 70, screen_height - 20, 140, 10)

# Game Variables
ball_speed_x = 7
ball_speed_y = -7
player_speed = 0
collision_counter = 0
life = 4
respawn_counter = life
running = True
playing = False

# Score text
score_font = pygame.font.Font('freesansbold.ttf', 20)
basic_font = pygame.font.Font('freesansbold.ttf', 32)
endscreen_font = pygame.font.Font('freesansbold.ttf', 70)
countdown_font = pygame.font.Font('freesansbold.ttf', 100)

pygame.display.set_caption("Pong Singleplayer - Playing" if playing else "Pong Singleplayer - Paused")
# Countdown beim Spielstart anzeigen
countdown()

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
                respawn_counter = life
                collision_counter = 0
                start_time = None  # Zurücksetzen der Startzeit für den Countdown
                playing = True
                countdown()

    if respawn_counter <= 0:
        respawn_counter = 0
        playing = False

    # Game Logic
    if playing:  # Führe Spiellogik nur aus, wenn das Spiel aktiv ist
        ball_animation()
        player_animation()

    # Visuals
    screen.fill(bg_color)
    # Score und Symbole anzeigen...
    score()
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, red, (0, screen_height - 100), (screen_width, screen_height - 100))

    pygame.display.flip()
    clock.tick(60)
