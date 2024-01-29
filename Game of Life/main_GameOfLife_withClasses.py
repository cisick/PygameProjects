import random
import pygame

pygame.init()

test_font = pygame.font.Font('font/Pixeltype.ttf', 30)
titel_font = pygame.font.Font('font/Pixeltype.ttf', 120)

BLACK = (0, 0, 0)
GREY = (128, 128, 128)

WIDTH, HEIGHT = 700, 700
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60
start_time = 0
generation = 0
alive = 0
died = 0
born = 0

# Erstelle das Pygame-Fenster
screen = pygame.display.set_mode((WIDTH + 300, HEIGHT + 80))
clock = pygame.time.Clock()

cell_images = [
    "cell_01.png",
    "cell_02.png",
    "cell_03.png",
    "cell_04.png",
    "cell_05.png",
    "cell_06.png"
]


def display_score():
    # Titel
    score_titel_part1_surf = titel_font.render(f'Game', False, (64, 64, 64))
    score_titel_part1_rect = score_titel_part1_surf.get_rect(midright=(800, 100))
    score_titel_part2_surf = titel_font.render(f'of', False, (64, 64, 64))
    score_titel_part2rect = score_titel_part2_surf.get_rect(midright=(800, 200))
    score_titel_part3_surf = titel_font.render(f'Life', False, (64, 64, 64))
    score_titel_part3rect = score_titel_part2_surf.get_rect(midright=(800, 300))

    screen.blit(score_titel_part1_surf, (800, 100))
    screen.blit(score_titel_part2_surf, (800, 200))
    screen.blit(score_titel_part3_surf, (800, 300))

    # Zeichnen Sie eine orange Linie von (100, 100) nach (300, 300) mit einer Dicke von 5 Pixeln
    pygame.draw.line(screen, (255, 165, 0), (705, 0), (705, 705), 5)
    pygame.draw.line(screen, (255, 165, 0), (0, 705), (1100, 705), 5)
    pygame.draw.line(screen, (255, 165, 0), (0, 775), (1100, 775), 5)

    # Erstellen der Bild-Objekte
    time_image = pygame.image.load('time_image.png')
    time_image = pygame.transform.scale(time_image, (40, 40))

    generations_image = pygame.image.load('generations_image.png')
    generations_image = pygame.transform.scale(generations_image, (40, 40))

    alive_image = pygame.image.load('alive_image.png')
    alive_image = pygame.transform.scale(alive_image, (40, 40))

    died_image = pygame.image.load('died_image.png')
    died_image = pygame.transform.scale(died_image, (40, 40))

    born_image = pygame.image.load('born_image.png')
    born_image = pygame.transform.scale(born_image, (40, 40))

    # Zeichnen der Bilder vor den Wörtern
    y0 = 720
    y1 = y0
    y2 = y1
    y3 = y1
    y4 = y1

    space_picuture = 200
    space_text = 20

    x0 = 20
    x1 = x0 + space_picuture
    x2 = x1 + space_picuture
    x3 = x2 + space_picuture
    x4 = x3 + space_picuture

    screen.blit(time_image, (x0, y0))  # Bild 0
    screen.blit(generations_image, (x1, y1))  # Bild 1
    screen.blit(alive_image, (x2, y2))  # Bild 2
    screen.blit(died_image, (x3, y3))  # Bild 3
    screen.blit(born_image, (x4, y4))  # Bild 4

    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    # Position des Texts
    text_run_time_x = x0 + time_image.get_width() + 10  # Passen Sie die Position an
    text_run_time_y = y0  # Passen Sie die Position an

    text_generation_x = x1 + time_image.get_width() + 10  # Passen Sie die Position an
    text_generation_y = y1  # Passen Sie die Position an

    text_alive_x = x2 + alive_image.get_width() + 10  # Passen Sie die Position an
    text_alive_y = y2  # Passen Sie die Position an

    text_died_x = x3 + alive_image.get_width() + 10  # Passen Sie die Position an
    text_died_y = y3  # Passen Sie die Position an

    text_born_x = x4 + alive_image.get_width() + 10  # Passen Sie die Position an
    text_born_y = y4  # Passen Sie die Position an

    # Zeichnen des Texts

    if current_time < 60:
        score_run_time_surf = test_font.render(f'running: {current_time} sec', False, (64, 64, 64))
    else:
        score_run_time_surf = test_font.render(f'running: {int(current_time / 60)} min', False, (64, 64, 64))

    score_run_time_rect = score_run_time_surf.get_rect(midleft=(text_run_time_x, text_run_time_y))

    score_generation_surf = test_font.render(f'Generation: {generation} ', False, (64, 64, 64))
    score_generation_rect = score_generation_surf.get_rect(midleft=(text_generation_x, text_generation_y))

    score_alive_surf = test_font.render(f'alive: {alive} ', False, (64, 64, 64))
    score_alive_rect = score_alive_surf.get_rect(midleft=(text_alive_x, text_alive_y))

    score_died_surf = test_font.render(f'died: {died}', False, (64, 64, 64))
    score_died_rect = score_died_surf.get_rect(midleft=(text_died_x, text_died_y))

    score_born_surf = test_font.render(f'born: {born}', False, (64, 64, 64))
    score_born_rect = score_born_surf.get_rect(midleft=(text_born_x, text_born_y))

    # Anzeigen des Textes an der GUI
    screen.blit(score_run_time_surf, (text_run_time_x, text_run_time_y))
    screen.blit(score_generation_surf, (text_generation_x, text_generation_y))
    screen.blit(score_alive_surf, (text_alive_x, text_alive_y))
    screen.blit(score_died_surf, (text_died_x, text_died_y))
    screen.blit(score_born_surf, (text_born_x, text_born_y))


def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])


# Ändere die Funktion, um zufällige Bilder zu zeichnen
def draw_grid_with_images(positions, grid, images):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            cell_position = (col, row)

            # Überprüfe, ob das Bild an dieser Position bereits festgelegt ist
            if cell_position in positions:

                if grid[row][col] is None:
                    selected_image = random.choice(images)
                    cell_image = pygame.image.load(selected_image)
                    cell_image = pygame.transform.scale(cell_image, (TILE_SIZE, TILE_SIZE))
                    grid[row][col] = (cell_image, selected_image)
                else:
                    cell_image, _ = grid[row][col]
                screen.blit(cell_image, (x, y))

            else:
                grid[row][col] = None  # Zurücksetzen des Bilds an dieser Position auf None

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def adjust_grid(positions):
    global generation
    global born
    global died
    global alive

    all_neighbors = set()
    new_positions = set()

    generation += 1

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)
            born += 1

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)
            born += 1
    global died

    if len(positions) > len(new_positions):
        died += len(positions) - len(new_positions)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if 0 <= x + dx < GRID_WIDTH:
            for dy in [-1, 0, 1]:
                if 0 <= y + dy < GRID_HEIGHT and not (dx == 0 and dy == 0):
                    neighbors.append((x + dx, y + dy))

    return neighbors


def main():
    running = True
    playing = False
    count = 0

    positions = set()
    grid = [[None for i in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= FPS:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Game of Life - Playing" if playing else "Game of Life - Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if x <= 699 and y <= 699:
                    if pos in positions:
                        positions.remove(pos)
                        global died
                        died += 1
                    else:
                        positions.add(pos)
                        global born
                        born += 1

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

                    global generation
                    generation = 1
                    born = 0
                    died = 0

        screen.fill(GREY)

        display_score()

        global alive
        alive = len(positions)

        draw_grid_with_images(positions, grid, cell_images)
        pygame.display.update()


if __name__ == "__main__":
    main()


class cell:
    # Konstruktor-Methode
    def __init__(self, wert):
        self.wert = wert

    # Eine Methode der Klasse
    def anzeigen(self):
        print("Der Wert ist:", self.wert)


# Eine Instanz der Klasse erstellen
cell1 = cell(42)

# Auf Methoden und Attribute der Instanz zugreifen
cell1.anzeigen()
print("Der Wert des Objekts ist:", cell1 .wert)