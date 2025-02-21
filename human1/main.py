import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Виселица")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Шрифты
FONT_LARGE = pygame.font.SysFont('arial', 48)
FONT_MEDIUM = pygame.font.SysFont('arial', 36)
FONT_SMALL = pygame.font.SysFont('arial', 24)

# Словари с категориями
CATEGORIES = {
    "Страны": ["КАЗАХСТАН", "РОССИЯ", "ФРАНЦИЯ", "ГЕРМАНИЯ", "ИТАЛИЯ"],
    "Столицы": ["АСТАНА", "МОСКВА", "ПАРИЖ", "БЕРЛИН", "РИМ"],
    "Жанры книг": ["ФАНТАСТИКА", "ДЕТЕКТИВ", "РОМАН", "ПОЭЗИЯ", "ДРАМА"],
    "Бытовые предметы": ["СТОЛ", "СТУЛ", "ЧАЙНИК", "ТЕЛЕВИЗОР", "ХОЛОДИЛЬНИК"],
    "Животные": ["ТИГР", "ЛЕВ", "СЛОН", "КРОЛИК", "ОСЁЛ"],
    "Цвета": ["КРАСНЫЙ", "СИНИЙ", "ЗЕЛЁНЫЙ", "ЖЁЛТЫЙ", "ЧЁРНЫЙ"],
    "Музыкальные инструменты": ["ГИТАРА", "ПИАНИНО", "СКРИПКА", "ФЛЕЙТА", "БАРАБАН"]
}


# Функция выбора категории
def choose_category():
    screen.fill(WHITE)
    text = FONT_LARGE.render("Выберите категорию", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 200, 50))

    buttons = []
    y_offset = 150
    for category in CATEGORIES.keys():
        rect = pygame.Rect(250, y_offset, 300, 50)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text_surface = FONT_MEDIUM.render(category, True, BLACK)
        screen.blit(text_surface, (260, y_offset + 10))
        buttons.append((rect, category))
        y_offset += 70

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, category in buttons:
                    if rect.collidepoint(event.pos):
                        return category


# Функция рисования виселицы
def draw_hangman(wrong):
    pygame.draw.line(screen, BLACK, (150, 500), (350, 500), 5)
    pygame.draw.line(screen, BLACK, (250, 500), (250, 100), 5)
    pygame.draw.line(screen, BLACK, (250, 100), (450, 100), 5)
    pygame.draw.line(screen, BLACK, (450, 100), (450, 150), 5)
    if wrong > 0:
        pygame.draw.circle(screen, BLACK, (450, 180), 30, 5)
    if wrong > 1:
        pygame.draw.line(screen, BLACK, (450, 210), (450, 320), 5)
    if wrong > 2:
        pygame.draw.line(screen, BLACK, (450, 240), (400, 280), 5)
    if wrong > 3:
        pygame.draw.line(screen, BLACK, (450, 240), (500, 280), 5)
    if wrong > 4:
        pygame.draw.line(screen, BLACK, (450, 320), (400, 380), 5)
    if wrong > 5:
        pygame.draw.line(screen, BLACK, (450, 320), (500, 380), 5)


# Функция отображения слова
def get_display_word(word, guessed):
    return ' '.join(letter if letter in guessed else '_' for letter in word)


def main():
    clock = pygame.time.Clock()
    category = choose_category()
    secret_word = random.choice(CATEGORIES[category])
    guessed_letters = set()
    wrong = 0
    max_wrong = 6
    user_text = ""
    input_rect = pygame.Rect(100, 450, 140, 50)

    running = True
    while running:
        screen.fill(WHITE)
        draw_hangman(wrong)

        display_word = get_display_word(secret_word, guessed_letters)
        text_surface = FONT_LARGE.render(display_word, True, BLACK)
        screen.blit(text_surface, (100, 350))

        category_text = FONT_SMALL.render(f"Категория: {category}", True, BLACK)
        screen.blit(category_text, (100, 50))

        error_text = FONT_SMALL.render(f"Ошибки: {wrong} / {max_wrong}", True, RED)
        screen.blit(error_text, (100, 520))

        instruction = FONT_SMALL.render("Введите букву и нажмите ENTER:", True, BLACK)
        screen.blit(instruction, (100, 420))

        pygame.draw.rect(screen, BLACK, input_rect, 2)
        input_surface = FONT_MEDIUM.render(user_text, True, BLACK)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_text:
                    guess = user_text.upper()[0]
                    if guess not in guessed_letters:
                        guessed_letters.add(guess)
                        if guess not in secret_word:
                            wrong += 1
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < 1 and event.unicode.isalpha():
                    user_text += event.unicode

        if wrong >= max_wrong:
            msg = FONT_LARGE.render(f"Вы проиграли! Слово: {secret_word}", True, RED)
            screen.blit(msg, (50, 50))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
        elif all(letter in guessed_letters for letter in secret_word):
            msg = FONT_LARGE.render("Поздравляем! Вы выиграли!", True, BLACK)
            screen.blit(msg, (50, 50))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
