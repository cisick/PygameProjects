import random
import pygame
import os

pygame.init()

# Definiere Konstanten
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Ändere die Größe der Zellen auf die Größe der Bilder
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

# Erstelle das Pygame-Fenster
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

cell_images = [
    "cell_01.png",
    "cell_02.png",
    "cell_03.png",
    "cell_04.png",
    "cell_05.png",
    "cell_06.png"
]


def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])


# Ändere die Funktion, um zufällige Bilder zu zeichnen
def draw_grid_with_images(positions):
    for position in positions:
        col, row = position
        x = col * TILE_SIZE
        y = row * TILE_SIZE

        # Wähle zufällig ein Bild aus der Liste der Bilder
        selected_image = random.choice(cell_images)
        cell_image = pygame.image.load(selected_image)

        # Passe die Bildgröße an
        cell_image = pygame.transform.scale(cell_image, (TILE_SIZE, TILE_SIZE))
        screen.blit(cell_image, (x, y))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))

    return neighbors


def main():
    running = True
    playing = False
    count = 0
    update_freq = 120

    positions = set()

    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                # Press C to delete all cells & stop playing:
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                # Press G to randomly spawn cells:
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)
                    positions = {(col, row) for col, row in positions}

        screen.fill(GREY)
        draw_grid_with_images(positions)
        pygame.display.update()


if __name__ == "__main__":
    main()
