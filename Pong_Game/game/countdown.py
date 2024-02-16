def score():
    # Anzeige von Level und Level-Counter
    level_text = score_font.render(f'Level: {level}', True, light_grey)
    screen.blit(level_text, (10, 10))
    pygame.draw.aaline(screen, red, (0, screen_height - 100), (screen_width, screen_height - 100))
    # Platzieren der Bilder für die Symbole auf dem Bildschirm
    screen.blit(diamond_icon, (10, screen_height - 250))
    screen.blit(gefangene_baelle_icon, (10, screen_height - 200))
    screen.blit(verlorene_baelle_icon, (10, screen_height - 150))


    # Anzeigen der Variablen
    screen.blit(score_font.render(str(diamond_counter), True, light_grey),(60, screen_height - 250))  # Position des Diamanten-Counters
    screen.blit(score_font.render(str(collision_counter), True, light_grey), (60, screen_height - 200))  # Position des gefangenen Bälle Counters
    screen.blit(score_font.render(str(respawn_counter), True, light_grey), (60, screen_height - 150))  # Position des verlorenen Bälle Counters


    if not playing and respawn_counter == 0:
        # Texte rendern
        died_text = endscreen_font.render('You died!', True, red)
        newGame_text = basic_font.render('Start New Game? Press N', True, red)

        # Breite und Höhe der Texte abrufen
        died_text_rect = died_text.get_rect()
        newGame_text_rect = newGame_text.get_rect()

        # Zentrale Position für die Texte berechnen
        died_text_rect.center = (screen_width // 2, screen_height // 2)
        newGame_text_rect.center = (screen_width // 2, screen_height // 2 + 100)

        # Texte auf dem Bildschirm platzieren
        screen.blit(died_text, died_text_rect)
        screen.blit(newGame_text, newGame_text_rect)