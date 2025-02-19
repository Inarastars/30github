import pygame
import random
import numpy as np
import sys

# Константы направлений
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Maze:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        # Для каждой ячейки: [верх, право, низ, лево] – True: стена есть
        self.walls = np.ones((rows, cols, 4), dtype=bool)
        self.visited = np.zeros((rows, cols), dtype=bool)
        self.generate_maze()

    def generate_maze(self):
        # Генерация лабиринта методом рекурсивного обхода (с использованием стека)
        stack = []
        current = (0, 0)
        self.visited[0, 0] = True
        stack.append(current)
        while stack:
            y, x = current
            neighbors = []
            if y > 0 and not self.visited[y - 1, x]:
                neighbors.append(((y - 1, x), UP))
            if x < self.cols - 1 and not self.visited[y, x + 1]:
                neighbors.append(((y, x + 1), RIGHT))
            if y < self.rows - 1 and not self.visited[y + 1, x]:
                neighbors.append(((y + 1, x), DOWN))
            if x > 0 and not self.visited[y, x - 1]:
                neighbors.append(((y, x - 1), LEFT))
            if neighbors:
                next_cell, direction = random.choice(neighbors)
                self.remove_wall((y, x), next_cell, direction)
                self.visited[next_cell[0], next_cell[1]] = True
                stack.append(current)
                current = next_cell
            else:
                current = stack.pop()

    def remove_wall(self, current, next_cell, direction):
        y, x = current
        ny, nx = next_cell
        if direction == UP:
            self.walls[y, x, UP] = False
            self.walls[ny, nx, DOWN] = False
        elif direction == RIGHT:
            self.walls[y, x, RIGHT] = False
            self.walls[ny, nx, LEFT] = False
        elif direction == DOWN:
            self.walls[y, x, DOWN] = False
            self.walls[ny, nx, UP] = False
        elif direction == LEFT:
            self.walls[y, x, LEFT] = False
            self.walls[ny, nx, RIGHT] = False

    def draw(self, surface):
        # Отрисовка стен лабиринта
        for y in range(self.rows):
            for x in range(self.cols):
                cx = x * self.cell_size
                cy = y * self.cell_size
                if self.walls[y, x, UP]:
                    pygame.draw.line(surface, (255, 255, 255), (cx, cy), (cx + self.cell_size, cy), 2)
                if self.walls[y, x, RIGHT]:
                    pygame.draw.line(surface, (255, 255, 255), (cx + self.cell_size, cy),
                                     (cx + self.cell_size, cy + self.cell_size), 2)
                if self.walls[y, x, DOWN]:
                    pygame.draw.line(surface, (255, 255, 255), (cx + self.cell_size, cy + self.cell_size),
                                     (cx, cy + self.cell_size), 2)
                if self.walls[y, x, LEFT]:
                    pygame.draw.line(surface, (255, 255, 255), (cx, cy + self.cell_size), (cx, cy), 2)


class MazeGame:
    def __init__(self, level=1):
        self.level = level
        self.init_level()
        self.player_pos = [0, 0]  # позиция игрока в ячейках: [строка, столбец]

    def init_level(self):
        # Размер лабиринта увеличивается с каждым уровнем: базово 10x10, затем +2 ячейки за уровень
        self.rows = 10 + (self.level - 1) * 2
        self.cols = 10 + (self.level - 1) * 2
        self.cell_size = 40  # размер ячейки в пикселях
        self.maze = Maze(self.rows, self.cols, self.cell_size)
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Maze Game - Уровень {self.level}")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)  # 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.draw()
            pygame.display.flip()

            # Если игрок достиг нижнего правого угла – переходим на следующий уровень
            if self.player_pos == [self.rows - 1, self.cols - 1]:
                pygame.time.delay(500)
                self.level += 1
                self.player_pos = [0, 0]
                self.init_level()
        pygame.quit()
        sys.exit()

    def handle_key(self, key):
        r, c = self.player_pos
        # Перемещение игрока осуществляется, если соответствующая стена отсутствует
        if key == pygame.K_UP and r > 0:
            if not self.maze.walls[r, c, UP]:
                self.player_pos[0] -= 1
        elif key == pygame.K_DOWN and r < self.rows - 1:
            if not self.maze.walls[r, c, DOWN]:
                self.player_pos[0] += 1
        elif key == pygame.K_LEFT and c > 0:
            if not self.maze.walls[r, c, LEFT]:
                self.player_pos[1] -= 1
        elif key == pygame.K_RIGHT and c < self.cols - 1:
            if not self.maze.walls[r, c, RIGHT]:
                self.player_pos[1] += 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        # Отрисовка игрока – красный круг в центре текущей ячейки
        r, c = self.player_pos
        cx = c * self.cell_size + self.cell_size // 2
        cy = r * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, (255, 0, 0), (cx, cy), self.cell_size // 3)


def main():
    pygame.init()
    game = MazeGame(level=1)
    game.run()


if __name__ == "__main__":
    main()
