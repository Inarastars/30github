import pygame

# Инициализация Pygame
pygame.init()

# Размер окна
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 40  # Размер одной клетки

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)  # Игрок
GREEN = (50, 200, 50)  # Выход

# Лабиринт (1 — стена, 0 — путь)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Координаты игрока (стартовая позиция)
player_x, player_y = 1, 1

# Координаты выхода
exit_x, exit_y = 8, 8

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт")

# Основной цикл игры
running = True
while running:
    pygame.time.delay(100)  # Задержка для управления скоростью игры
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and maze[player_y][player_x - 1] == 0:
        player_x -= 1
    if keys[pygame.K_RIGHT] and maze[player_y][player_x + 1] == 0:
        player_x += 1
    if keys[pygame.K_UP] and maze[player_y - 1][player_x] == 0:
        player_y -= 1
    if keys[pygame.K_DOWN] and maze[player_y + 1][player_x] == 0:
        player_y += 1

    # Отрисовка лабиринта
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            color = BLACK if maze[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка игрока
    pygame.draw.rect(screen, RED, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка выхода
    pygame.draw.rect(screen, GREEN, (exit_x * CELL_SIZE, exit_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Проверка победы
    if player_x == exit_x and player_y == exit_y:
        print("Ты выиграл!")
        running = False

    pygame.display.update()

pygame.quit()
