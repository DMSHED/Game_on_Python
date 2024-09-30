import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_width, bullet_height, speed, parent):
        super().__init__()
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)
        small_font = pygame.font.Font(None, 16)

        self.position = (x, y)
        self.speed = speed
        self.parent = parent

        # создаем поверхность для спрайта
        self.image = pygame.Surface([bullet_width, bullet_height])
        pygame.draw.lines(self.image, WHITE, True, [(0, 0), (5, 5), (0, 10), (10, 15)], 1)

        # рисуем прямоугольник на поверхности спрайта
        self.rect = self.image.get_rect().move(x, y)

    # обновить бомбу в соответствии с текущей позицией
    def update(self):
        (x, y) = self.position
        self.rect = self.image.get_rect().move(x, y)

    # рисуем спрайт на экране
    def draw(self, surface):
        surface.blit(self.image, self.rect)
