import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH = 500
HEIGHT = 500
GRID_SIZE = 25
GRID_WIDTH = 1
GRID_HEIGHT = 1
FPS = 60

# 颜色定义
BACKGROUND_COLOR = (200, 200, 200)
PRIMARY_COLOR = (50, 50, 150)
SECONDARY_COLOR = (100, 100, 200)
ACCENT_COLOR = (255, 215, 0)
TEXT_COLOR = (0, 0, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)

# 字体
FONT_FAMILY = "SimHei"
FONT_SMALL = pygame.font.SysFont(FONT_FAMILY, 20)
FONT_MEDIUM = pygame.font.SysFont(FONT_FAMILY, 30)
FONT_LARGE = pygame.font.SysFont(FONT_FAMILY, 48)

class Minesweeper:
    def __init__(self, difficulty='medium'):
        if difficulty == 'easy':
            self.rows = 20
            self.cols = 20
            self.mines = 40
        elif difficulty == 'medium':
            self.rows = 20
            self.cols = 20
            self.mines = 40
        else:  # hard
            self.rows = 20
            self.cols = 20
            self.mines = 40
            
        self.reset()
    
    def reset(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = False
        self.first_click = True
        self.place_mines()
    
    def place_mines(self):
        if not self.first_click:
            return
            
        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if self.board[y][x] != -1 and not (self.first_click and self.revealed[y][x]):
                self.board[y][x] = -1
                mines_placed += 1
                
                # 更新周围格子数字
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < self.rows and 0 <= nx < self.cols and self.board[ny][nx] != -1:
                            self.board[ny][nx] += 1
    
    def reveal(self, row, col):
        if self.game_over or self.flagged[row][col]:
            return
            
        if self.first_click:
            self.first_click = False
            self.place_mines()
            
        if self.board[row][col] == -1:
            self.game_over = True
            return
            
        if not self.revealed[row][col]:
            self.revealed[row][col] = True
            
            # 如果是空白格子，递归揭示周围
            if self.board[row][col] == 0:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = row + dy, col + dx
                        if 0 <= ny < self.rows and 0 <= nx < self.cols:
                            self.reveal(ny, nx)
            
            # 检查胜利条件
            if self.check_win():
                self.game_over = True
    
    def toggle_flag(self, row, col):
        if not self.revealed[row][col] and not self.game_over:
            self.flagged[row][col] = not self.flagged[row][col]
    
    def check_win(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True

def draw_button(surface, text, font, x, y, width, height, color, hover_color, text_color):
    button_rect = pygame.Rect(x, y, width, height)
    mouse_pos = pygame.mouse.get_pos()
    
    current_color = color
    if button_rect.collidepoint(mouse_pos):
        current_color = hover_color
    
    pygame.draw.rect(surface, current_color, button_rect, border_radius=5)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    
    return button_rect

def draw_centered_text(surface, text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    surface.blit(text_surface, text_rect)

def game_loop():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("扫雷")
    
    game = Minesweeper()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // GRID_SIZE
                row = y // GRID_SIZE
                
                if 0 <= row < game.rows and 0 <= col < game.cols:
                    if event.button == 1:  # 左键点击
                        game.reveal(row, col)
                        if game.board[row][col] == -1:
                            running = False
                    elif event.button == 3:  # 右键点击
                        game.toggle_flag(row, col)
        
        # 绘制游戏
        screen.fill(BACKGROUND_COLOR)
        
        # 绘制格子
        for row in range(game.rows):
            for col in range(game.cols):
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                
                if game.revealed[row][col]:
                    pygame.draw.rect(screen, (220, 220, 220), rect)
                    pygame.draw.rect(screen, (180, 180, 180), rect, 1)
                    
                    if game.board[row][col] > 0:
                        number_color = [
                            (0, 0, 255),   # 1
                            (0, 128, 0),    # 2
                            (255, 0, 0),    # 3
                            (0, 0, 128),    # 4
                            (128, 0, 0),    # 5
                            (0, 128, 128),  # 6
                            (0, 0, 0),      # 7
                            (128, 128, 128) # 8
                        ][game.board[row][col] - 1]
                        
                        text = FONT_SMALL.render(str(game.board[row][col]), True, number_color)
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                    elif game.board[row][col] == -1 and game.game_over:
                        pygame.draw.circle(screen, (255, 0, 0), rect.center, GRID_SIZE // 4)
                else:
                    pygame.draw.rect(screen, (160, 160, 160), rect)
                    pygame.draw.rect(screen, (120, 120, 120), rect, 1)
                    
                    if game.flagged[row][col]:
                        pygame.draw.circle(screen, (255, 0, 0), rect.center, GRID_SIZE // 4)
        
        # 检查胜利条件
        if game.check_win() and not game.game_over:
            draw_centered_text(screen, "你赢了！", FONT_LARGE, PRIMARY_COLOR, -50)
            running = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # 游戏结束界面
    button_width = 200
    button_height = 50
    restart_button_y = HEIGHT // 2 + 40
    exit_button_y = restart_button_y + button_height + 20
    
    while True:
        screen.fill(BACKGROUND_COLOR)
        
        # 创建半透明覆盖层
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明黑色背景
        
        # 绘制游戏结束时的棋盘状态
        for row in range(game.rows):
            for col in range(game.cols):
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                
                if game.board[row][col] == -1 or game.revealed[row][col]:
                    pygame.draw.rect(overlay, (220, 220, 220), rect)
                    pygame.draw.rect(overlay, (180, 180, 180), rect, 1)
                    
                    if game.board[row][col] > 0:
                        number_color = [
                            (0, 0, 255),   # 1
                            (0, 128, 0),    # 2
                            (255, 0, 0),    # 3
                            (0, 0, 128),    # 4
                            (128, 0, 0),    # 5
                            (0, 128, 128),  # 6
                            (0, 0, 0),      # 7
                            (128, 128, 128) # 8
                        ][game.board[row][col] - 1]
                        
                        text = FONT_SMALL.render(str(game.board[row][col]), True, number_color)
                        text_rect = text.get_rect(center=rect.center)
                        overlay.blit(text, text_rect)
                    elif game.board[row][col] == -1:
                        pygame.draw.circle(overlay, (255, 0, 0), rect.center, GRID_SIZE // 4)
                elif game.flagged[row][col]:
                    pygame.draw.rect(overlay, (160, 160, 160), rect)
                    pygame.draw.rect(overlay, (120, 120, 120), rect, 1)
                    pygame.draw.circle(overlay, (255, 0, 0), rect.center, GRID_SIZE // 4)
        
        screen.blit(overlay, (0, 0))
        
        # 绘制游戏结果文本
        if game.game_over:
            draw_centered_text(screen, "游戏结束！", FONT_LARGE, PRIMARY_COLOR, -100)
        else:
            draw_centered_text(screen, "你赢了！", FONT_LARGE, PRIMARY_COLOR, -100)
        
        # 绘制按钮（不透明）
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
                if restart_rect.collidepoint(event.pos):  # 点击重新开始按钮
                    return True
                elif exit_rect.collidepoint(event.pos):  # 点击退出游戏按钮
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    while True:
        restart = game_loop()
        if not restart:
            break
    pygame.quit()
    sys.exit()