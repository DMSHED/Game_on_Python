import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_width, bullet_height, speed):
        super().__init__()
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)
        small_font = pygame.font.Font(None, 16)

        self.position = (x, y)
        self.speed = speed

        # создаем поверхность для спрайта
        self.image = pygame.Surface([bullet_width, bullet_height])
        self.image.fill(GREEN)
        # рисуем прямоугольник на поверхности спрайта
        self.rect = self.image.get_rect().move(x, y)

    # перемещаем спрайт в соответствии с положением пути
    def update(self):
        (x, y) = self.position
        self.rect = self.image.get_rect().move(x, y)

    # Рисуем спрайт на экране
    def draw(self, surface):
        surface.blit(self.image, self.rect)
