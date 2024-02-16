def spawn_diamonds():
    global diamonds
    print("SPAWN")
    diamonds = []
    for _ in range(10):
        diamond = pygame.Rect(random.randint(0, screen_width - 40), random.randint(0, screen_height // 2), 40, 40)
        diamonds.append(diamond)