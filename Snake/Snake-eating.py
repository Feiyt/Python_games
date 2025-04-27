import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# --- Unified Style Constants ---
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 6.48

# Colors
BACKGROUND_COLOR = (200, 200, 200) # Light Gray
PRIMARY_COLOR = (50, 50, 150)      # Medium Blue
SECONDARY_COLOR = (100, 100, 200) # Lighter Blue
ACCENT_COLOR = (255, 215, 0)       # Gold
TEXT_COLOR = (0, 0, 0)             # Black
BUTTON_TEXT_COLOR = (255, 255, 255) # White
# Game Specific Colors (derived from unified palette)
SNAKE_HEAD_COLOR = PRIMARY_COLOR
SNAKE_BODY_COLOR = SECONDARY_COLOR
FOOD_COLOR = ACCENT_COLOR
SCORE_COLOR = TEXT_COLOR
GAMEOVER_TEXT_COLOR = PRIMARY_COLOR

# Fonts
FONT_FAMILY = "SimHei"
FONT_SMALL = pygame.font.SysFont(FONT_FAMILY, 24)
FONT_MEDIUM = pygame.font.SysFont(FONT_FAMILY, 36)
FONT_LARGE = pygame.font.SysFont(FONT_FAMILY, 48)
# --- End Unified Style Constants ---

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = (1, 0)
        self.new_direction = self.direction
        self.grow = False
    
    def update(self):
        if (self.new_direction[0] + self.direction[0] != 0 or
            self.new_direction[1] + self.direction[1] != 0):
            self.direction = self.new_direction
        
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1]
        )
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def check_collision(self):
        return len(self.body) != len(set(self.body))

# --- Reintroduce Food Class ---
class Food:
    def __init__(self):
        self.position = (0, 0) # Initialize position
        self.randomize_position() # Set initial random position

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
# --- End Food Class ---

# --- Standardized Button Function ---
def draw_button(surface, text, font, x, y, width, height, color, hover_color, text_color):
    # Calculate text size for padding
    text_surf_temp = font.render(text, True, text_color)
    text_width, text_height = text_surf_temp.get_size()
    
    # Add padding to the provided width, or use text width + padding if width is too small
    padded_width = max(width, text_width + 40) # Ensure at least 20px padding each side
    
    button_rect = pygame.Rect(x, y, padded_width, height)
    # Adjust x position based on new width to keep it centered if width was specified
    # If original 'width' was meant to be the final width, this maintains centering.
    # If x,y was top-left, we might need to adjust x based on (padded_width - width)/2
    # Let's assume the original x was for centering, so we adjust it:
    button_rect.centerx = x + width // 2 # Recenter based on original x and width center point
    button_rect.y = y # Keep original y

    mouse_pos = pygame.mouse.get_pos()
    
    current_color = color
    if button_rect.collidepoint(mouse_pos):
        current_color = hover_color
        
    pygame.draw.rect(surface, current_color, button_rect, border_radius=5)
    
    # Render text again (though we have size, rendering again is safer)
    text_surface = font.render(text, True, text_color)
    # Center text in the potentially wider button_rect
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    
    return button_rect # Return the actual drawn rect

def draw_centered_text(surface, text, font, color, y_offset=0):
    text_surface = font.render(text, True, color) # Use the rendered surface
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    surface.blit(text_surface, text_rect)
# --- End Standardized Button Function ---

def game_loop():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("贪吃蛇")
    
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()
    score = 0
    body_radius = GRID_SIZE // 2 - 2 # Slightly smaller for better spacing
    head_radius = GRID_SIZE // 2 # Head slightly larger

    # 主游戏循环
    running = True
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in {
                    pygame.K_UP, pygame.K_w, 
                    pygame.K_DOWN, pygame.K_s,
                    pygame.K_LEFT, pygame.K_a,
                    pygame.K_RIGHT, pygame.K_d
                }:
                    snake.new_direction = {
                        pygame.K_UP: (0, -1),    pygame.K_w: (0, -1),
                        pygame.K_DOWN: (0, 1),   pygame.K_s: (0, 1),
                        pygame.K_LEFT: (-1, 0),  pygame.K_a: (-1, 0),
                        pygame.K_RIGHT: (1, 0),  pygame.K_d: (1, 0)
                    }[event.key]

        # 游戏更新
        snake.update()
        
        # 碰撞检测
        head_x, head_y = snake.body[0]
        if (head_x < 0 or head_x >= GRID_WIDTH or
            head_y < 0 or head_y >= GRID_HEIGHT):
            running = False
        
        if snake.body[0] == food.position:
            snake.grow = True
            score += 1
            food.randomize_position()
            while food.position in snake.body:
                food.randomize_position()
        
        if snake.check_collision():
            running = False

        # 画面绘制
        screen.fill(BACKGROUND_COLOR) # Use new background
        
        # 绘制食物
        food_x = food.position[0] * GRID_SIZE + GRID_SIZE // 2
        food_y = food.position[1] * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(screen, FOOD_COLOR, (food_x, food_y), body_radius) # Use new food color
        
        # 绘制蛇
        for idx, (x, y) in enumerate(snake.body):
            center_x = x * GRID_SIZE + GRID_SIZE // 2
            center_y = y * GRID_SIZE + GRID_SIZE // 2
            radius = head_radius if idx == 0 else body_radius
            color = SNAKE_HEAD_COLOR if idx == 0 else SNAKE_BODY_COLOR # Use new snake colors
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
        
        # 显示分数
        score_text = FONT_MEDIUM.render(f"得分：{score}", True, SCORE_COLOR)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # 游戏结束界面
    button_width = 200
    button_height = 50
    restart_button_y = HEIGHT // 2 + 40
    exit_button_y = restart_button_y + button_height + 20

    while True:
        screen.fill(BACKGROUND_COLOR) # Use new background

        # 游戏结束文字 - Use standard fonts and colors
        draw_centered_text(screen, "游戏结束！", FONT_LARGE, GAMEOVER_TEXT_COLOR, -100)
        draw_centered_text(screen, f"最终得分：{score}", FONT_MEDIUM, TEXT_COLOR, -30)

        # 选项菜单 - Use draw_button
        restart_rect = draw_button(
            screen, "重新开始 (R)", FONT_MEDIUM,
            WIDTH // 2 - button_width // 2, restart_button_y, button_width, button_height,
            PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR
        )
        exit_rect = draw_button(
            screen, "退出游戏 (Q)", FONT_MEDIUM,
            WIDTH // 2 - button_width // 2, exit_button_y, button_width, button_height,
            PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR
        )

        pygame.display.flip()

        # 处理菜单事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 按下 R 键重新开始
                    return True
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:  # 按下 Q 键或 ESC 键退出游戏
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):  # 点击"重新开始"
                        return True
                    elif exit_rect.collidepoint(mouse_pos):  # 点击"退出游戏"
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    while True:
        restart = game_loop()
        if not restart:
            break
    pygame.quit()
    sys.exit()