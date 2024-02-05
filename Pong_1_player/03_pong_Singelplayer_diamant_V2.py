import pygame
import random
import sys
import time

def ball_animation():
    global ball_speed_x, ball_speed_y, collision_counter, respawn_counter, diamond_counter, level, d_treffer_pro_level_counter, d_treffer_until_destroyed_counter

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
        collision_counter += 1

    # Kollisionserkennung mit Diamanten
    for diamond in diamonds[:]:  # Durch eine Kopie der Liste iterieren, um während des Iterierens Elemente entfernen zu können
        if ball.colliderect(diamond):
            d_treffer_until_destroyed_counter += 1
            if d_treffer_until_destroyed_counter >= level:  # Überprüfen, ob die erforderliche Trefferzahl erreicht wurde
                diamonds.remove(diamond)
                diamond_counter += 1
                d_treffer_pro_level_counter += 1
                d_treffer_until_destroyed_counter = 0
                print(diamond)
                print(len(diamonds))
                if d_treffer_pro_level_counter >= 10:
                    level += 1
                    spawn_diamonds()
                    d_treffer_pro_level_counter = 0
            else:
                ball_speed_y *= -1  # Ball abprallen lassen, wenn die erforderliche Trefferzahl noch nicht erreicht wurde
                ball_speed_x *= -1



def player_animation():
    player.x += player_speed

    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def ball_start():
    global ball_speed_x, ball_speed_y, respawn_counter, collision_counter, playing, start_time

    ball.center = (screen_width / 2, screen_height - 200)
    ball_speed_y *= -1
    ball_speed_x *= random.choice((1, -1))
    player.center = (screen_width / 2, screen_height - 20)

    if respawn_counter > 0:
        countdown()

def score():
    # Anzeige von Level und Level-Counter
    level_text = score_font.render(f'Level: {level}', True, light_grey)
    screen.blit(level_text, (10, 10))
    pygame.draw.aaline(screen, red, (0, screen_height - 100), (screen_width, screen_height - 100))
    # Platzieren der Bilder für die Symbole auf dem Bildschirm
    screen.blit(diamond_icon, (10, screen_height - 250))
    screen.blit(gefangene_baelle_icon, (10, screen_height - 200))
    screen.blit(verlorene_baelle_icon, (10, screen_height - 150))


    # Anzeigen der Variablen
    screen.blit(score_font.render(str(diamond_counter), True, light_grey),(60, screen_height - 250))  # Position des Diamanten-Counters
    screen.blit(score_font.render(str(collision_counter), True, light_grey), (60, screen_height - 200))  # Position des gefangenen Bälle Counters
    screen.blit(score_font.render(str(respawn_counter), True, light_grey), (60, screen_height - 150))  # Position des verlorenen Bälle Counters


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

def spawn_diamonds():
    global diamonds
    print("SPAWN")
    diamonds = []
    for _ in range(10):
        diamond = pygame.Rect(random.randint(0, screen_width - 40), random.randint(0, screen_height // 2), 40, 40)
        diamonds.append(diamond)

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
diamond_counter = 0
d_treffer_pro_level_counter = 0
d_treffer_until_destroyed_counter = 10
level = 1
diamonds = []
diamond_icon = pygame.image.load('diamant.png')
diamond_icon = pygame.transform.scale(diamond_icon, (40, 40))
gefangene_baelle_icon = pygame.image.load('gefangene_baelle_01.png')
gefangene_baelle_icon = pygame.transform.scale(gefangene_baelle_icon, (40, 40))
verlorene_baelle_icon = pygame.image.load('left_life_01.png')
verlorene_baelle_icon = pygame.transform.scale(verlorene_baelle_icon, (40, 40))

running = True
playing = False
start_time = None

# Score text
basic_font = pygame.font.Font('freesansbold.ttf', 32)
endscreen_font = pygame.font.Font('freesansbold.ttf', 70)
countdown_font = pygame.font.Font('freesansbold.ttf', 100)
score_font = pygame.font.Font('freesansbold.ttf', 20)  # Hinzufügen der score_font Variable

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
