import pygame
from pygame.locals import *
import pygame.joystick
import sys
import math

pygame.init()
clock = pygame.time.Clock()

# Fenster einrichten
window_width = 1200
window_height = 700
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Air_Hockey')

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Spielumrandung
edge = 50

# Spieler initialisieren
num_players = 2
players = []
for i in range(num_players):
    player_radius = 25  # Radius des Spielers
    if i == 0:
        color = RED
        player_x = edge + player_radius
        player_y = window_height // 2
    else:
        color = BLUE
        player_x = window_width - edge - player_radius
        player_y = window_height // 2

    players.append([[player_x, player_y], color])


# Ball initialisieren
ball_radius = 20
ball_x = window_width // 2
ball_y = window_height // 2
ball_speed = 5
ball_velocity_x = 0
ball_velocity_y = 0

# Tore initialisieren
goal_width = 10
goal_height = 200
goal_left = pygame.Rect(0, window_height // 2 - goal_height // 2, goal_width, goal_height)
goal_right = pygame.Rect(window_width - goal_width, window_height // 2 - goal_height // 2, goal_width, goal_height)

# Spielerpunkte
player_scores = [0, 0]

# Text Schriftart initialisieren
font = pygame.font.SysFont(None, 36)

# Controller initialisieren
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
if joystick_count < num_players:
    print(f"Nicht genügend Joysticks gefunden. Du benötigst mindestens {num_players} PS4-Controller.")
    pygame.quit()
    sys.exit()
else:
    joysticks = [pygame.joystick.Joystick(i) for i in range(num_players)]
    for joystick in joysticks:
        joystick.init()


# Funktion zur Berechnung des Abstands zwischen zwei Punkten
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Funktion zum Zeichnen der Begrenzungen
def draw_boundaries():
    pygame.draw.rect(screen, WHITE, (0, edge, window_width, window_height - 2 * edge), 10)  # Spielumrandung
    pygame.draw.line(screen, WHITE, [window_width / 2, edge], [window_width / 2, window_height - edge], 5)
    pygame.draw.line(screen, WHITE, [window_width / 2 - 100, edge], [window_width / 2 - 100, window_height - edge], 5)
    pygame.draw.line(screen, WHITE, [window_width / 2 + 100, edge], [window_width / 2 + 100, window_height - edge], 5)
    pygame.draw.circle(screen, WHITE, (edge, window_height // 2), 200, 4)
    pygame.draw.circle(screen, WHITE, (window_width - edge, window_height // 2), 200, 5)  # Großer Kreis
    pygame.draw.circle(screen, WHITE, (window_width // 2, window_height // 2), 50, 5)  # Kleiner Kreis


# Funktion zum Zeichnen der Tore
def draw_goals():
    pygame.draw.rect(screen, players[0][1], goal_left)
    pygame.draw.rect(screen, players[1][1], goal_right)


# Hauptschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Eingaben von den Controllern verarbeiten
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)


        # Spieler bewegen
        players[i][0][0] += int(axis_x * 5)
        players[i][0][1] += int(axis_y * 5)

        # Begrenze die Position des Spielers innerhalb des Spielfelds
        players[i][0][0] = max(10 + player_radius, min(players[i][0][0], window_width - 10 - player_radius))
        players[i][0][1] = max(edge + 10 + player_radius, min(players[i][0][1], window_height - edge - 10 - player_radius))

        # Kollisionserkennung und Reaktion
        dist = distance(ball_x, ball_y, players[i][0][0], players[i][0][1])
        if dist < ball_radius + player_radius:
            # Berechne die Richtung des Stoßes
            dx = ball_x - players[i][0][0]
            dy = ball_y - players[i][0][1]
            angle = math.atan2(dy, dx)

            # Passe die Ballgeschwindigkeit entsprechend an
            ball_velocity_x = ball_speed * math.cos(angle)
            ball_velocity_y = ball_speed * math.sin(angle)

    # Bewege den Ball
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Überprüfe, ob der Ball in ein Tor gegangen ist
    if ball_x - ball_radius < 0:
        if goal_left.collidepoint(ball_x, ball_y):
            player_scores[1] += 1
            ball_x = window_width // 2
            ball_y = window_height // 2
            ball_velocity_x = 0
            ball_velocity_y = 0
    elif ball_x + ball_radius > window_width:
        if goal_right.collidepoint(ball_x, ball_y):
            player_scores[0] += 1
            ball_x = window_width // 2
            ball_y = window_height // 2
            ball_velocity_x = 0
            ball_velocity_y = 0

    # Begrenze die Position des Balls innerhalb des Fensters

    if ball_x - ball_radius < 10 and (ball_y > (window_height // 2) + (goal_height // 2) or ball_y < (window_height // 2) - (goal_height // 2)):
        ball_x = 10 + ball_radius
        ball_velocity_x *= -1

    elif ball_x + ball_radius > window_width - 10 and (ball_y > (window_height // 2) + (goal_height // 2) or ball_y < (window_height // 2) - (goal_height // 2)):
        ball_x = window_width - 10 - ball_radius
        ball_velocity_x *= -1

    if ball_y - ball_radius < edge + 10:
        ball_y = edge + 10 + ball_radius
        ball_velocity_y *= -1

    elif ball_y + ball_radius > window_height - edge -10:
        ball_y = window_height - edge - 10 - ball_radius
        ball_velocity_y *= -1


    # Bildschirm zeichnen
    screen.fill(BLACK)
    draw_boundaries()  # Spielfeldbegrenzungen zeichnen
    draw_goals()  # Tore zeichnen
    for player_pos, color in players:
        pygame.draw.circle(screen, color, player_pos, player_radius)

    # Spielerstand anzeigen
    player1_score_text = font.render(f"Player 1: {player_scores[0]}", True, RED)
    player2_score_text = font.render(f"Player 2: {player_scores[1]}", True, BLUE)
    screen.blit(player1_score_text, (20, 20))
    screen.blit(player2_score_text, (window_width - player2_score_text.get_width() - 20, 20))

    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)
    pygame.display.flip()

    # Bildschirm aktualisieren
    clock.tick(60)

pygame.quit()
sys.exit()
