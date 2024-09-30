import pygame

pygame.init()

# Создаем экран
display_width = 800
display_height = 600

# параметры окна
WINDOW_SIZE = (display_width, display_height)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Space Invanders')

# константы цветов
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,150,0)
RED = (255,0,0)
BLUE = (0,0,255)
colors = [GREEN, RED, BLUE]

# шрифт
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 16)

piece_size = 20
alien_names = ['invader1', 'invader2', 'invader2', 'invader3', 'invader3' ]

game_time = 0
board_cleared = False

# Количество баллов за убийство босса
score_dict =  {
    'invader1': 30,
    'invader2': 20,
    'invader3': 10
}

# жизни игрока
player_lives = 3

# Настройка музыки
alien_dying = pygame.mixer.Sound('sounds/3.wav')
bullet_fire_sound = pygame.mixer.Sound('sounds/1.wav')
player_hit_sound = pygame.mixer.Sound('sounds/2.wav')
alien_movement = pygame.mixer.Sound('sounds/6.wav')
alien_movement2 = pygame.mixer.Sound('sounds/7.wav')
player_dying = pygame.mixer.Sound('sounds/5.wav')
saucer_sound = pygame.mixer.Sound('sounds/8.wav')
saucer_dying = pygame.mixer.Sound('sounds/3.wav')

# Создаем иконку
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

def run_game():


    while True:
        # Проверяем события выхода
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


run_game()