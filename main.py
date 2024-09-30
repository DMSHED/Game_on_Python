import pygame

from Bullet import Bullet
from Player import Player

pygame.init()

# Создаем экран
window_width = 800
window_height = 660

# параметры окна
WINDOW_SIZE = (window_width, window_height)
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

# Количество баллов за убийство
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

# Настройки спрайтов
player = Player('man', 30, 600)
bullet = Bullet(0, 0, 3, 15, .1)

# фиксируем нажатие клавиш
def process_events():
    #
    global player_left, player_right, bullet_active, level
    (player_x, player_y) = player.position
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # проверяем двигается ли игрок
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                if bullet_active == False and not player.dead:
                    bullet_active = True
                    bullet.position = (player_x + 30, player_y - 20)
                    bullet_fire_sound.play()
            elif event.key == pygame.K_LEFT and player_x > 0:
                player_left = True
                player_right = False
            elif event.key == pygame.K_RIGHT and player_x < window_width:
                player_right = True
                player_left = False
            elif event.key == pygame.K_y and game_over == True:
                initialize_game_state()
            elif event.key == pygame.K_n and game_over == True:
                running = False
        elif event.type == pygame.KEYUP:
            player_left = False
            player_right = False
    return running

def handle_bullet(bullet, bullet_active):
    (bullet_x, bullet_y) = bullet.position
    bullet_y = bullet_y - bullet.speed
    bullet.position = (bullet_x, bullet_y)
    bullet.update()
    bullet.draw(window)


    if (bullet_y < 0):
        bullet_active = False

    return bullet_active


def initialize_game_state():
    global player_score, start_time, game_over, \
        player_left, player_right, bullet_active, \
        player, alien_groups, score, player_lives, \
        move_aliens_right, move_aliens_down, \
        first_speed_up, second_speed_up, third_speed_up, \
        level, bomb_frequency, blink_speed

    print("Initializing game state")
    start_time = pygame.time.get_ticks()
    player_limit = 3
    move_aliens_right = True
    move_aliens_down = False
    level = 1
    game_over = False
    first_speed_up = False
    second_speed_up = False
    third_speed_up = False
    bomb_frequency = 5
    blink_speed = 400
    player_score = 0
    player_lives = 3
    game_over = False
    player_left = False
    player_right = False
    bullet_active = False
    player.dead = False
    player.update()


# инициализация игровых параметров
initialize_game_state()
# Основной игровой цикл
running = True
start_time = pygame.time.get_ticks()
first_speed_up = False
second_speed_up = False
third_speed_up = False
blink_speed = 400
saucer_blink_speed = 150

# принимает параметры, необходимые для перемещения спрайта игрока
# проверяем границы и если игрок выйдет за
# границы экрана, мы не разрешаем движение
# если игрок помечен как мертвый, нам не нужно его перемещать
def handle_player_movement(window_width, player_left, player_right, player, player_x):
    if (player.dead):
        pass
    elif player_left:
        if (player_x - player.speed) > 0:
            player.move_left()
    elif player_right:
        if (player_x + player.speed) < window_width - player.get_width():
            player.move_right()

    player.update()
    player.draw(window)

while running:
    (player_x, player_y) = player.position
    window.fill(BLACK)

    running = process_events()

    # переместить игрока
    handle_player_movement(window_width, player_left, player_right, player, player_x)

    # move the bullet
    if bullet_active:
        bullet_active = handle_bullet(bullet, bullet_active)

    # обновить дисплей
    pygame.display.flip()
