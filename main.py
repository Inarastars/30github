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
        self.selected = None
        self.lives = 3
        self.level = 1
        self.create_new_level()

    def create_new_level(self):
        empty_cells = self.increase_difficulty()
        self.board = self.generate_sudoku(empty_cells)
        self.original_board = deepcopy(self.board)
        self.solution = deepcopy(self.board)
        self.solve(self.solution)
        self.lives = 3

    def increase_difficulty(self):
        difficulties = {
            1: 1,  # Легкий уровень
            2: 5,  # Средний уровень
            3: 10,  # Сложный уровень
            4: 15,  # Очень сложный уровень
            5: 20,  # Экспертный уровень
        }
        return difficulties.get(self.level, 45)

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def generate_sudoku(self, empty_cells):
        board = np.zeros((9, 9), dtype=int)
        for _ in range(17):
            row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
            while not self.is_valid(board, row, col, num) or board[row][col] != 0:
                row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
            board[row][col] = num

        board_copy = deepcopy(board)
        self.solve(board_copy)

        indices = list(range(81))
        random.shuffle(indices)
        for i in indices[:empty_cells]:
            board[i // 9][i % 9] = 0

        return board

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
            self.create_new_level()

    def run(self):
        running = True
        while running:
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
                                    running = False
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