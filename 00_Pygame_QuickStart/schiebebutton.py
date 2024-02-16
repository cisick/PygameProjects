import pygame
import sys

# Initialisierung von Pygame
pygame.init()

# Farben definieren
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Bildschirmgröße
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200

# Schaltflächenabmessungen
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50

# Variable initialisieren
variable = 0

# Schriftart initialisieren
font = pygame.font.Font(None, 36)

# Bildschirm erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Schiebeschalter Beispiel")

# Funktion zum Zeichnen von Text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Funktion zum Zeichnen der Schaltflächen
def draw_buttons():
    # Plus-Schaltfläche zeichnen
    pygame.draw.rect(screen, GRAY, (150, 50, BUTTON_WIDTH, BUTTON_HEIGHT))
    draw_text("+", font, BLACK, 175, 75)

    # Minus-Schaltfläche zeichnen
    pygame.draw.rect(screen, GRAY, (50, 50, BUTTON_WIDTH, BUTTON_HEIGHT))
    draw_text("-", font, BLACK, 75, 75)

# Hauptprogrammschleife
running = True
while running:
    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Mausklick-Ereignisse überprüfen
            mouse_pos = pygame.mouse.get_pos()
            if 50 <= mouse_pos[0] <= 100 and 50 <= mouse_pos[1] <= 100:
                # Wenn die Maus auf der Minus-Schaltfläche liegt, Variable verringern
                variable -= 1
            elif 150 <= mouse_pos[0] <= 200 and 50 <= mouse_pos[1] <= 100:
                # Wenn die Maus auf der Plus-Schaltfläche liegt, Variable erhöhen
                variable += 1

    # Bildschirm löschen
    screen.fill(WHITE)

    # Schaltflächen zeichnen
    draw_buttons()

    # Variable zeichnen
    draw_text(str(variable), font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Bildschirm aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()
sys.exit()
