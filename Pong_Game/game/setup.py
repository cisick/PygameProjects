import pygame

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
diamond_icon = pygame.image.load('images/diamant.png')
diamond_icon = pygame.transform.scale(diamond_icon, (40, 40))
gefangene_baelle_icon = pygame.image.load('images/gefangene_baelle_01.png')
gefangene_baelle_icon = pygame.transform.scale(gefangene_baelle_icon, (40, 40))
verlorene_baelle_icon = pygame.image.load('images/left_life_01.png')
verlorene_baelle_icon = pygame.transform.scale(verlorene_baelle_icon, (40, 40))

running = True
playing = False
start_time = None

# Score text
basic_font = pygame.font.Font('freesansbold.ttf', 32)
endscreen_font = pygame.font.Font('freesansbold.ttf', 70)
countdown_font = pygame.font.Font('freesansbold.ttf', 100)
score_font = pygame.font.Font('freesansbold.ttf', 20)  # Hinzufügen der score_font Variable

