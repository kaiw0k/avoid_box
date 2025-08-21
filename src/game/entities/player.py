import pygame


class Player:
    def __init__(self, x, y, screen_width=960, green_speed_factor=1.0):
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
        self.base_speed = 5
        self.speed = self.base_speed
        self.green_speed_factor = green_speed_factor  # 绿色方块速度因子
        self.color = (255, 0, 0)  # 红色
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_speed = -15
        self.is_jumping = False
        self.ground_y = 600 - self.height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # 添加二段跳相关属性
        self.jumps_remaining = 2  # 最大跳跃次数
        self.space_pressed = False  # 添加空格键状态追踪
        self.screen_width = screen_width
        self.drop_through = False  # 是否正在落下台阶
        self.current_platform = None  # 当前站立的台阶
        self.dropping_platform = None  # 正在落下的台阶

    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        # 检测向下+跳跃组合，触发落下台阶
        down_pressed = keys[pygame.K_DOWN] or keys[pygame.K_s]
        if keys[pygame.K_SPACE]:
            if not self.space_pressed:
                if down_pressed and self.current_platform:
                    # 如果按住向下键且在台阶上，则落下
                    self.drop_through = True
                    self.dropping_platform = self.current_platform  # 记录当前正在落下的台阶
                elif not self.is_jumping or self.jumps_remaining > 0:
                    # 否则正常跳跃
                    self.velocity_y = self.jump_speed
                    self.is_jumping = True
                    self.jumps_remaining -= 1
            self.space_pressed = True
        else:
            self.space_pressed = False

        # 边界限制
        self.x = max(0, min(self.x, self.screen_width - self.width))
        self.rect.x = self.x

    def update(self, platforms):
        # 应用重力
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # 更新矩形位置
        self.rect.x = self.x
        self.rect.y = self.y

        # 检查与平台的碰撞
        on_ground = False
        self.current_platform = None
        for platform in platforms:
            if platform.check_collision(self.rect):
                # 如果正在落下台阶且是当前正在落下的台阶
                if self.drop_through and platform == self.dropping_platform:
                    if self.rect.top > platform.rect.bottom:
                        # 完全离开当前台阶后重置状态
                        self.drop_through = False
                        self.dropping_platform = None
                    continue
                # 正常从上方碰撞台阶
                if self.velocity_y > 0 and self.rect.bottom > platform.rect.top:
                    # 如果不是正在落下的台阶，则停在上面
                    if not self.drop_through or platform != self.dropping_platform:
                        self.y = platform.rect.top - self.height
                        self.velocity_y = 0
                        on_ground = True
                        self.current_platform = platform
                        # 停在新台阶上时重置落下状态
                        self.drop_through = False
                        self.dropping_platform = None
                    break

        # 检查是否落地
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.velocity_y = 0
            on_ground = True
            self.drop_through = False
            self.dropping_platform = None

        # 如果落地，重置跳跃状态
        if on_ground:
            self.is_jumping = False
            self.jumps_remaining = 2

        # 限制方块在屏幕范围内
        self.x = max(0, min(self.x, self.screen_width - self.width))
        self.y = max(0, min(self.y, self.ground_y))
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def set_screen_width(self, screen_width):
        self.screen_width = screen_width

    def update_green_speed_factor(self, green_speed_factor):
        self.green_speed_factor = green_speed_factor
        self.speed = self.base_speed * (1 + 0.12 * ((green_speed_factor - 1) / 0.1))
