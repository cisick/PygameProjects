import pygame
import random

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750

# Farben
WHITE = (255, 255, 255)
BLACK = (205, 198, 115)
GREY49 = (125, 125, 125)
YELLOW = (255, 255, 0)

# Anzahl der Hühner
NUM_CHICKENS = 10

# Zeitdauer des Spiels in Sekunden
GAME_DURATION = 60  # 1 Minute

# Menü-Text
MENU_FONT = pygame.font.Font(None, 30)
TITLE_FONT = pygame.font.Font(None, 25)
TIMER_FONT = pygame.font.Font(None, 36)

# Bildschirm aktualisierungsrate
FPS = 60

# Fenster erstellen
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Moorhuhn Jagd')

# Bilder laden und an Fenstergröße anpassen
background_image = pygame.image.load('Moorhuhnbilder/Moorlandschaft.jpg').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
menu_image = pygame.image.load('Moorhuhnbilder/Moorhuhnjagd_Menubild_01.jpg').convert()
menu_image = pygame.transform.scale(menu_image, (WINDOW_HEIGHT, WINDOW_HEIGHT))
chicken_image_left = pygame.image.load('Moorhuhnbilder/Moorhuhn_01.png')
chicken_image_left = pygame.transform.scale(chicken_image_left, (40, 40))  # Huhn auf 40x40 skalieren
chicken_image_right = pygame.image.load('Moorhuhnbilder/Moorhuhn_02.png')
chicken_image_right = pygame.transform.scale(chicken_image_right, (40, 40))  # Huhn auf 40x40 skalieren

# Gruppe für Hühner
all_sprites = pygame.sprite.Group()
chickens = pygame.sprite.Group()


# Zurücksetzen der Variablen
def init():
    global all_sprites, chickens, score, ammo
    # Punkte und Munition zurücksetzen
    score = 0
    ammo = 8
    window.blit(background_image, (0, 0))
    all_sprites = pygame.sprite.Group()
    chickens = pygame.sprite.Group()

# Spieler
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)

# Huhn
class Chicken(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
        if self.direction == "left":
            self.image = chicken_image_right
            self.rect = self.image.get_rect()
            self.rect.x = WINDOW_WIDTH  # Huhn startet am rechten Bildschirmrand
            self.speed = random.randint(1, 3) * -1  # Huhn fliegt nach links
        else:
            self.image = chicken_image_left
            self.rect = self.image.get_rect()
            self.rect.x = 0 - self.rect.width  # Huhn startet am linken Bildschirmrand
            self.speed = random.randint(1, 3)  # Huhn fliegt nach rechts
        self.rect.y = random.randrange(0, WINDOW_HEIGHT // 2)

    def update(self):
        # Huhn bewegen
        self.rect.x += self.speed
        # Wenn das Huhn den Bildschirmrand erreicht, starte es von der anderen Seite neu
        if self.direction == "left" and self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
            self.rect.y = random.randrange(0, WINDOW_HEIGHT // 2)
            self.speed = random.randint(1, 3) * -1
        elif self.direction == "right" and self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0
            self.rect.y = random.randrange(0, WINDOW_HEIGHT // 2)
            self.speed = random.randint(1, 3)


# Spieler erstellen
player = Player()
all_sprites.add(player)

# Timer für das Spielende
game_end_timer = None

# Zähler für Punkte und Munition
score = 0
ammo = 8

# Counter-Anzeige
font = pygame.font.Font(None, 36)

# Menü anzeigen
def show_menu():
    window.fill(BLACK)
    # Zentriertes Menübild
    menu_rect = menu_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(menu_image, menu_rect)
    title_text = TITLE_FONT.render('Moorhuhn Jagd', True, WHITE)
    start_text = MENU_FONT.render('Neues Spiel starten', True, GREY49)
    title_text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    start_text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    # Button-Umrandung zeichnen
    pygame.draw.rect(window, YELLOW, (start_text_rect.left - 10, start_text_rect.top - 10,
                                      start_text_rect.width + 20, start_text_rect.height + 20), 3)

    window.blit(title_text, title_text_rect)
    window.blit(start_text, start_text_rect)
    pygame.display.flip()

# Menü klicken überprüfen
def check_menu_click(pos, start_text_rect):
    return start_text_rect.collidepoint(pos)

# Hauptspiel Schleife
running = True
game_running = False
menu_shown = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_running and menu_shown:
            # Überprüfe, ob der Mausklick auf den Button "Neues Spiel starten" erfolgt ist
            start_text_rect = MENU_FONT.render('Neues Spiel starten', True, WHITE).get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            if check_menu_click(event.pos, start_text_rect):
                # Starte ein neues Spiel, wenn auf den "Neues Spiel" -Button geklickt wird
                game_running = True
                game_end_timer = pygame.time.get_ticks() + GAME_DURATION * 1000  # Zeit in Millisekunden
                menu_shown = False
                # Alle Hühner entfernen
                chickens.empty()
                # Das Spiel neu zeichnen
                window.fill(WHITE)  # Hintergrund zeichnen
                all_sprites.draw(window)  # Hühner zeichnen
                pygame.display.flip()  # Spiel aktualisieren
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False
                menu_shown = True
                # zurücksetzen der Variablen
                init()
                # Das Menü neu zeichnen
                show_menu()

            if game_running:
                # Überprüfe, ob Munition vorhanden ist und reduziere sie bei Klick
                if event.key == pygame.K_r and ammo < 8:
                    ammo = 8

        elif event.type == pygame.MOUSEBUTTONDOWN and game_running:
            # Überprüfe, ob Munition vorhanden ist und reduziere sie bei Klick
            if ammo > 0:
                ammo -= 1
                # Überprüfe, ob ein Huhn angeklickt wurde
                clicked_sprites = [sprite for sprite in chickens if sprite.rect.collidepoint(event.pos)]
                if clicked_sprites:
                    clicked_sprites[0].kill()  # Entferne das Huhn
                    score += 1  # Erhöhe den Punktestand

    if game_running:
        # Spiel läuft
        current_time = pygame.time.get_ticks()
        if current_time >= game_end_timer:
            # Spielzeit abgelaufen
            game_running = False
            menu_shown = True
            init()
            # Das Menü neu zeichnen
            show_menu()
        else:
            # Hühner spawnen
            if len(chickens) < NUM_CHICKENS:
                if len(chickens) % 2 == 0:
                    chicken = Chicken("left")  # Huhn fliegt von links nach rechts
                else:
                    chicken = Chicken("right")  # Huhn fliegt von rechts nach links
                all_sprites.add(chicken)
                chickens.add(chicken)

            # Hintergrund zeichnen
            window.blit(background_image, (0, 0))

            # Hühner aktualisieren und zeichnen
            chickens.update()
            all_sprites.draw(window)

            # Punkte- und Munitionszähler anzeigen
            score_text = font.render("Punkte: " + str(score), True, WHITE)
            ammo_text = font.render("Munition: " + str(max(ammo, 0)), True, WHITE)  # Munition kann nicht negativ sein
            timer_text = TIMER_FONT.render("Verbleibende Zeit: " + str(max(0, (game_end_timer - current_time) // 1000)), True, WHITE)
            window.blit(score_text, (10, 10))
            window.blit(ammo_text, (10, 40))
            window.blit(timer_text, (10, 70))

            # Spiel aktualisieren
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)
    else:
        # Menü anzeigen
        show_menu()

# Pygame beenden
pygame.quit()