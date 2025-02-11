import numpy as np
import random
import pygame
from copy import deepcopy


class SudokuGame:
    def __init__(self):
        pygame.init()
        self.window_size = 540
        self.cell_size = self.window_size // 9
        self.screen = pygame.display.set_mode((self.window_size, self.window_size + 60))
        pygame.display.set_caption("Судоку")
        self.font = pygame.font.Font(None, 40)
        self.menu_font = pygame.font.Font(None, 50)
        self.selected = None
        self.lives = 3
        self.level = 1
        self.difficulty = None
        self.show_menu = True

    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        title = self.menu_font.render("Выберите сложность:", True, (0, 0, 0))
        easy = self.menu_font.render("Легкий", True, (0, 128, 0))
        medium = self.menu_font.render("Средний", True, (255, 165, 0))
        hard = self.menu_font.render("Сложный", True, (255, 0, 0))

        title_rect = title.get_rect(center=(self.window_size // 2, 150))
        easy_rect = easy.get_rect(center=(self.window_size // 2, 250))
        medium_rect = medium.get_rect(center=(self.window_size // 2, 350))
        hard_rect = hard.get_rect(center=(self.window_size // 2, 450))

        self.screen.blit(title, title_rect)
        self.screen.blit(easy, easy_rect)
        self.screen.blit(medium, medium_rect)
        self.screen.blit(hard, hard_rect)

        return easy_rect, medium_rect, hard_rect

    def generate_base(self):
        """Генерирует базовую решенную сетку судоку"""
        base = [[0 for x in range(9)] for y in range(9)]

        # Заполняем диагональные блоки 3x3
        for i in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for row in range(3):
                for col in range(3):
                    base[row + i][col + i] = nums[row * 3 + col]

        # Решаем остальную часть головоломки
        def solve_grid(grid):
            for row in range(9):
                for col in range(9):
                    if grid[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid_full(grid, row, col, num):
                                grid[row][col] = num
                                if solve_grid(grid):
                                    return True
                                grid[row][col] = 0
                        return False
            return True

        solve_grid(base)
        return base

    def is_valid_full(self, grid, row, col, num):
        """Проверяет, можно ли поставить число в данную позицию"""
        # Проверка строки
        for x in range(9):
            if grid[row][x] == num:
                return False

        # Проверка столбца
        for x in range(9):
            if grid[x][col] == num:
                return False

        # Проверка блока 3x3
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def generate_puzzle(self, difficulty):
        """Генерирует головоломку судоку заданной сложности"""
        # Создаем решенную сетку
        solution = self.generate_base()
        puzzle = [row[:] for row in solution]

        # Определяем количество пустых клеток в зависимости от сложности
        if difficulty == "easy":
            cells_to_remove = 30
        elif difficulty == "medium":
            cells_to_remove = 40
        else:  # hard
            cells_to_remove = 50

        # Удаляем числа
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)

        for i, j in positions[:cells_to_remove]:
            puzzle[i][j] = 0

        return np.array(puzzle), np.array(solution)

    def create_new_game(self):
        self.board, self.solution = self.generate_puzzle(self.difficulty)
        self.original_board = deepcopy(self.board)
        self.lives = 3
        self.level = 1

    def is_valid(self, board, row, col, num):
        return self.is_valid_full(board.tolist(), row, col, num)

    def draw_hearts(self):
        heart_size = 20
        for i in range(3):
            color = (255, 0, 0) if i < self.lives else (0, 0, 0)
            pygame.draw.polygon(self.screen, color, [
                (50 + i * 40, 20),
                (60 + i * 40, 10),
                (70 + i * 40, 20),
                (60 + i * 40, 30)
            ])

    def draw_level(self):
        level_text = self.font.render(f"Уровень: {self.level}", True, (0, 0, 0))
        self.screen.blit(level_text, (self.window_size - 150, 15))

    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (240, 240, 240), (0, 0, self.window_size, 60))
        self.draw_hearts()
        self.draw_level()

        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0),
                             (i * self.cell_size, 60),
                             (i * self.cell_size, self.window_size + 60), line_width)
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, i * self.cell_size + 60),
                             (self.window_size, i * self.cell_size + 60), line_width)

    def draw_numbers(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    color = (0, 0, 255) if self.original_board[i][j] == 0 else (0, 0, 0)
                    number = self.font.render(str(self.board[i][j]), True, color)
                    x = j * self.cell_size + (self.cell_size - number.get_width()) // 2
                    y = i * self.cell_size + 60 + (self.cell_size - number.get_height()) // 2
                    self.screen.blit(number, (x, y))

    def highlight_selected(self):
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(self.screen, (255, 255, 0),
                             (col * self.cell_size, row * self.cell_size + 60,
                              self.cell_size, self.cell_size), 3)

    def check_game_over(self):
        if self.lives <= 0:
            game_over_text = self.font.render(f"Игра окончена! Уровень: {self.level}", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.window_size // 4, self.window_size // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            return True
        return False

    def check_level_complete(self):
        if np.array_equal(self.board, self.solution):
            self.level += 1
            self.board, self.solution = self.generate_puzzle(self.difficulty)
            self.original_board = deepcopy(self.board)
            self.lives = 3

    def run(self):
        running = True
        while running:
            if self.show_menu:
                easy_rect, medium_rect, hard_rect = self.draw_menu()
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if easy_rect.collidepoint(mouse_pos):
                            self.difficulty = "easy"
                            self.show_menu = False
                            self.create_new_game()
                        elif medium_rect.collidepoint(mouse_pos):
                            self.difficulty = "medium"
                            self.show_menu = False
                            self.create_new_game()
                        elif hard_rect.collidepoint(mouse_pos):
                            self.difficulty = "hard"
                            self.show_menu = False
                            self.create_new_game()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if pos[1] > 60:
                            col = pos[0] // self.cell_size
                            row = (pos[1] - 60) // self.cell_size
                            self.selected = (row, col)
                    if event.type == pygame.KEYDOWN and self.selected:
                        row, col = self.selected
                        if self.original_board[row][col] == 0:
                            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3,
                                             pygame.K_4, pygame.K_5, pygame.K_6,
                                             pygame.K_7, pygame.K_8, pygame.K_9]:
                                num = int(event.unicode)
                                if num != self.solution[row][col]:
                                    self.lives -= 1
                                    if self.check_game_over():
                                        self.show_menu = True
                                        self.selected = None
                                else:
                                    self.board[row][col] = num
                                    self.check_level_complete()
                            elif event.key == pygame.K_BACKSPACE:
                                self.board[row][col] = 0

                self.draw_grid()
                self.draw_numbers()
                self.highlight_selected()
                pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = SudokuGame()
    game.run()