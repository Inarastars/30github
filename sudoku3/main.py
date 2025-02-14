import numpy as np
import random
import pygame
from copy import deepcopy

class SudokuGame:
    def __init__(self):
        pygame.init()
        self.window_size = 540
        self.cell_size = self.window_size // 9
        self.toolbar_height = 60  # высота верхней панели
        # Общее окно: верхняя панель, игровое поле, нижняя панель для цифр
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

        # Попытка загрузить изображение фона главного меню и картинки для фона
        try:
            self.bg_menu_image = pygame.image.load("assets/bg_menu.png").convert()
        except Exception as e:
            self.bg_menu_image = None

        try:
            self.pencil_img = pygame.image.load("assets/pencil.png").convert_alpha()
        except Exception as e:
            self.pencil_img = None

        try:
            self.pen_img = pygame.image.load("assets/pen.png").convert_alpha()
        except Exception as e:
            self.pen_img = None

        # Переключатель: располагается по центру верхней панели
        self.toggle_width = 80
        self.toggle_height = 30
        self.toggle_x = (self.window_size - self.toggle_width) // 2
        self.toggle_y = (self.toolbar_height - self.toggle_height) // 2

        # Элементы для фонового декора главного меню: случайные позиции, размеры и типы
        self.background_elements = self.generate_background_elements()

        # Счетчик оставшихся цифр
        self.remaining_numbers = {i: 9 for i in range(1, 10)}

    def generate_background_elements(self):
        elements = []
        for _ in range(20):  # количество фоновых элементов
            x = random.randint(0, self.window_size - 50)
            y = random.randint(0, self.window_size + self.toolbar_height * 2 - 50)
            elem_type = random.choice(["digit", "pencil", "pen"])
            if elem_type == "digit":
                content = str(random.randint(1, 9))
            elif elem_type == "pencil":
                content = "pencil"  # будем пытаться рисовать картинку карандаша
            else:
                content = "pen"     # или картинки ручки
            size = random.randint(20, 60)
            alpha = random.randint(50, 100)
            elements.append((x, y, content, size, alpha))
        return elements

    def draw_menu_background(self):
        # Фон главного меню: если доступно изображение, используем его, иначе заливаем цветом
        if self.bg_menu_image:
            bg = pygame.transform.scale(self.bg_menu_image, (self.window_size, self.window_size + self.toolbar_height * 2))
            self.screen.blit(bg, (0, 0))
        else:
            self.screen.fill((220, 230, 250))
        # Наложение случайных фоновых элементов
        for x, y, content, size, alpha in self.background_elements:
            if content == "pencil" and self.pencil_img:
                img = pygame.transform.scale(self.pencil_img, (size, size))
                img.set_alpha(alpha)
                self.screen.blit(img, (x, y))
            elif content == "pen" and self.pen_img:
                img = pygame.transform.scale(self.pen_img, (size, size))
                img.set_alpha(alpha)
                self.screen.blit(img, (x, y))
            else:
                font = pygame.font.Font(None, size)
                text_surface = font.render(content, True, (150, 180, 230))
                text_surface.set_alpha(alpha)
                self.screen.blit(text_surface, (x, y))

    def draw_sudoku_background(self):
        # Заливка игрового поля с синим оттенком
        self.screen.fill((200, 220, 255))

    def draw_toggle(self):
        # Рисуем переключатель: овал с движущимся кругом и иконками
        toggle_rect = pygame.Rect(self.toggle_x, self.toggle_y, self.toggle_width, self.toggle_height)
        pygame.draw.ellipse(self.screen, (200, 200, 200), toggle_rect)
        circle_radius = self.toggle_height // 2 - 2
        if self.pencil_mode:
            circle_x = self.toggle_x + self.toggle_width - circle_radius - 2
        else:
            circle_x = self.toggle_x + circle_radius + 2
        circle_y = self.toggle_y + self.toggle_height // 2
        pygame.draw.circle(self.screen, (100, 100, 100), (circle_x, circle_y), circle_radius)
        # Рисуем иконки: слева – ручка, справа – карандаш
        pen_icon = self.pencil_font.render("✒️", True, (0, 0, 0))
        pencil_icon = self.pencil_font.render("✎", True, (0, 0, 0))
        pen_icon_rect = pen_icon.get_rect(center=(self.toggle_x + self.toggle_width // 4, self.toggle_y + self.toggle_height // 2))
        pencil_icon_rect = pencil_icon.get_rect(center=(self.toggle_x + 3 * self.toggle_width // 4, self.toggle_y + self.toggle_height // 2))
        self.screen.blit(pen_icon, pen_icon_rect)
        self.screen.blit(pencil_icon, pencil_icon_rect)

    def update_remaining_numbers(self):
        self.remaining_numbers = {i: 9 for i in range(1, 10)}
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.remaining_numbers[self.board[i][j]] -= 1

    def draw_remaining_numbers(self):
        number_width = self.window_size // 9
        for i in range(1, 10):
            number_surface = self.font.render(str(i), True, (0, 0, 0))
            x = (i - 1) * number_width + number_width // 2 - number_surface.get_width() // 2
            y = self.window_size + self.toolbar_height * 2 - 50
            self.screen.blit(number_surface, (x, y))
            remaining = self.remaining_numbers[i]
            remaining_surface = self.pencil_font.render(str(remaining), True, (100, 100, 100))
            x = (i - 1) * number_width + number_width // 2 - remaining_surface.get_width() // 2
            y += 25
            self.screen.blit(remaining_surface, (x, y))

    def draw_menu(self):
        # Рисуем фон главного меню с изображениями, затем пункты меню
        self.draw_menu_background()
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
        pygame.draw.rect(self.screen, (0, 128, 0), easy_rect.inflate(20, 10), 2)
        pygame.draw.rect(self.screen, (255, 165, 0), medium_rect.inflate(20, 10), 2)
        pygame.draw.rect(self.screen, (255, 0, 0), hard_rect.inflate(20, 10), 2)
        return easy_rect, medium_rect, hard_rect

    def draw_grid(self):
        # Верхняя панель: жизни, уровень и переключатель
        pygame.draw.rect(self.screen, (240, 240, 240), (0, 0, self.window_size, self.toolbar_height))
        self.draw_hearts()
        self.draw_level()
        self.draw_toggle()
        # Рисуем линии сетки судоку
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0),
                             (i * self.cell_size, self.toolbar_height),
                             (i * self.cell_size, self.window_size + self.toolbar_height), line_width)
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, i * self.cell_size + self.toolbar_height),
                             (self.window_size, i * self.cell_size + self.toolbar_height), line_width)
        self.highlight_selected()

    def highlight_selected(self):
        if self.selected is not None:
            row, col = self.selected
            highlight_color = (128, 128, 128, 100)
            selected_border_color = (255, 255, 0)
            row_surf = pygame.Surface((self.window_size, self.cell_size), pygame.SRCALPHA)
            row_surf.fill(highlight_color)
            self.screen.blit(row_surf, (0, row * self.cell_size + self.toolbar_height))
            col_surf = pygame.Surface((self.cell_size, self.window_size), pygame.SRCALPHA)
            col_surf.fill(highlight_color)
            self.screen.blit(col_surf, (col * self.cell_size, self.toolbar_height))
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
                    color = (0, 0, 0) if self.original_board[i][j] != 0 else (0, 0, 255)
                    number_surface = self.font.render(str(self.board[i][j]), True, color)
                    x = j * self.cell_size + (self.cell_size - number_surface.get_width()) // 2
                    y = i * self.cell_size + self.toolbar_height + (self.cell_size - number_surface.get_height()) // 2
                    self.screen.blit(number_surface, (x, y))

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
                        mark_surface = self.pencil_font.render(str(mark), True, (128, 128, 128))
                        self.screen.blit(mark_surface, (x, y))

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
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
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
        else:
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

    def draw_bottom_toolbar(self):
        bottom_rect = pygame.Rect(0, self.window_size + self.toolbar_height, self.window_size, self.toolbar_height)
        pygame.draw.rect(self.screen, (240, 240, 240), bottom_rect)

    def update_screen(self):
        self.draw_sudoku_background()
        self.draw_grid()
        self.draw_numbers()
        self.draw_pencil_marks()
        self.draw_bottom_toolbar()
        if self.board is not None:
            self.update_remaining_numbers()
            self.draw_remaining_numbers()
        pygame.display.flip()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(30)
            if self.is_menu_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        easy_rect, medium_rect, hard_rect = self.draw_menu()
                        if easy_rect.collidepoint(mouse_pos):
                            self.difficulty = "easy"
                            self.create_new_game()
                        elif medium_rect.collidepoint(mouse_pos):
                            self.difficulty = "medium"
                            self.create_new_game()
                        elif hard_rect.collidepoint(mouse_pos):
                            self.difficulty = "hard"
                            self.create_new_game()
                self.draw_menu()
                pygame.display.flip()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        # Если клик в области переключателя (верхняя панель)
                        toggle_rect = pygame.Rect(self.toggle_x, self.toggle_y, self.toggle_width, self.toggle_height)
                        if toggle_rect.collidepoint(pos):
                            self.pencil_mode = not self.pencil_mode
                        else:
                            if pos[1] >= self.toolbar_height and pos[1] <= self.window_size + self.toolbar_height:
                                col = pos[0] // self.cell_size
                                row = (pos[1] - self.toolbar_height) // self.cell_size
                                self.selected = (row, col)
                    if event.type == pygame.KEYDOWN and self.selected is not None:
                        if event.unicode.isdigit() and event.unicode != '0':
                            num = int(event.unicode)
                            row, col = self.selected
                            if self.pencil_mode:
                                if num in self.pencil_marks[row][col]:
                                    self.pencil_marks[row][col].remove(num)
                                else:
                                    self.pencil_marks[row][col].add(num)
                            else:
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
