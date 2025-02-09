import pygame
import random

pygame.init()

# Размеры поля
WIDTH, HEIGHT = 360, 600  # Увеличил ширину
BLOCK_SIZE = 30
COLUMNS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Цвета
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)
PINK = (255, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0),
          (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Фигуры тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]  # Z
]


class Tetromino:
    def __init__(self, x, y, shape):
        self.x, self.y = x, y
        self.shape = shape
        self.color = random.choice(COLORS)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


# Проверка столкновений
def collision(board, shape, x, y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell and (x + col_idx < 0 or x + col_idx >= COLUMNS or y + row_idx >= ROWS or board[y + row_idx][
                x + col_idx]):
                return True
    return False


# Очистка заполненных линий
def clear_lines(board, score, combo):
    full_rows = [i for i in range(ROWS) if all(board[i])]
    for row in full_rows:
        del board[row]
        board.insert(0, [0] * COLUMNS)
    if full_rows:
        combo += 1
        score += 100 * combo
    else:
        combo = 0
    return len(full_rows), score, combo


def main():
    score = 0
    combo = 0
    try:
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())
    except FileNotFoundError:
        highscore = 0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = [[0] * COLUMNS for _ in range(ROWS)]
    current_piece = Tetromino(COLUMNS // 2 - 1, 0, random.choice(SHAPES))
    running, game_over = True, False
    fall_time, fast_fall = 0, False

    while running:
        screen.fill(WHITE)
        fall_time += clock.get_rawtime()
        clock.tick(60)

        if fall_time > (10 if fast_fall else 50):
            if not collision(board, current_piece.shape, current_piece.x, current_piece.y + 1):
                current_piece.y += 1
            else:
                for row_idx, row in enumerate(current_piece.shape):
                    for col_idx, cell in enumerate(row):
                        if cell:
                            board[current_piece.y + row_idx][current_piece.x + col_idx] = current_piece.color
                score += 10
                cleared, score, combo = clear_lines(board, score, combo)
                current_piece = Tetromino(COLUMNS // 2 - 1, 0, random.choice(SHAPES))
                if collision(board, current_piece.shape, current_piece.x, current_piece.y):
                    game_over = True
                    running = False
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not collision(board, current_piece.shape, current_piece.x - 1,
                                                                current_piece.y):
                    current_piece.x -= 1
                if event.key == pygame.K_RIGHT and not collision(board, current_piece.shape, current_piece.x + 1,
                                                                 current_piece.y):
                    current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    fast_fall = True
                if event.key == pygame.K_UP:
                    rotated_shape = [list(row) for row in zip(*current_piece.shape[::-1])]
                    if not collision(board, rotated_shape, current_piece.x, current_piece.y):
                        current_piece.shape = rotated_shape
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    fast_fall = False

        for y in range(ROWS):
            for x in range(COLUMNS):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)
                if board[y][x]:
                    pygame.draw.rect(screen, board[y][x], rect)

        for row_idx, row in enumerate(current_piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((current_piece.x + col_idx) * BLOCK_SIZE,
                                       (current_piece.y + row_idx) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, current_piece.color, rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        highscore_text = font.render(f'High Score: {highscore}', True, (0, 0, 0))
        screen.blit(highscore_text, (10, 40))
        pygame.display.flip()

    if score > highscore:
        highscore = score
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))

    print(f"Game Over! Final Score: {score} | High Score: {highscore}")
    pygame.quit()


if __name__ == "__main__":
    main()
