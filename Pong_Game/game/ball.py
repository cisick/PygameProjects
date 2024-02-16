import setup
import diamand
import collision

def ball_animation():
    global ball_speed_x, ball_speed_y, collision_counter, respawn_counter, diamond_counter, level, d_treffer_pro_level_counter, d_treffer_until_destroyed_counter

    setup.ball.x += ball_speed_x
    setup.ball.y += ball_speed_y
    if setup.ball.bottom >= setup.screen_height:
        respawn_counter -= 1
        collision.ball_start()
    if setup.ball.top <= 0:
        ball_speed_y *= -1
    if setup.ball.left <= 0 or setup.ball.right >= setup.screen_width:
        ball_speed_x *= -1

    if setup.ball.colliderect(setup.player):
        ball_speed_y *= -1
        collision_counter += 1

    # Kollisionserkennung mit Diamanten
    for diamond in setup.diamonds[:]:  # Durch eine Kopie der Liste iterieren, um während des Iterierens Elemente entfernen zu können
        if setup.ball.colliderect(diamond):
            d_treffer_until_destroyed_counter += 1
            if d_treffer_until_destroyed_counter >= level:  # Überprüfen, ob die erforderliche Trefferzahl erreicht wurde
                setup.diamonds.remove(diamond)
                diamond_counter += 1
                d_treffer_pro_level_counter += 1
                d_treffer_until_destroyed_counter = 0
                print(diamond)
                print(len(setup.diamonds))
                if d_treffer_pro_level_counter >= 10:
                    level += 1
                    spawn_diamonds()
                    d_treffer_pro_level_counter = 0
            else:
                ball_speed_y *= -1  # Ball abprallen lassen, wenn die erforderliche Trefferzahl noch nicht erreicht wurde
                ball_speed_x *= -1

