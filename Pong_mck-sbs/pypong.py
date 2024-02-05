import pygame
import random

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (50, 50, 50)
COLOR_GREEN = (0, 255, 0)

X_PLAYER = 600
X_MACHINE = 30

score_player = 0
score_machine = 0

rect_player = None
rect_machine = None
circ_ball = None

dy_player = 0
dy_machine = 0

gameOver = False;
#dx,dx,x,y,r

ball = []


def setup_init(pyg, scr):
    global rect_player, rect_machine, circ_ball, ball, score_machine, score_player, gameOver

    score_player = 0
    score_machine = 0
    gameOver = False;
    scr.fill(COLOR_BLACK)
    x, y = scr.get_size()

    #Mittellinie
    pyg.draw.rect(scr, COLOR_GRAY, (x/2-5, 0, 10, y))
    # Balken links, screen, Farbe, (x, y, Breite, Höhe)
    rect_player = pygame.Rect((X_PLAYER, y/2-35, 10, 70))
    rect_machine = pygame.Rect((X_MACHINE, y/2-35, 10, 70))
    ball = [1, 0, int(x/2), int(y/2), 7]

    pyg.draw.rect(scr, COLOR_WHITE, rect_player)
    pyg.draw.rect(scr, COLOR_WHITE, rect_machine)

    # Kreis, screen, Farbe, (x,y), Radius, Strichstärke
    pyg.draw.circle(scr, COLOR_WHITE, (x/2, y/2), 7, 0)

    font_score1 = pygame.font.SysFont(None, 200)
    font_score2 = pygame.font.SysFont(None, 200)
    text_score1 = font_score1.render(str(score_player), True, COLOR_GRAY)
    text_score2 = font_score2.render(str(score_machine), True, COLOR_GRAY)

    scr.blit(text_score1, (120,50))
    scr.blit(text_score2, (440, 50))

    #Text
    font = pygame.font.SysFont(None, 48)
    font2 = pygame.font.SysFont(None, 32)


    text = font.render("Pong-Game implemented in Python", True, COLOR_GREEN)
    text2 = font2.render("s: start, m: mute/unmute, p: pause/run, q: quit", True, COLOR_GREEN)


    textpos = text.get_rect()
    textpos.centerx = scr.get_rect().centerx

    textpos2 = text2.get_rect()
    textpos2.centerx = scr.get_rect().centerx
    textpos2.centery = 70

    scr.blit(text, textpos)
    scr.blit(text2, textpos2)

def manage_items(pyg, scr):
    global dy_player, dy_machine, score_machine, score_player, gameOver

    x, y = scr.get_size()

    #dy_machine = 4

    #KI für Arme
    if rect_machine.y + 50 < ball[3]:
        dy_machine = 2
    elif rect_machine.y + 20> ball[3]:
        dy_machine = -2
    else:
        dy_machine = 0


    #Begrenzung Gegner
    if rect_machine.y < 0:
        dy_machine = 0
        rect_machine.y = 0
    elif rect_machine.y > y - 70:
        dy_machine = 0
        rect_machine.y = y -70

    rect_machine.move_ip(0, dy_machine)

    #Begrenzung Spieler
    if rect_player.y < 0:
        dy_player = 0
        rect_player.y = 0
    elif rect_player.y > y - 70:
        dy_player = 0
        rect_player.y = y -70


    rect_player.move_ip(0, dy_player)

    #if ball[2] < 0:
    #    ball[0] = ball[0] * -1

    if ball[2] > x + 100:
        ball[0] = 1
        score_machine = score_machine +1
        new_round(pyg, scr)

    elif ball[2] < 0:
        ball[0] = -1
        score_player = score_player +1
        new_round(pyg, scr)

    if score_player == 10 or score_machine == 10:
        font_score = pygame.font.SysFont(None, 50)
        if score_player == 10:
            text_score = font_score.render("WON!", True, COLOR_GREEN)
        else:
            text_score = font_score.render("LOST!", True, COLOR_GREEN)
        scr.blit(text_score, (350, 10))
        gameOver = True

    #player spielt ball
    if (ball[2] > rect_player.x and ball[2] < rect_player.x + 10 ) and ( ball[3] > rect_player.y and ball[3] < rect_player.y + rect_player.height):
        ##nach erster Runde schneller
        if ball[0] == 1:
            ball[0] = ball[0] * 4

        #Richtungswechsel spieler
        ball[1] = int((ball[3] - rect_player.y -35 + 3) / 10)
        ball[2] = rect_player.x

        if ball[1] == 0:
            ball[1] = random.randint(-1, 1)

        ball[0] = ball[0] * -1

    #Maschine spielt ball
    if (ball[2] < rect_machine.x  and ball[2] > rect_machine.x - 10) and ( ball[3] > rect_machine.y and ball[3] < rect_machine.y + rect_machine.height):
        ##nach erster Runde schneller
        if ball[0] == -1:
            ball[0] = ball[0] * -4

        #Richtungswechsel spieler
        ball[1] = int((ball[3] - rect_machine.y -35 + 3) / 10)
        ball[2] = rect_machine.x

        if ball[1] == 0:
            ball[1] = random.randint(-1, 1)

        ball[0] = ball[0] * -1


    #Spiel über Bande
    if ball[3] > y-3 or ball[3] < 0:
        ball[1] = ball[1] * -1


    #Ballbewegung
    ball[2] = ball[2] + ball[0]
    ball[3] = ball[3] + ball[1]


    #pyg.draw.circle(scr, COLOR_WHITE, (ball[0], ball[1]), ball[2], ball[3])

def update_game(pyg, scr):
    global rect_player, rect_machine, score_machine, score_player, gameOver



    scr.fill(COLOR_BLACK)
    x, y = scr.get_size()

    manage_items(pyg, scr)

    #Mittellinie
    pyg.draw.rect(scr, COLOR_GRAY, (x/2-5, 0, 10, y))
    # Balken links, screen, Farbe, (x, y, Breite, Höhe)

    pyg.draw.rect(scr, COLOR_WHITE, rect_player)

    pyg.draw.rect(scr, COLOR_WHITE, rect_machine)

    # Kreis, screen, Farbe, (x,y), Radius, Strichstärke
    #pyg.draw.circle(scr, COLOR_WHITE, (x/2, y/2), 7, 0)


    font_score1 = pygame.font.SysFont(None, 200)
    font_score2 = pygame.font.SysFont(None, 200)
    text_score1 = font_score1.render(str(score_machine), True, COLOR_GRAY)
    text_score2 = font_score2.render(str(score_player), True, COLOR_GRAY)

    scr.blit(text_score1, (120,50))
    scr.blit(text_score2, (440, 50))

    pyg.draw.circle(scr, COLOR_WHITE, (ball[2], ball[3]), ball[4], 0)

    return gameOver

def move_player(ev):
    global dy_player
    global rect_player

    if ev.type == pygame.KEYDOWN:
        if pygame.key.name(ev.key) == "down":
            dy_player = 3
        elif pygame.key.name(ev.key) == "up":
            dy_player = -3

    if ev.type == pygame.KEYUP:
        if pygame.key.name(ev.key) == "down" or pygame.key.name(ev.key) == "up":
            dy_player = 0


def new_round(pyg, scr):
    global ball

    x, y = scr.get_size()

    ball[1] = random.randint(-1, 1)

    ball[2] = x/2
    ball[3] = random.randint(100, 400)
