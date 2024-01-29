# Aufgabe 1) Ändern Sie das Programm derart,
# dass die Variablen dx und dy (z.B. 3) am Programmanfang definiert werden. (fertig)
# Durch Drücken der Tasten ändert sich die Position des Objektes um diese Werte.
# Aufgabe 2) Startpunkt des Objektes soll zufällig erfolgen. (fertig)
# Aufgabe 3) Initialisieren Sie dx und dy auch zufällig (-20 bis 20)
# zu Beginn des Spiels und lassen Sie das Objekt sich selbständig bewegen.
# Aufgabe 4) Zeichnen Sie drei Rechtecke (oben, unten, rechts) als Begrenzung.

# Example file showing a circle moving on screen
import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dx = random.randint(-20, 20)
dy = random.randint(-20, 20)
dt = 0
player_pos = pygame.Vector2(random.randint(40, 1240), random.randint(40, 680))
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    pygame.draw.circle(screen, "red", player_pos, 40)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        print("Key: W")
        player_pos.y += 1 * dy
    if keys[pygame.K_s]:
        player_pos.y -= 1 * dy
    if keys[pygame.K_a]:
        player_pos.x += 1 * dx
    if keys[pygame.K_d]:
        player_pos.x -= 1 * dx

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
