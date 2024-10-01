import pygame

from Bullet import Bullet
from Invander import Invander
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

backgr = pygame.image.load("back2.png")
backgr = pygame.transform.scale(backgr, (window_width, window_height))

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
    if (handle_alien_hit(bullet_x, bullet_y)):
        bullet_active = False
        bullet.position = (0, 0)

    # if (handle_saucer_hit(bullet_x, bullet_y)):
    #     bullet_active = False
    #     bullet.position = (0, 0)

    if (bullet_y < 0):
        bullet_active = False

    return bullet_active

# создание пришельцев
def create_aliens():
    global alien_groups, level
    alien_groups = []
    for i in range(0, 5):
        alien_group = pygame.sprite.Group()
        for j in range(0, 11):
            alien = Invander(alien_names[i], alien_names[i] + 'c', 30 + (j * 60), 100 + i*60, alien_group, score_dict[alien_names[i]], level)
            alien_group.add(alien)
        alien_groups.append(alien_group)

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
    create_aliens()

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


def check_for_removal(alien):
    if alien.death_time > 0 and alien.death_time + 250 < pygame.time.get_ticks():
        alien.parent.remove(alien)
        if (len(alien.parent) == 0):
            alien_groups.remove(alien.parent)

def handle_alien_hit(bullet_x, bullet_y):
    global gems_collected, player_score, bullet, alien_groups
    for alien_group in alien_groups:
        for alien in alien_group:
            (x, y) = alien.position
            if bullet_x > x and bullet_x < x + alien.get_width() and  \
                 bullet_y > y and bullet_y < y + alien.get_height():
                alien.kill()
                alien_dying.play()
                player_score += alien.points
                return True
    return False

def draw_aliens(window, alien_groups):
    for alien_group in alien_groups:
        for alien in alien_group.sprites():
            alien.draw(window)
            check_for_removal(alien)

# Движение пришельцев

def find_leftmost_alien():
    minimum_x = window_width
    leftmost_alien = None
    for alien_group in alien_groups:
        alien = alien_group.sprites()[0]
        if (alien.position[0] < minimum_x):
            minimum_x = alien.position[0]
            leftmost_alien = alien

    return leftmost_alien


def find_rightmost_alien():
    maximum_x = 0
    rightmost_alien = None
    for alien_group in alien_groups:
        alien = alien_group.sprites()[-1]
        if (alien.position[0] > maximum_x):
            maximum_x = alien.position[0]
            rightmost_alien = alien

    return rightmost_alien


def find_bottommost_alien():
    maximum_y = 999
    bottommost_alien = None
    for alien_group in alien_groups:
        alien = alien_group.sprites()[-1]
        if (alien.position[1] < maximum_y):
            maximum_y = alien.position[0]
            bottommost_alien = alien
    return bottommost_alien


def move_aliens(leftmost, rightmost, bottommost, move_right, move_down):
    global game_time

    last_alien = rightmost
    first_alien = leftmost

    if (last_alien is None) or (first_alien is None):
        return (move_right, move_down)

    (last_alien_x, last_alien_y) = last_alien.position
    (first_alien_x, first_alien_y) = first_alien.position

    # move right and possibly down
    if move_right:
        if last_alien_x + last_alien.speed >= window_width - (last_alien.rect.width + 5):
            move_right = False
            if last_alien_y + last_alien.speed < window_height - last_alien.rect.height:
                if (bottommost.position[1] < window_height - 50):
                    move_down = True
        return move_right, move_down

    # move left and possibly down
    if not move_right:
        if first_alien_x - first_alien.speed <= 0:
            move_right = True
            if first_alien_y + first_alien.speed < window_height - first_alien.rect.height:
                if (bottommost.position[1] < window_height - 50):
                    move_down = True

    return move_right, move_down


def aliens_exist():
    for alien_group in alien_groups:
        if len(alien_group) > 0:
            return True
    return False

def handle_alien_movement():
    global game_time, move_aliens_down, alien_groups, move_aliens_right
    alien_rightmost = find_rightmost_alien()
    alien_leftmost = find_leftmost_alien()
    alien_bottommost = find_bottommost_alien()
    (move_aliens_right, move_aliens_down) = move_aliens(alien_leftmost, alien_rightmost,
                                                         alien_bottommost, move_aliens_right, move_aliens_down)

    # do animation
    for alien_group in alien_groups:
        for next_alien in alien_group:
            next_alien.switch_image(int(game_time/blink_speed) % 2 )
            next_alien.update()

    if game_time % 400 == 0 and aliens_exist():
        if game_time % 800 == 0:
            alien_movement.play()
        else:
            alien_movement2.play()

    for alien_group in alien_groups:
        for alien in alien_group:
            (x,y) = alien.position
            if move_aliens_right:
                alien.move_right()
            else:
                alien.move_left()
            if move_aliens_down:
                alien.move_down()
            alien.update()

    move_aliens_down = False

while running:
    (player_x, player_y) = player.position
    # window.fill(BLACK)
    window.blit(backgr, (0,0))

    running = process_events()

    # переместить игрока
    handle_player_movement(window_width, player_left, player_right, player, player_x)

    handle_alien_movement()


    # движение снаряда
    if bullet_active:
        bullet_active = handle_bullet(bullet, bullet_active)

    # рисуем пришельца и проверяем, убили ли его
    draw_aliens(window, alien_groups)

    # обновить дисплей
    pygame.display.flip()
