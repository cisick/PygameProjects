import pygame
import random
import sys


def ball_animation():
    global ball_speed_x, ball_speed_y, collision_counter

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height:
        ball_start()
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    if ball.colliderect(player):
        ball_speed_y *= -1
        collision_counter += 1


def player_animation():
    player.x += player_speed

    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width


def ball_start():
    global ball_speed_x, ball_speed_y, respawn_counter, collision_counter, playing
    respawn_counter -= 1
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


def score():
    # Laden der Bilder für die Symbole
    gefangene_baelle_icon = pygame.image.load('gefangene_baelle_01.png')
    # gefangene_baelle_icon = pygame.transform.scale(gefangene_baelle_icon, (40, 40))
    verlorene_baelle_icon = pygame.image.load('left_life_01.png')
    # verlorene_baelle_icon = pygame.transform.scale(verlorene_baelle_icon, (40, 40))

    # Platzieren der Bilder für die Symbole auf dem Bildschirm
    screen.blit(gefangene_baelle_icon, (450, 470))
    screen.blit(verlorene_baelle_icon, (450, 380))

    # Rendern und Anzeigen des Texts mit Bezeichnungen
    gefangene_baelle_text = basic_font.render('Gefangene Bälle:', True, light_grey)
    leben_text = basic_font.render('Verbliebene Leben:', True, light_grey)
    screen.blit(gefangene_baelle_text, (600, 470))
    screen.blit(leben_text, (600, 380))

    # Anzeigen der Variablen
    catch_counter = basic_font.render(f'{collision_counter}', True, light_grey)
    lost_balls_counter = basic_font.render(f'{respawn_counter}', True, light_grey)
    screen.blit(catch_counter, (990, 470))  # Position des gefangenen Bälle Texts und Bilds
    screen.blit(lost_balls_counter, (990, 380))  # Position des verlorenen Bälle Texts und Bilds

    if playing == False and respawn_counter == 0:
        died_text = basic_font.render('You died!:', True, red)
        screen.blit(died_text, (200, 200))

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
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width / 2 - 70, screen_height - 20, 140, 10)

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
collision_counter = 0
respawn_counter = 4
running = True
playing = False

# Score text
basic_font = pygame.font.Font('freesansbold.ttf', 32)

while running:

    pygame.display.set_caption("Pong Singelplayer - Playing" if playing else "Pong Singelplayer - Paused")

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
