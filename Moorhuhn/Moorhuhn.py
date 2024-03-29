import pygame
import random
import pickle
import sys

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750

# Farben
WHITE = (255, 255, 255)
GREEN_LIGHT = (205, 198, 115)
DARK_SLATE_GRAY = (47, 79, 79)
GREY49 = (125, 125, 125)
YELLOW = (255, 255, 0)

# Anzahl der Hühner
NUM_CHICKENS = 10

# Anzahl der Ballons
NUM_BALLOONS = 2

# Zeitdauer des Spiels in Sekunden
GAME_DURATION = 60   # 1 Minute

# Menü-Text
MENU_FONT = pygame.font.Font(None, 30)
TITLE_FONT = pygame.font.Font(None, 25)
TIMER_FONT = pygame.font.Font(None, 36)
OPTION_FONT = pygame.font.Font(None, 40)
HIGHSCORE_FONT_H = pygame.font.Font(None, 80)
HIGHSCORE_FONT = pygame.font.Font(None, 60)

# Bildschirmaktualisierungsrate
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
balloon_image = pygame.image.load('Moorhuhnbilder/Ballon_01.png')
balloon_image = pygame.transform.scale(balloon_image, (90, 140))  # Huhn auf 100x50 skalieren
# mouse cursor
cursor_game = pygame.image.load('Moorhuhnbilder/mouse_03.png')
cursor_game = pygame.transform.scale(cursor_game, (60, 60))
cursor_button_click = pygame.image.load('Moorhuhnbilder/mouse_02.png')
cursor_button_click = pygame.transform.scale(cursor_button_click, (40, 40))

# Audio laden
menu_sound = pygame.mixer.Sound("audio/menu_sound.mp3")
shot_sound = pygame.mixer.Sound("audio/9mm_pistol_shot_sound.mp3")
alarm_sound = pygame.mixer.Sound("audio/chicken_single_alarm_sound.mp3")
e_shot_sound = pygame.mixer.Sound("audio/empty_gun_shot_sound.mp3")
load_sound = pygame.mixer.Sound("audio/load_gun_sound.mp3")
slap_sound = pygame.mixer.Sound("audio/hardslap.mp3")
pop_sound = pygame.mixer.Sound("audio/pop_balloon.mp3")

# Gruppe für Hühner
all_sprites = pygame.sprite.Group()
chickens = pygame.sprite.Group()
balloons = pygame.sprite.Group()


# Zurücksetzen der Variablen
def init():
    global all_sprites, chickens, score, ammo, playing, option_menu, highscore_menu, menu_shown, chicken_kill, balloon_kill, balloons, is_audio_running
    pygame.display.set_caption("Moorhuhn Jagd")
    playing = True
    option_menu = False
    highscore_menu = False
    player.score = 0
    score = 0
    ammo = 8
    chicken_kill = False
    balloon_kill = False
    window.blit(background_image, (0, 0))
    all_sprites = pygame.sprite.Group()
    chickens = pygame.sprite.Group()
    balloons = pygame.sprite.Group()
    menu_shown = True
    is_audio_running = False
    pygame.mouse.set_visible(True)
    # Stop Music
    menu_sound.stop()


# Spieler
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
        self.score = 0  # Initialisierung der Punktzahl

    def increase_score(self, points):
        self.score += points

    def decrease_score(self, points):
        self.score -= points


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


# Heißluftballon
class Balloon(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
        if self.direction == "left":
            self.image = balloon_image
            self.rect = self.image.get_rect()
            self.rect.x = WINDOW_WIDTH  # Ballon startet am rechten Bildschirmrand
            self.speed = -1  # Ballon fliegt nach links
        else:
            self.image = balloon_image
            self.rect = self.image.get_rect()
            self.rect.x = 0 - self.rect.width  # Ballon startet am linken Bildschirmrand
            self.speed = 1  # Ballon fliegt nach rechts
            self.rect.y = random.randrange(0, WINDOW_HEIGHT // 2)

    def update(self):
        # Ballon bewegen
        self.rect.x += self.speed
        # Wenn der Ballon den Bildschirmrand erreicht, starte er von der anderen Seite neu
        if self.direction == "left" and self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
            self.rect.y = random.randrange(0, WINDOW_HEIGHT // 2)
            self.speed = -1
        elif self.direction == "right" and self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0
            self.rect.y = random.randrange(0, WINDOW_HEIGHT // 2)
            self.speed = 1


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
    global is_audio_running
    window.fill(GREEN_LIGHT)
    # Zentriertes Menübild
    menu_rect = menu_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(menu_image, menu_rect)
    title_text = TITLE_FONT.render('Moorhuhn Jagd', True, WHITE)
    start_text = MENU_FONT.render('Neues Spiel starten', True, WHITE)
    option_text = MENU_FONT.render('Tastenbelegung', True, WHITE)
    highscore_text = MENU_FONT.render('Highscore', True, WHITE)
    quit_text = MENU_FONT.render('Beenden', True, WHITE)
    title_text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    start_text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, 180))
    option_text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, 240))
    highscore_text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, 305))
    quit_text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, 370))

    if not is_audio_running:
        pygame.mixer.Sound.play(menu_sound, loops = -1) # audio
        is_audio_running = True

    window.blit(title_text, title_text_rect)
    window.blit(start_text, start_text_rect)
    window.blit(option_text, option_text_rect)
    window.blit(highscore_text, highscore_text_rect)
    window.blit(quit_text, quit_text_rect)
    pygame.display.flip()


def show_option_menu():
    global WINDOW_HEIGHT
    window.fill(GREEN_LIGHT)
    # Erstelle eine Linie
    start_pos = (300, 110)  # Senkrechte Linie startet in der Mitte oben
    end_pos = (300, WINDOW_HEIGHT)
    pygame.draw.line(window, DARK_SLATE_GRAY, start_pos, end_pos, 5)

    # Überschrift
    key_assignment = HIGHSCORE_FONT_H.render('Tastenbelegung: ', True, DARK_SLATE_GRAY)
    key_assignment_text_rect = key_assignment.get_rect(topleft=(50, 40))

    # Taste
    esc = HIGHSCORE_FONT.render('ESC', True, DARK_SLATE_GRAY)
    esc_rect = esc.get_rect(topleft=(50, 110))
    r = HIGHSCORE_FONT.render('R', True, DARK_SLATE_GRAY)
    r_rect = r.get_rect(topleft=(50, 170))
    mouse_left = HIGHSCORE_FONT.render('Maus links', True, DARK_SLATE_GRAY)
    mouse_left_rect = mouse_left.get_rect(topleft=(50, 230))
    space = HIGHSCORE_FONT.render('Leertaste', True, DARK_SLATE_GRAY)
    space_rect = space.get_rect(topleft=(50, 290))

    # Text
    esc_text = HIGHSCORE_FONT.render('Zurück zum Menu', True, DARK_SLATE_GRAY)
    esc_text_rect = esc_text.get_rect(topleft=(350, 110))
    r_text = HIGHSCORE_FONT.render('Nachladen', True, DARK_SLATE_GRAY)
    r_text_rect = r_text.get_rect(topleft=(350, 170))
    mouse_left_text = HIGHSCORE_FONT.render('Schießen', True, DARK_SLATE_GRAY)
    mouse_left_text_rect = mouse_left_text.get_rect(topleft=(350, 230))
    space_text = HIGHSCORE_FONT.render('Spiel pausieren', True, DARK_SLATE_GRAY)
    space_text_rect = space_text.get_rect(topleft=(350, 290))

    # Anzeige:
    # Überschrift
    window.blit(key_assignment, key_assignment_text_rect)
    # Taste anzeigen
    window.blit(esc, esc_rect)
    window.blit(r, r_rect)
    window.blit(mouse_left, mouse_left_rect)
    window.blit(space, space_rect)
    # Text anzeigen
    window.blit(esc_text, esc_text_rect)
    window.blit(r_text, r_text_rect)
    window.blit(mouse_left_text, mouse_left_text_rect)
    window.blit(space_text, space_text_rect)

    pygame.display.flip()


def input_username():
    input_active = True
    player_name = ""
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        window.fill(GREEN_LIGHT)

        username = HIGHSCORE_FONT.render("Geben Sie Ihren Namen ein:", True, DARK_SLATE_GRAY)
        username_rect = username.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
        user_input = HIGHSCORE_FONT.render(player_name, True, DARK_SLATE_GRAY)
        user_input_rect = user_input.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
        window.blit(username, username_rect)
        window.blit(user_input, user_input_rect)

        pygame.display.flip()

    # Spielernamen in der Player-Instanz setzen
    player.name = player_name


def save_score(player):
    try:
        with open('highscores.dat', 'rb') as file:
            highscores = pickle.load(file)
    except (FileNotFoundError, EOFError):
        highscores = []

    # Player-Instanz in ein Tupel aus Spielername und Punktzahl
    player_data = (player.name, player.score)
    highscores.append(player_data)
    highscores.sort(key=lambda x: x[1], reverse=True)  # Nach der Punktzahl sortieren

    # Spielerdaten speichern
    highscores_without_surface = highscores[:10]
    with open('highscores.dat', 'wb') as file:
        pickle.dump(highscores_without_surface, file)


def show_highscore():
    window.fill(GREEN_LIGHT)
    try:
        with open('highscores.dat', 'rb') as file:
            highscores = pickle.load(file)
            window.fill(GREEN_LIGHT)
            window.blit(HIGHSCORE_FONT_H.render("Highscore:", True, DARK_SLATE_GRAY), (50, 40))
            for i, player_data in enumerate(highscores, 1):
                name, score = player_data  # Entpacken des Spielerdaten-Tupels
                window.blit(HIGHSCORE_FONT.render(f"{i}. {name}: {score}", True, DARK_SLATE_GRAY), (50, 50 + i * 60))
    except FileNotFoundError:
        window.fill(GREEN_LIGHT)
        window.blit(HIGHSCORE_FONT.render("Es ist noch kein Highscore vorhanden.", True, DARK_SLATE_GRAY), (50, 50))
    pygame.display.flip()


def change_cursor_game():
    pygame.mouse.set_visible(False)
    pos = pygame.mouse.get_pos()
    pos = (pos[0] - 30, pos[1] - 30)
    window.blit(cursor_game, pos)
    # pygame.display.update()


def change_cursor_option():
    pygame.mouse.set_visible(False)
    pos = pygame.mouse.get_pos()
    window.blit(cursor_button_click, pos)


# Hauptspiel Schleife
running = True
game_running = False
menu_shown = True
playing = True
option_menu = False
highscore_menu = False
is_audio_running = False
cursor_set_visible = True

# hitbox variabeln
hitbox_width = 230
hitbox_height = 40
hitbox_x = 480
hitbox_y1 = 160
hitbox_y2 = 222
hitbox_y3 = 284
hitbox_y4 = 346

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_running and menu_shown:
            # Überprüfen, ob die Maus innerhalb der Hitbox liegt
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if hitbox_x < mouse_x < hitbox_x + hitbox_width and \
               hitbox_y1 < mouse_y < hitbox_y1 + hitbox_height:
                # Starte ein neues Spiel, wenn auf den "Neues Spiel" -Button geklickt wird
                game_running = True
                game_end_timer = pygame.time.get_ticks() + GAME_DURATION * 1000  # Zeit in Millisekunden
                menu_shown = False
                # zurücksetzen der Variabeln
                init()
                # Das Spiel neu zeichnen
                window.fill(WHITE)  # Hintergrund zeichnen
                all_sprites.draw(window)  # Hühner zeichnen
                pygame.display.flip()  # Spiel aktualisieren

            elif hitbox_x < mouse_x < hitbox_x + hitbox_width and hitbox_y2 < mouse_y < hitbox_y2 + hitbox_height:
                print("Option Tastenbelegung")
                option_menu = True

            elif hitbox_x < mouse_x < hitbox_x + hitbox_width and hitbox_y3 < mouse_y < hitbox_y3 + hitbox_height:
                # Highscore anzeigen, wenn auf den "Highscore" -Button geklickt wird
                highscore_menu = True
                show_highscore()  # Anzeigen des Highscores

            elif hitbox_x < mouse_x < hitbox_x + hitbox_width and hitbox_y4 < mouse_y < hitbox_y4 + hitbox_height:
                print("Beenden")

                sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False
                menu_shown = True
                init()  # zurücksetzen der Variablen
                show_menu()  # Das Menü neu zeichnen

            if game_running:
                if event.key == pygame.K_SPACE:
                    playing = not playing  # Pausieren oder Fortsetzen des Spiels

                # Überprüfe, ob Munition vorhanden ist und reduziere sie bei Klick
                if event.key == pygame.K_r and ammo < 8:
                    pygame.mixer.Sound.play(load_sound)
                    ammo = 8

        elif event.type == pygame.MOUSEBUTTONDOWN and game_running:
            # Überprüfe, ob Munition vorhanden ist und reduziere sie bei Klick
            if ammo == 0:
                pygame.mixer.Sound.play(e_shot_sound)
            if ammo > 0:
                pygame.mixer.Sound.play(shot_sound)
                ammo -= 1
                # Überprüfe, ob ein Huhn angeklickt wurde
                clicked_sprites = [sprite for sprite in chickens if sprite.rect.collidepoint(event.pos)]
                if clicked_sprites:
                    clicked_sprites[0].kill()  # Entferne das Huhn
                    chicken_kill = True
                    player.increase_score(1)  # Erhöhe den Punktestand
                # Überprüfe, ob ein Ballon angeklickt wurde
                clicked_sprites = [sprite for sprite in balloons if sprite.rect.collidepoint(event.pos)]
                if clicked_sprites:
                    clicked_sprites[0].kill()  # Entferne Ballon
                    balloon_kill = True
                    if player.score > 10:
                        player.decrease_score(10)  # Verringere den Punktestand
                    else:
                        player.score = 0

    if game_running:
        # Spiel läuft
        pygame.display.set_caption("Moorhuhn Jagd - Playing" if playing else "Moorhuhn Jagd - Paused")
        current_time = pygame.time.get_ticks()
        menu_sound.stop()
        if playing:
            if current_time <= 10:
                pygame.mixer.Sound.play(alarm_sound)
            if chicken_kill:
                pygame.mixer.Sound.play(slap_sound)
                chicken_kill = False
            if balloon_kill:
                pygame.mixer.Sound.play(pop_sound)
                balloon_kill = False
            if current_time >= game_end_timer:
                # Spielzeit abgelaufen
                game_running = False
                input_username()
                save_score(player)
                show_highscore()  # Anzeigen des Highscores nach dem Spiel
                init()
                #Das Menü neu zeichnen
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
                if len(balloons) < NUM_BALLOONS:
                    if len(balloons) % 2 == 0:
                        balloon = Balloon("left")  # Huhn fliegt von links nach rechts
                    else:
                        balloon = Balloon("right")  # Huhn fliegt von rechts nach links
                    all_sprites.add(balloon)
                    balloons.add(balloon)

                # Hintergrund zeichnen
                window.blit(background_image, (0, 0))

                # Hühner aktualisieren und zeichnen
                chickens.update()
                balloons.update()
                all_sprites.draw(window)
                change_cursor_game()

                # Punkte- und Munitionszähler anzeigen
                score_text = font.render("Punkte: " + str(player.score), True, WHITE)  # Spielerpunkte anzeigen
                ammo_text = font.render("Munition: " + str(max(ammo, 0)), True, WHITE)  # Munition kann nicht negativ sein
                timer_text = TIMER_FONT.render("Verbleibende Zeit: " + str(max(0, (game_end_timer - current_time) // 1000)) + " sec", True, WHITE)
                window.blit(score_text, (10, 10))
                window.blit(ammo_text, (10, 40))
                window.blit(timer_text, (10, 70))

                # Spiel aktualisieren
                pygame.display.flip()
                pygame.time.Clock().tick(FPS)

    elif option_menu:
        show_option_menu()
    elif highscore_menu:
        show_highscore()
    else:
        # Menü anzeigen
        show_menu()

# Pygame beenden
# pygame.quit()
sys.exit()
