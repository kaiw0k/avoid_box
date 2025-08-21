import pygame
import random


class GreenBlock:
    def __init__(self, screen_width, screen_height, x=None, y=None, direction=None, score=0, base_speed=8,
                 score_step=10):
        self.size = int(screen_width * 0.05)
        if y is not None:
            self.y = y
        else:
            self.y = random.randint(int(screen_height * 0.1), int(screen_height * 0.8))
        if direction is not None:
            self.direction = direction
        else:
            self.direction = random.choice(['left', 'right'])
        if x is not None:
            self.x = x
        else:
            if self.direction == 'left':
                self.x = screen_width
            else:
                self.x = -self.size
        # 动态速度计算
        speed_factor = 1 + 0.1 * (score // score_step)
        if direction is not None and x is not None:
            if direction == 'left':
                self.speed = -base_speed * speed_factor
            else:
                self.speed = base_speed * speed_factor
        else:
            if self.direction == 'left':
                self.speed = -base_speed * speed_factor
            else:
                self.speed = base_speed * speed_factor
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.color = (0, 200, 0)
        self.scored = False  # 是否已计分

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_out_of_screen(self, screen_width):
        return self.x < -self.size or self.x > screen_width

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)
