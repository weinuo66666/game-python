import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 定義一些常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 255)  # 白色
BLACK = (0, 0, 0)
PLATFORM_COLOR = BLACK
WHITE = (255, 255, 255)  # 白色

# 設定平台參數
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 20
JUMP_HEIGHT = 25  # 跳躍高度設為25
PLATFORM_GAP = JUMP_HEIGHT  # 距離為跳躍高度的1倍

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
INITIAL_SPEED = 0  # 初始速度
MAX_SPEED = 15  # 原為10，增加到1.5倍
ACCELERATION = 1  # 加速度
GRAVITY = 1  # 重力加速度
FAST_FALL_SPEED = 15  # 急速下墜的速度

# 創建遊戲窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("簡單的Pygame遊戲")

# 加載主角圖片，並調整尺寸
player_image = pygame.image.load("a-guy-sitting-at-the-edge-of-an-apartment-and-is-d.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

# 創建遊戲角色
player = pygame.Rect(375, SCREEN_HEIGHT - PLAYER_HEIGHT - 100, PLAYER_WIDTH, PLAYER_HEIGHT)
platforms = [pygame.Rect((SCREEN_WIDTH - PLATFORM_WIDTH) // 2, SCREEN_HEIGHT - 100, PLATFORM_WIDTH, PLATFORM_HEIGHT)]

# 控制跳躍
is_jumping = False
jump_count = JUMP_HEIGHT
player_y_speed = 0  # 垂直速度

# 控制移動速度
move_left = False
move_right = False
fast_falling = False  # 急速下墜狀態
speed = INITIAL_SPEED

# 遊戲運行標誌
is_game_active = True

# 初始平台移動速度
PLATFORM_SPEED = 2
SPEED_INCREMENT = 1  # 每十秒速度增加量

# 計分相關
score = 0
score_event = pygame.USEREVENT + 2
pygame.time.set_timer(score_event, 100)  # 每0.1秒加1分

# 顯示字體設置
font = pygame.font.Font(None, 36)

# 平台生成計時器
platform_timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(platform_timer_event, 500)  # 每0.5秒生成一個新平台

# 加速計時器
speed_increase_event = pygame.USEREVENT + 3
pygame.time.set_timer(speed_increase_event, 10000)  # 每10秒加速一次

# 生成新平台函數（保留原有版本）
def generate_new_platform():
    if len(platforms) > 0:
        last_platform = platforms[-1]
        new_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        new_y = last_platform.y - PLATFORM_GAP * 10
        return pygame.Rect(new_x, new_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    else:
        # 如果沒有平台，則在螢幕底部生成一個平台
        return pygame.Rect((SCREEN_WIDTH - PLATFORM_WIDTH) // 2, SCREEN_HEIGHT - 100, PLATFORM_WIDTH, PLATFORM_HEIGHT)

# 遊戲主循環
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_s:
                fast_falling = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
                speed = INITIAL_SPEED  # 重置速度
            if event.key == pygame.K_RIGHT:
                move_right = False
                speed = INITIAL_SPEED  # 重置速度
            if event.key == pygame.K_s:
                fast_falling = False
        elif event.type == platform_timer_event:
            if is_game_active:
                platforms.append(generate_new_platform())  # 生成新平台
        elif event.type == score_event:
            if is_game_active:
                score += 1  # 每0.1秒加1分
        elif event.type == speed_increase_event:
            PLATFORM_SPEED += SPEED_INCREMENT  # 每10秒加速一次
    
    if is_game_active:
        # 處理移動
        if move_left:
            if speed < MAX_SPEED:
                speed += ACCELERATION
            player.x = max(player.x - speed, 0)
        if move_right:
            if speed < MAX_SPEED:
                speed += ACCELERATION
            player.x = min(player.x + speed, SCREEN_WIDTH - PLAYER_WIDTH)

        if fast_falling:
            player_y_speed = FAST_FALL_SPEED
        else:
            player_y_speed += GRAVITY

        player.y += player_y_speed

        # 檢查是否站在平台上
        on_platform = False
        for platform in platforms:
            if (player.bottom >= platform.y and
                player.bottom <= platform.y + PLATFORM_HEIGHT and
                player.centerx >= platform.x and
                player.centerx <= platform.x + PLATFORM_WIDTH):
                player.bottom = platform.y
                player_y_speed = 0
                on_platform = True
                break

        keys = pygame.key.get_pressed()

        if not on_platform and player_y_speed >= 0:
            is_jumping = False

        # 處理跳躍
        if not is_jumping and on_platform:
            if keys[pygame.K_SPACE]:
                is_jumping = True
                player_y_speed = -JUMP_HEIGHT  # 跳躍時設置向上速度
        
        # 確保玩家緊貼平台
        if on_platform and not is_jumping and not fast_falling:
            player_y_speed = 0
            player.bottom = platform.y

        # 檢查是否掉出螢幕
        if player.top > SCREEN_HEIGHT:
            is_game_active = False  # 停止遊戲邏輯

        # 移動平台
        for platform in platforms:
            platform.y += PLATFORM_SPEED

        # 移除超出螢幕的舊平台
        platforms = [platform for platform in platforms if platform.y < SCREEN_HEIGHT]

    # 更新螢幕
    screen.fill(BG_COLOR)

    # 繪製主角圖片
    screen.blit(player_image, (player.x, player.y))
    
    for platform in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, platform)

    # 顯示分數
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if not is_game_active:
        # 顯示Game Over信息
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
