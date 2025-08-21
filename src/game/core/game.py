import pygame
import sys
from ..entities.player import Player
from ..entities.platform import Platform
from ..entities.green_block import GreenBlock  # 新增导入
import random


class Game:
    def __init__(self):
        pygame.init()
        # 默认窗口分辨率放大50%
        self.default_width = int(960 * 1.5)
        self.default_height = int(540 * 1.5)
        self.screen_width = self.default_width
        self.screen_height = self.default_height
        self.fullscreen = False
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("方块跳跃 Demo")
        self.clock = pygame.time.Clock()
        self.score = 0  # 计分牌
        self.green_blocks = []  # 绿色方块列表
        self.spawn_timer = 0  # 绿色方块生成计时器
        self.font = pygame.font.SysFont(None, int(self.screen_height * 0.07))  # 分数字体
        self.init_elements()
        self.game_over = False  # 游戏结束标志
        self.game_over_time = None  # 记录游戏结束时间
        self.waiting_restart = False  # 是否等待重启
        self.countdown_start_time = None  # 倒计时开始时间
        self.countdown_seconds = 3  # 倒计时秒数
        self.waiting_start = True  # 是否等待游戏开始
        self.start_countdown_start_time = None  # 开始倒计时起始时间
        self.start_countdown_seconds = 3  # 开始倒计时秒数

    def init_elements(self):
        import random
        player_size = int(self.screen_width * 0.05)
        player_x = int(self.screen_width * 0.05)
        player_y = int(self.screen_height * 0.55)
        self.player = Player(player_x, player_y, self.screen_width, green_speed_factor=1.0)
        self.player.width = player_size
        self.player.height = player_size
        self.player.rect = pygame.Rect(player_x, player_y, player_size, player_size)
        self.player.ground_y = self.screen_height - player_size

        # 台阶参数
        plat_w = int(self.screen_width * 0.2)  # 台阶宽度为屏幕宽度的20%
        plat_h = int(self.screen_height * 0.07 * 0.4)  # 台阶高度
        jump_height = int((15 ** 2) / (2 * 0.8))  # 跳跃高度，约140像素

        # 计算安全的水平间距
        min_horizontal_gap = player_size * 2  # 最小水平间距为玩家宽度的2倍
        safe_platform_distance = plat_w + min_horizontal_gap  # 台阶之间的安全距离

        # 计算可用的水平空间
        usable_width = self.screen_width - 2 * int(self.screen_width * 0.05)  # 去除两侧边距
        platform_slots = []  # 可用的台阶位置槽

        # 将可用空间划分为若干槽位
        num_slots = 5  # 预设5个槽位
        slot_width = usable_width / num_slots
        for i in range(num_slots):
            slot_x = int(self.screen_width * 0.05) + i * slot_width
            platform_slots.append(slot_x)

        # 最下方台阶距离底部 jump_height ~ jump_height*1.2
        min_gap = int(jump_height * 0.8)  # 稍微降低最低高度，增加难度
        max_gap = int(jump_height * 1.2)
        base_y = self.screen_height - plat_h - random.randint(min_gap, max_gap)

        self.platforms = []
        used_slots = []
        plat_y = base_y

        for i in range(4):
            # 从未使用的槽位中随机选择一个
            available_slots = [x for x in platform_slots if x not in used_slots]
            if not available_slots:  # 如果所有槽位都用完了，重置使用记录
                used_slots = []
                available_slots = platform_slots

            # 在选定的槽位范围内随机偏移
            selected_slot = random.choice(available_slots)
            max_offset = (slot_width - plat_w) / 2
            offset = random.uniform(-max_offset, max_offset)
            plat_x = selected_slot + offset

            # 确保台阶不会超出屏幕边界
            plat_x = max(int(self.screen_width * 0.05),
                         min(int(self.screen_width * 0.95) - plat_w, plat_x))

            used_slots.append(selected_slot)
            self.platforms.append(Platform(int(plat_x), int(plat_y), plat_w, plat_h))

            # 计算下一个台阶的垂直位置
            if i < 3:
                # 根据当前平台位置调整下一个平台的垂直间距
                vertical_gap = random.randint(min_gap, max_gap)
                # 如果水平距离较远，适当减小垂直间距
                for prev_platform in self.platforms:
                    horizontal_dist = abs(plat_x - prev_platform.rect.x)
                    if horizontal_dist > safe_platform_distance * 1.5:
                        vertical_gap = int(vertical_gap * 0.85)  # 减少15%的垂直间距
                plat_y -= vertical_gap

        self.green_blocks = []
        self.spawn_timer = 0
        self.font = pygame.font.SysFont(None, int(self.screen_height * 0.07))
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()
                # 游戏初始等待状态，按空格进入倒计时
                if self.waiting_start and self.start_countdown_start_time is None:
                    if event.key == pygame.K_SPACE:
                        self.start_countdown_start_time = pygame.time.get_ticks()
                if self.game_over and not self.waiting_restart:
                    if event.key == pygame.K_SPACE:
                        self.waiting_restart = True
                        self.countdown_start_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        # 只有正式游戏状态才响应输入
        if not self.game_over and not self.waiting_restart and not self.waiting_start:
            self.player.handle_input(keys)
        return True

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            info = pygame.display.Info()
            max_w, max_h = info.current_w, info.current_h
            ratio = 16 / 9
            if max_w / max_h > ratio:
                new_h = max_h
                new_w = int(new_h * ratio)
            else:
                new_w = max_w
                new_h = int(new_w / ratio)
            self.screen_width = new_w
            self.screen_height = new_h
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        else:
            self.screen_width = self.default_width
            self.screen_height = self.default_height
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.init_elements()  # 切换分辨率后重设元素

    def update(self):
        # 只有正式游戏状态才更新
        if self.game_over or self.waiting_restart or self.waiting_start:
            return

        self.player.set_screen_width(self.screen_width)
        # 计算绿色方块速度因子和生成概率
        speed_base = 8
        score_step = 10
        green_speed_factor = 1 + 0.1 * (self.score // score_step)
        # 初始生成概率为0.5（50%），每10分增加10%
        spawn_chance = 0.5 + 0.1 * (self.score // score_step)
        # 从红色方块高度生成的概率，初始20%，每10分增加10%
        player_height_chance = 0.2 + 0.1 * (self.score // score_step)
        self.player.update_green_speed_factor(green_speed_factor)
        self.player.update(self.platforms)
        # 绿色方块生成逻辑
        self.spawn_timer += 1
        if self.spawn_timer > 40:  # 每隔约0.7秒检查是否生成
            if random.random() < spawn_chance:  # 使用动态生成概率
                if random.random() < player_height_chance:  # 使用动态的玩家高度生成概率
                    direction = random.choice(['left', 'right'])
                    size = int(self.screen_width * 0.05)
                    if direction == 'left':
                        x = self.screen_width
                        y = self.player.y
                    else:
                        x = -size
                        y = self.player.y
                    self.green_blocks.append(
                        GreenBlock(self.screen_width, self.screen_height, x=x, y=y, direction=direction,
                                   score=self.score, base_speed=speed_base, score_step=score_step))
                else:
                    self.green_blocks.append(
                        GreenBlock(self.screen_width, self.screen_height, score=self.score, base_speed=speed_base,
                                   score_step=score_step))
            self.spawn_timer = 0
        # 更新绿色方块
        for block in self.green_blocks:
            block.update()
        # 检查绿色方块与红色方块的碰撞和计分
        for block in self.green_blocks:
            if block.check_collision(self.player.rect):
                block.scored = True  # 碰撞不计分
                if not self.game_over:
                    self.game_over = True
                    self.game_over_time = pygame.time.get_ticks()
            elif not block.scored:
                # 判断是否完全经过红色方块
                if block.direction == 'left' and block.x + block.size < self.player.x:
                    self.score += 1
                    block.scored = True
                elif block.direction == 'right' and block.x > self.player.x + self.player.width:
                    self.score += 1
                    block.scored = True
        # 移除出界的绿色方块
        self.green_blocks = [b for b in self.green_blocks if not b.is_out_of_screen(self.screen_width)]

    def render(self):
        self.screen.fill((255, 255, 255))
        # 绘制所有台阶
        for platform in self.platforms:
            platform.draw(self.screen)
        for block in self.green_blocks:
            block.draw(self.screen)
        self.player.draw(self.screen)
        # 绘制分数
        try:
            font = pygame.font.SysFont("SimHei", int(self.screen_height * 0.07))
        except:
            font = pygame.font.SysFont(None, int(self.screen_height * 0.07))

        # 绘制分数
        score_surf = font.render(f"分数: {self.score}", True, (0, 0, 0))
        score_rect = score_surf.get_rect(topleft=(10, 10))
        self.screen.blit(score_surf, score_rect)

        # 绘制全屏提示
        fullscreen_surf = font.render("F键全屏", True, (100, 100, 100))  # 使用灰色
        fullscreen_rect = fullscreen_surf.get_rect(topleft=(score_rect.right + 20, 10))
        self.screen.blit(fullscreen_surf, fullscreen_rect)

        # 游戏初始等待提示
        if self.waiting_start and self.start_countdown_start_time is None:
            try:
                font2 = pygame.font.SysFont("SimHei", int(self.screen_height * 0.12))
            except:
                font2 = pygame.font.SysFont(None, int(self.screen_height * 0.12))
            text = font2.render("按空格键开始", True, (0, 0, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, int(self.screen_height * 0.25)))
            self.screen.blit(text, text_rect)
        # 游戏初始倒计时
        if self.waiting_start and self.start_countdown_start_time is not None:
            now = pygame.time.get_ticks()
            left = self.start_countdown_seconds - int((now - self.start_countdown_start_time) / 1000)
            if left < 0:
                left = 0
            try:
                font2 = pygame.font.SysFont("SimHei", int(self.screen_height * 0.12))
            except:
                font2 = pygame.font.SysFont(None, int(self.screen_height * 0.12))
            text = font2.render(f"{left}", True, (0, 128, 0))
            text_rect = text.get_rect(center=(self.screen_width // 2, int(self.screen_height * 0.25)))
            self.screen.blit(text, text_rect)
        # 游戏结束提示
        if self.game_over and not self.waiting_restart:
            try:
                font2 = pygame.font.SysFont("SimHei", int(self.screen_height * 0.12))
            except:
                font2 = pygame.font.SysFont(None, int(self.screen_height * 0.12))
            text = font2.render("游戏结束", True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.screen_width // 2, int(self.screen_height * 0.25)))
            self.screen.blit(text, text_rect)
            tip = font.render("按空格键重新开始", True, (0, 0, 0))
            tip_rect = tip.get_rect(center=(self.screen_width // 2, int(self.screen_height * 0.35)))
            self.screen.blit(tip, tip_rect)
        # 倒计时提示
        if self.waiting_restart:
            now = pygame.time.get_ticks()
            left = self.countdown_seconds - int((now - self.countdown_start_time) / 1000)
            if left < 0:
                left = 0
            try:
                font2 = pygame.font.SysFont("SimHei", int(self.screen_height * 0.12))
            except:
                font2 = pygame.font.SysFont(None, int(self.screen_height * 0.12))
            text = font2.render(f"{left}", True, (0, 128, 0))
            text_rect = text.get_rect(center=(self.screen_width // 2, int(self.screen_height * 0.25)))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            # 游戏初始倒计时结束后正式开始
            if self.waiting_start and self.start_countdown_start_time is not None:
                now = pygame.time.get_ticks()
                if now - self.start_countdown_start_time >= self.start_countdown_seconds * 1000:
                    self.waiting_start = False
                    self.start_countdown_start_time = None
            # 倒计时结束后重置游戏
            if self.waiting_restart:
                now = pygame.time.get_ticks()
                if now - self.countdown_start_time >= self.countdown_seconds * 1000:
                    self.game_over = False
                    self.waiting_restart = False
                    self.countdown_start_time = None
                    self.init_elements()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()
