import numpy as np
import random
import pygame
from copy import deepcopy


class SudokuGame:
    def __init__(self):
        pygame.init()
        self.window_size = 540
        self.cell_size = self.window_size // 9
        self.toolbar_height = 60
        self.screen = pygame.display.set_mode((self.window_size, self.window_size + self.toolbar_height * 2))
        pygame.display.set_caption("Судоку")
        self.font = pygame.font.Font(None, 40)
        self.pencil_font = pygame.font.Font(None, 20)
        self.menu_font = pygame.font.Font(None, 50)
        self.selected = None
        self.lives = 3
        self.level = 1
        self.difficulty = None
        self.is_menu_active = True
        self.pencil_mode = False
        self.pencil_marks = [[set() for _ in range(9)] for _ in range(9)]
        self.board = None
        self.solution = None
        self.original_board = None

        # Инициализация кнопок для ручки и карандаша
        self.pen_rect = pygame.Rect(self.window_size // 2 - 60, self.window_size + self.toolbar_height + 10, 40, 40)
        self.pencil_rect = pygame.Rect(self.window_size // 2 + 20, self.window_size + self.toolbar_height + 10, 40, 40)

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

        # Рамки для кнопок
        pygame.draw.rect(self.screen, (0, 128, 0), easy_rect.inflate(20, 10), 2)
        pygame.draw.rect(self.screen, (255, 165, 0), medium_rect.inflate(20, 10), 2)
        pygame.draw.rect(self.screen, (255, 0, 0), hard_rect.inflate(20, 10), 2)

        return easy_rect, medium_rect, hard_rect

    def draw_toolbar(self):
        # Отрисовка панели инструментов
        toolbar_rect = pygame.Rect(0, self.window_size + self.toolbar_height, self.window_size, self.toolbar_height)
        pygame.draw.rect(self.screen, (240, 240, 240), toolbar_rect)

        # Отрисовка кнопок ручки и карандаша
        pygame.draw.rect(self.screen, (200, 200, 200) if not self.pencil_mode else (255, 255, 255), self.pen_rect)
        pen_text = self.font.render("✒️", True, (0, 0, 0))
        pen_rect = pen_text.get_rect(center=self.pen_rect.center)
        self.screen.blit(pen_text, pen_rect)

        pygame.draw.rect(self.screen, (200, 200, 200) if self.pencil_mode else (255, 255, 255), self.pencil_rect)
        pencil_text = self.font.render("✎", True, (0, 0, 0))
        pencil_rect = pencil_text.get_rect(center=self.pencil_rect.center)
        self.screen.blit(pencil_text, pencil_rect)

        pygame.draw.rect(self.screen, (0, 0, 0), self.pen_rect, 2)
        pygame.draw.rect(self.screen, (0, 0, 0), self.pencil_rect, 2)

        # Текст режима
        mode_text = "Режим: Карандаш" if self.pencil_mode else "Режим: Ручка"
        mode_surface = self.font.render(mode_text, True, (0, 0, 0))
        mode_rect = mode_surface.get_rect(center=(self.window_size // 2, self.window_size + self.toolbar_height - 20))
        self.screen.blit(mode_surface, mode_rect)

    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        # Верхняя панель для hearts и уровня
        pygame.draw.rect(self.screen, (240, 240, 240), (0, 0, self.window_size, self.toolbar_height))
        self.draw_hearts()
        self.draw_level()

        # Отрисовка линий сетки
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            # Вертикальные линии
            pygame.draw.line(self.screen, (0, 0, 0),
                             (i * self.cell_size, self.toolbar_height),
                             (i * self.cell_size, self.window_size + self.toolbar_height), line_width)
            # Горизонтальные линии
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, i * self.cell_size + self.toolbar_height),
                             (self.window_size, i * self.cell_size + self.toolbar_height), line_width)
        self.highlight_selected()

    def highlight_selected(self):
        if self.selected is not None:
            row, col = self.selected
            # Создаем полупрозрачный поверхностный слой для подсветки (серый с альфа-каналом 100 из 255)
            highlight_color = (128, 128, 128, 100)
            selected_border_color = (255, 255, 0)  # Цвет обводки выбранной ячейки

            # Подсветка строки
            row_surf = pygame.Surface((self.window_size, self.cell_size), pygame.SRCALPHA)
            row_surf.fill(highlight_color)
            self.screen.blit(row_surf, (0, row * self.cell_size + self.toolbar_height))

            # Подсветка столбца
            col_surf = pygame.Surface((self.cell_size, self.window_size), pygame.SRCALPHA)
            col_surf.fill(highlight_color)
            self.screen.blit(col_surf, (col * self.cell_size, self.toolbar_height))

            # Обводка выбранной ячейки
            pygame.draw.rect(self.screen, selected_border_color,
                             (col * self.cell_size,
                              row * self.cell_size + self.toolbar_height,
                              self.cell_size, self.cell_size), 3)

    def draw_numbers(self):
        if self.board is None:
            return
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    # Если число было изначально, рисуем чёрным, иначе синим
                    color = (0, 0, 0) if self.original_board[i][j] != 0 else (0, 0, 255)
                    number = self.font.render(str(self.board[i][j]), True, color)
                    x = j * self.cell_size + (self.cell_size - number.get_width()) // 2
                    y = i * self.cell_size + self.toolbar_height + (self.cell_size - number.get_height()) // 2
                    self.screen.blit(number, (x, y))

    def draw_pencil_marks(self):
        for i in range(9):
            for j in range(9):
                if self.pencil_marks[i][j]:
                    marks = sorted(list(self.pencil_marks[i][j]))
                    for idx, mark in enumerate(marks):
                        row_offset = idx // 3
                        col_offset = idx % 3
                        x = j * self.cell_size + col_offset * (self.cell_size // 3) + 5
                        y = i * self.cell_size + self.toolbar_height + row_offset * (self.cell_size // 3) + 2
                        mark_text = self.pencil_font.render(str(mark), True, (128, 128, 128))
                        self.screen.blit(mark_text, (x, y))

    def generate_base(self):
        base = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for row in range(3):
                for col in range(3):
                    base[row + i][col + i] = nums[row * 3 + col]

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
        # Проверка строки и столбца
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        # Проверка блока 3×3
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def generate_puzzle(self, difficulty):
        solution = self.generate_base()
        puzzle = [row[:] for row in solution]

        if difficulty == "easy":
            cells_to_remove = 30
        elif difficulty == "medium":
            cells_to_remove = 40
        else:  # hard
            cells_to_remove = 50

        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        for i, j in positions[:cells_to_remove]:
            puzzle[i][j] = 0

        return np.array(puzzle), np.array(solution)

    def create_new_game(self):
        self.board, self.solution = self.generate_puzzle(self.difficulty)
        self.original_board = deepcopy(self.board)
        self.pencil_marks = [[set() for _ in range(9)] for _ in range(9)]
        self.lives = 3
        self.level = 1
        self.is_menu_active = False

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

    def draw_hearts(self):
        for i in range(3):
            if i < self.lives:
                pygame.draw.polygon(self.screen, (255, 0, 0), [
                    (50 + i * 40, 20),
                    (60 + i * 40, 10),
                    (70 + i * 40, 20),
                    (60 + i * 40, 30)
                ])
            else:
                pygame.draw.polygon(self.screen, (128, 128, 128), [
                    (50 + i * 40, 20),
                    (59 + i * 40, 10),
                    (60 + i * 40, 20),
                    (59 + i * 40, 30)
                ])
                pygame.draw.polygon(self.screen, (128, 128, 128), [
                    (61 + i * 40, 10),
                    (70 + i * 40, 20),
                    (61 + i * 40, 30),
                    (60 + i * 40, 20)
                ])

    def draw_level(self):
        level_text = self.font.render(f"Уровень: {self.level}", True, (0, 0, 0))
        self.screen.blit(level_text, (self.window_size - 150, 15))

    def update_screen(self):
        self.draw_grid()
        self.draw_numbers()
        self.draw_pencil_marks()
        self.draw_toolbar()
        pygame.display.flip()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(30)  # Ограничение до 30 FPS
            if self.is_menu_active:
                easy_rect, medium_rect, hard_rect = self.draw_menu()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if easy_rect.collidepoint(mouse_pos):
                            self.difficulty = "easy"
                            self.create_new_game()
                        elif medium_rect.collidepoint(mouse_pos):
                            self.difficulty = "medium"
                            self.create_new_game()
                        elif hard_rect.collidepoint(mouse_pos):
                            self.difficulty = "hard"
                            self.create_new_game()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        # Проверка нажатия кнопок ручки/карандаша
                        if self.pen_rect.collidepoint(pos):
                            self.pencil_mode = False
                        elif self.pencil_rect.collidepoint(pos):
                            self.pencil_mode = True
                        else:
                            # Если клик в области сетки, определяем выбранную ячейку
                            if pos[1] >= self.toolbar_height and pos[1] <= self.window_size + self.toolbar_height:
                                col = pos[0] // self.cell_size
                                row = (pos[1] - self.toolbar_height) // self.cell_size
                                self.selected = (row, col)
                    if event.type == pygame.KEYDOWN and self.selected is not None:
                        if event.unicode.isdigit() and event.unicode != '0':
                            num = int(event.unicode)
                            row, col = self.selected
                            if self.pencil_mode:
                                # Добавляем или удаляем карандашную запись
                                if num in self.pencil_marks[row][col]:
                                    self.pencil_marks[row][col].remove(num)
                                else:
                                    self.pencil_marks[row][col].add(num)
                            else:
                                # В режиме ручки проверяем, можно ли ставить число (только если ячейка не изначальная)
                                if self.original_board[row][col] == 0:
                                    if num == self.solution[row][col]:
                                        self.board[row][col] = num
                                        self.pencil_marks[row][col] = set()
                                        self.check_level_complete()
                                    else:
                                        self.lives -= 1
                            self.selected = None
                self.update_screen()
                if self.check_game_over():
                    running = False
        pygame.quit()


if __name__ == "__main__":
    game = SudokuGame()
    game.run()
