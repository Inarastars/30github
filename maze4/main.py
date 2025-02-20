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
    def __init__(self, difficulty):
        self.set_difficulty(difficulty)
        self.player_pos = [0, 0]  # позиция игрока: [строка, столбец]

    def set_difficulty(self, difficulty):
        if difficulty == 1:
            self.rows, self.cols = 10, 10
        elif difficulty == 2:
            self.rows, self.cols = 20, 20
        elif difficulty == 3:
            self.rows, self.cols = 30, 30
        self.cell_size = 40  # размер ячейки в пикселях
        self.maze = Maze(self.rows, self.cols, self.cell_size)
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Maze Game - Уровень сложности {difficulty}")

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

            # Если игрок достиг нижнего правого угла – завершаем игру
            if self.player_pos == [self.rows - 1, self.cols - 1]:
                pygame.time.delay(500)
                print("Поздравляем! Вы прошли лабиринт!")
                running = False
        pygame.quit()
        sys.exit()

    def handle_key(self, key):
        r, c = self.player_pos
        if key == pygame.K_UP and r > 0 and not self.maze.walls[r, c, UP]:
            self.player_pos[0] -= 1
        elif key == pygame.K_DOWN and r < self.rows - 1 and not self.maze.walls[r, c, DOWN]:
            self.player_pos[0] += 1
        elif key == pygame.K_LEFT and c > 0 and not self.maze.walls[r, c, LEFT]:
            self.player_pos[1] -= 1
        elif key == pygame.K_RIGHT and c < self.cols - 1 and not self.maze.walls[r, c, RIGHT]:
            self.player_pos[1] += 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        # Отрисовка игрока – красный круг в центре текущей ячейки
        r, c = self.player_pos
        cx = c * self.cell_size + self.cell_size // 2
        cy = r * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, (255, 0, 0), (cx, cy), self.cell_size // 3)

def show_menu():
    menu_width, menu_height = 640, 480
    screen = pygame.display.set_mode((menu_width, menu_height))
    pygame.display.set_caption("Maze Game - Выбор уровня сложности")
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)

    title_text = title_font.render("Выберите уровень сложности", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(menu_width // 2, 100))

    options = [("Легкий", 1), ("Средний", 2), ("Сложный", 3)]
    option_rects = []
    for i, (option_text, diff) in enumerate(options):
        text_surface = font.render(option_text, True, (255, 255, 255))
        rect = text_surface.get_rect(center=(menu_width // 2, 200 + i * 60))
        option_rects.append((option_text, rect, diff))

    selected_difficulty = None
    while selected_difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for text, rect, diff in option_rects:
                    if rect.collidepoint(pos):
                        selected_difficulty = diff
                        break

        screen.fill((0, 0, 0))
        screen.blit(title_text, title_rect)
        for text, rect, diff in option_rects:
            # Изменение цвета при наведении курсора
            if rect.collidepoint(pygame.mouse.get_pos()):
                rendered_text = font.render(text, True, (255, 0, 0))
            else:
                rendered_text = font.render(text, True, (255, 255, 255))
            screen.blit(rendered_text, rect)
        pygame.display.flip()
    return selected_difficulty

def main():
    pygame.init()
    difficulty = show_menu()  # Запуск меню для выбора сложности
    game = MazeGame(difficulty)
    game.run()

if __name__ == "__main__":
    main()
