import pygame
import random
import sys

# Initialisierung von Pygame
pygame.init()

# Bildschirmgröße
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fenster erstellen
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Bilder laden
hangman_imgs = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

# Font für die Anzeige des Wortes
font = pygame.font.SysFont(None, 60)
font_hint = pygame.font.SysFont(None, 30)

# Wörterliste
word_list = [
    "apfel", "banane", "orange", "traube", "ananas", "erdbeere", "heidelbeere",
    "tisch", "stuhl", "bett", "schrank", "lampe", "teppich", "vorhang",
    "hund", "katze", "maus", "kaninchen", "hamster", "vogel", "fisch",
    "auto", "zug", "flugzeug", "schiff", "fahrrad", "motorrad", "roller",
    "schule", "kindergarten", "universität", "buch", "stift", "radiergummi",
    "sonne", "mond", "sterne", "wolke", "regen", "schnee", "wind",
    "park", "spielplatz", "zoo", "museum", "strand", "wald", "berg"
]


# Zufälliges Wort auswählen
word = random.choice(word_list)
guessed = ["_" for _ in word]  # Liste zum Speichern der geratenen Buchstaben

# Variable zum Zählen der falschen Versuche
wrong_attempts = 0

# Funktion zum Zeichnen des Hangman-Bildes
def draw_hangman():
    win.blit(hangman_imgs[wrong_attempts], (100, 100))

# Funktion zum Zeichnen des Wortes
def draw_word():
    text = font.render(" ".join(guessed), True, BLACK)
    win.blit(text, (300, 400))

# Funktion zum Überprüfen des Spielstatus
def check_game_status():
    if wrong_attempts == 6:
        return "lose"
    elif "_" not in guessed:
        return "win"
    else:
        return "continue"

# Hauptspiel-Schleife
run = True
while run:
    # Event-Schleife
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Überprüfe, ob die Eingabetaste (Enter) gedrückt wurde
                # Zurücksetzen des Spiels
                wrong_attempts = 0
                word = random.choice(word_list)
                guessed = ["_" for _ in word]

            if pygame.K_a <= event.key <= pygame.K_z and not (wrong_attempts == 6 or "_" not in guessed):
                letter = chr(event.key)
                if letter in word:
                    for i, char in enumerate(word):
                        if char == letter:
                            guessed[i] = letter
                else:
                    wrong_attempts += 1



    # Bildschirm löschen
    win.fill(WHITE)

    # Hangman zeichnen
    draw_hangman()

    # Wort zeichnen
    draw_word()

    # Spielanweisung
    text = font_hint.render("Neues Spiel starten: Enter", True, BLACK)
    win.blit(text, (10, 10))

    # Spielstatus überprüfen
    game_status = check_game_status()
    if game_status == "lose":
        text = font.render("You Lose!", True, BLACK)
        win.blit(text, (300, 200))
    elif game_status == "win":
        text = font.render("You Win!", True, BLACK)
        win.blit(text, (300, 200))

    # Bildschirm aktualisieren
    pygame.display.update()

# Pygame beenden
# pygame.quit()
# sys.exit()
