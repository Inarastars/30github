import pygame
import random
import numpy as np
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Maze Game")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
clock = pygame.time.Clock()

# Параметры лабиринта:
CELL_SIZE = 20
MAZE_WIDTH = screen.get_width() // CELL_SIZE
MAZE_HEIGHT = screen.get_height() // CELL_SIZE


def generate_maze(width, height):
    """
    Генерирует лабиринт с использованием алгоритма рекурсивного backtracking.
    В этой версии стартовая позиция фиксирована в (1, 1), а финиш – в (width-2, height-2).
    """
    maze = np.ones((height, width), dtype=int)

    # Фиксированный старт:
    start_x, start_y = 1, 1
    maze[start_y, start_x] = 0
    stack = [(start_x, start_y)]

    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny, nx] == 1:
                neighbors.append((nx, ny, dx, dy))
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[ny, nx] = 0
            maze[y + dy // 2, x + dx // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    # Финиш – фиксирован в правом нижнем углу (напротив начала)
    finish_x, finish_y = width - 2, height - 2
    maze[finish_y, finish_x] = 0
    return maze, (start_x, start_y), (finish_x, finish_y)


def draw_maze(maze):
    for y in range(maze.shape[0]):
        for x in range(maze.shape[1]):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y, x] == 1:
                pygame.draw.rect(screen, (255, 255, 255), rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect)


def draw_entities(player_pos, finish):
    # Финиш – зеленый квадрат
    finish_rect = pygame.Rect(finish[0] * CELL_SIZE, finish[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, (0, 255, 0), finish_rect)
    # Игрок – красный квадрат
    player_rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, (255, 0, 0), player_rect)


def save_level(maze, start, finish, level):
    filename = f"maze_level_{level}.npz"
    np.savez(filename, maze=maze, start=start, finish=finish)
    print(f"Уровень {level} сохранен в {filename}")


def load_level(level):
    filename = f"maze_level_{level}.npz"
    if os.path.exists(filename):
        data = np.load(filename)
        maze = data['maze']
        start = tuple(data['start'])
        finish = tuple(data['finish'])
        print(f"Уровень {level} загружен из {filename}")
        return maze, start, finish
    else:
        print(f"Файл {filename} не найден. Генерация нового лабиринта.")
        return generate_maze(MAZE_WIDTH, MAZE_HEIGHT)


def game_loop():
    level = 1
    maze, start, finish = load_level(level)
    # Игрок стартует в фиксированной позиции
    player_pos = list(start)
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_level(maze, start, finish, level)
                running = False
            elif event.type == pygame.KEYDOWN:
                new_pos = list(player_pos)
                if event.key == pygame.K_LEFT:
                    new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    new_pos[0] += 1
                elif event.key == pygame.K_UP:
                    new_pos[1] -= 1
                elif event.key == pygame.K_DOWN:
                    new_pos[1] += 1
                elif event.key == pygame.K_n:
                    level += 1
                    maze, start, finish = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
                    player_pos = list(start)
                    continue
                if (0 <= new_pos[0] < MAZE_WIDTH and 0 <= new_pos[1] < MAZE_HEIGHT and
                        maze[new_pos[1], new_pos[0]] == 0):
                    player_pos = new_pos

        if tuple(player_pos) == finish:
            print("Уровень пройден!")
            save_level(maze, start, finish, level)
            level += 1
            maze, start, finish = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
            player_pos = list(start)

        screen.blit(background, (0, 0))
        draw_maze(maze)
        draw_entities(player_pos, finish)
        pygame.display.flip()


game_loop()
pygame.quit()
