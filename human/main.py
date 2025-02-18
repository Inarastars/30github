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

# Список слов (все слова из разных тем)
WORDS = [
    "КОМНАТА", "ДОМ", "ЛЕС", "РЕКА", "ГОРА", "ПОЛЕ", "ОЗЕРО", "СОЛНЦЕ",
    "ЛУНА", "ЗВЕЗДА", "МОРЕ", "ПЛЯЖ", "ПТИЦА", "КОТ", "СОБАКА", "МАШИНА",
    "ВЕЛОСИПЕД", "ОКНО", "СТОЛ", "КНИГА", "ЦВЕТОК", "ГАРДЕН", "РЫБА", "БЕРЕГ"
]


# Функция рисования виселицы (пошагово)
def draw_hangman(wrong):
    # Основание и стойка
    pygame.draw.line(screen, BLACK, (150, 500), (350, 500), 5)
    pygame.draw.line(screen, BLACK, (250, 500), (250, 100), 5)
    pygame.draw.line(screen, BLACK, (250, 100), (450, 100), 5)
    pygame.draw.line(screen, BLACK, (450, 100), (450, 150), 5)
    if wrong > 0:
        # Голова
        pygame.draw.circle(screen, BLACK, (450, 180), 30, 5)
    if wrong > 1:
        # Туловище
        pygame.draw.line(screen, BLACK, (450, 210), (450, 320), 5)
    if wrong > 2:
        # Левая рука
        pygame.draw.line(screen, BLACK, (450, 240), (400, 280), 5)
    if wrong > 3:
        # Правая рука
        pygame.draw.line(screen, BLACK, (450, 240), (500, 280), 5)
    if wrong > 4:
        # Левая нога
        pygame.draw.line(screen, BLACK, (450, 320), (400, 380), 5)
    if wrong > 5:
        # Правая нога
        pygame.draw.line(screen, BLACK, (450, 320), (500, 380), 5)


# Функция для формирования строки с отгаданными буквами
def get_display_word(word, guessed):
    display = ""
    for letter in word:
        if letter in guessed:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()


def main():
    clock = pygame.time.Clock()

    secret_word = random.choice(WORDS)
    guessed_letters = set()
    wrong = 0
    max_wrong = 6

    input_active = True
    user_text = ""

    # Поле ввода для буквы
    input_rect = pygame.Rect(100, 450, 140, 50)

    running = True
    while running:
        screen.fill(WHITE)
        # Рисуем виселицу и добавляем части тела по количеству ошибок
        draw_hangman(wrong)

        # Отображаем текущее состояние слова
        display_word = get_display_word(secret_word, guessed_letters)
        text_surface = FONT_LARGE.render(display_word, True, BLACK)
        screen.blit(text_surface, (100, 350))

        # Информация об ошибках
        error_text = FONT_SMALL.render(f"Ошибки: {wrong} / {max_wrong}", True, RED)
        screen.blit(error_text, (100, 520))

        # Инструкция ввода
        instruction = FONT_SMALL.render("Введите букву и нажмите ENTER:", True, BLACK)
        screen.blit(instruction, (100, 420))

        # Отрисовка поля ввода
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        input_surface = FONT_MEDIUM.render(user_text, True, BLACK)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if user_text:
                        # Берём только первую букву, переводим в верхний регистр
                        guess = user_text.upper()[0]
                        if guess not in guessed_letters:
                            guessed_letters.add(guess)
                            if guess not in secret_word:
                                wrong += 1
                        user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text) < 1 and event.unicode.isalpha():
                        user_text += event.unicode

        # Проверка победы или поражения
        if wrong >= max_wrong:
            # Проигрыш
            msg = FONT_LARGE.render(f"Вы проиграли! Слово: {secret_word}", True, RED)
            screen.blit(msg, (50, 50))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
        elif all(letter in guessed_letters for letter in secret_word):
            # Победа
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
