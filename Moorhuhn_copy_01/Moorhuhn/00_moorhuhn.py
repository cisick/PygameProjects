import pygame
import random
import button


class Game:
    def __init__(self, width = 1400, height = 750):
        self.WIDTH = width
        self.HEIGHT = height
        # define fonts
        self.font = pygame.font.SysFont("arialblack", 40)
        # define colours
        self.TEXT_COL = (255, 255, 255)

        # Erstellen des Anwendungsfensters
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # game variables
        self.clock = pygame.time.Clock()
        self.game_paused = False
        self.menu_state = "main"
        self.running = True

        # load background
        self.background_picture = pygame.image.load("Moorhuhnbilder/Moorhuhnlandschaft.jpg").convert_alpha()
        self.rect = self.background_picture.get_rect()

        # load button images
        self.resume_img = pygame.image.load("Images/button_resume.png").convert_alpha()
        self.rect = self.resume_img.get_rect()
        self.options_img = pygame.image.load("Images/button_options.png").convert_alpha()
        self.rect = self.options_img.get_rect()
        self.quit_img = pygame.image.load("Images/button_quit.png").convert_alpha()
        self.rect = self.quit_img.get_rect()
        self.video_img = pygame.image.load('Images/button_video.png').convert_alpha()
        self.rect = self.video_img.get_rect()
        self.audio_img = pygame.image.load('Images/button_audio.png').convert_alpha()
        self.rect = self.audio_img.get_rect()
        self.keys_img = pygame.image.load('Images/button_keys.png').convert_alpha()
        self.rect = self.keys_img.get_rect()
        self.back_img = pygame.image.load('Images/button_back.png').convert_alpha()
        self.rect = self.back_img.get_rect()
        # Weitere Initialisierungen...

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False
            # Weitere Ereignisbehandlungen...

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Spiellogik aktualisieren, z.B. Kollisionen überprüfen, Punkte berechnen usw.
        pass

    def render(self):
        self.screen.fill((205, 170, 125))  # Hintergrund zeichnen
        self.screen.blit(self.background_picture, (0, 0))
        # Alle Spielobjekte zeichnen, z.B. Moorhühner, Schütze, Punkteanzeige usw.

        pygame.display.flip()

    def menu(self):
        pygame.display.set_caption("Main Menu")

        # create button instances
        resume_button = button.Button(304, 125, self.resume_img, 1)
        options_button = button.Button(297, 250, self.options_img, 1)
        quit_button = button.Button(336, 375, self.quit_img, 1)
        video_button = button.Button(226, 75, self.video_img, 1)
        audio_button = button.Button(225, 200, self.audio_img, 1)
        keys_button = button.Button(246, 325, self.keys_img, 1)
        back_button = button.Button(332, 450, self.back_img, 1)

        # check if game is paused
        if self.game_paused == True:
            # check menu state
            if self.menu_state == "main":
                # draw pause screen buttons
                if resume_button.draw(self.screen):
                    game_paused = False
                if options_button.draw(self.screen):
                    self.menu_state = "options"
                if quit_button.draw(self.screen):
                    run = False
            # check if the options menu is open
            if self.menu_state == "options":
                # draw the different options buttons
                if video_button.draw(self.screen):
                    print("Video Settings")
                if audio_button.draw(self.screen):
                    print("Audio Settings")
                if keys_button.draw(self.screen):
                    print("Change Key Bindings")
                if back_button.draw(self.screen):
                    menu_state = "main"
        else:
            draw_text("Press SPACE to pause", self.font, self.TEXT_COL, 160, 250)

        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            self.screen.blit(img, (x, y))

            pygame.display.update()

        pygame.quit()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Highscore:
    def __init__(self):
        self.image = pygame.image.load("schuetze.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Moorhuhn:
    def __init__(self, x, y):
        self.image = pygame.image.load("Moorhuhnbilder/Moorhuhn_01.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = random.randint(1, 3)  # Zufällige Geschwindigkeit

    def update(self):
        self.rect.x += self.velocity

        # Moorhuhn-Bewegung aktualisieren, z.B. umdrehen, wenn der Bildschirmrand erreicht wird

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Schuetze:
    def __init__(self):
        self.image = pygame.image.load("schuetze.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Munition:
    def __init__(self):
        self.image = pygame.image.load("schuetze.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Weitere Klassen wie Hindernisse, Waffen, Punktezähler usw. können ebenfalls hinzugefügt werden

if __name__ == "__main__":
    pygame.init()
    game = Game()
    pygame.display.set_caption("Moorhuhn")
    game.run()
    pygame.quit()
