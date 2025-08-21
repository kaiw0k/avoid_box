import pygame


class Platform:
    def __init__(self, x, y, width, height, color=(150, 75, 0)):  # 默认棕色
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)
