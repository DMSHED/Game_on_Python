import pygame

pygame.init()

# Создаем экран
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))


def run_game():
    # Делаем название программы
    pygame.display.set_caption("TEST")

    # Создаем иконку
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    while True:
        # Проверяем события выхода
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


run_game()