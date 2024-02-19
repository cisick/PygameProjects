# import the pygame module, so you can use it
import pygame
from pypong import *

#music "Space Running" from https://www.musicfox.com

pygame.init()
pygame.display.set_caption('PyPong')
screen = pygame.display.set_mode((640, 480))


setup_init(pygame, screen)

# define a variable to control the main loop
running = True
started = False
paused = False
muted = False
gameOver = False

clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

# main loop
while running:
    clock.tick(200)
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        move_player(event)
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "s":
                if not started:
                    setup_init(pygame, screen)
                    new_round(pygame, screen)
                    started = True
            elif pygame.key.name(event.key) == "p":
                if started:
                    paused = not paused
            elif pygame.key.name(event.key) == "q":
                paused = False
                started = False
                setup_init(pygame, screen)
            elif pygame.key.name(event.key) == "m":
                if not muted:
                    pygame.mixer.music.pause()
                    muted = True
                else:
                    pygame.mixer.music.unpause()
                    muted = False

    if started and not paused:
        started = not update_game(pygame, screen)
    pygame.display.update()

