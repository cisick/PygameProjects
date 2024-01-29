import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render('My game', False, 'Dark Grey').convert()

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_x_position = 810
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (300, 50))
    if snail_x_position < -90:
        snail_x_position = 810
    else:
        snail_x_position -= 2
    screen.blit(snail_surface, (snail_x_position, 265))

    pygame.display.update()
    clock.tick(60)
