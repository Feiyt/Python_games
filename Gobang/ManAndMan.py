import sys
import pygame
from pygame.locals import *
import pygame.gfxdraw
from checkerboard import Checkerboard, Point
from checkerboard import BLACK_CHESSMAN as B_Orig, WHITE_CHESSMAN as W_Orig, Chessman

# --- Unified Style Constants ---
SIZE = 30
Line_Points = 19
Outer_Width = 20
Border_Width = 4
Inside_Width = 4
Border_Length = SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width
Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width
SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2
SCREEN_WIDTH = SCREEN_HEIGHT + 200 # Keep info panel width

Stone_Radius = SIZE // 2 - 3
Stone_Radius2 = SIZE // 2 + 3

# Colors (Same as ManAndMachine)
BACKGROUND_COLOR = (200, 200, 200) # Light Gray
PRIMARY_COLOR = (50, 50, 150)      # Medium Blue (Used for UI elements like buttons)
SECONDARY_COLOR = (100, 100, 200) # Lighter Blue
ACCENT_COLOR = (255, 215, 0)       # Gold
TEXT_COLOR = (0, 0, 0)             # Black
BUTTON_TEXT_COLOR = (255, 255, 255) # White
GRID_LINE_COLOR = (100, 100, 100) # Dark Gray
# --- Modify Piece Colors --- 
PLAYER1_COLOR = (0, 0, 0) # Black pieces
PLAYER2_COLOR = (255, 255, 255) # White pieces
# --- End Piece Color Modification ---
INFO_TEXT_COLOR = PRIMARY_COLOR # Keep UI text blue
WINNER_TEXT_COLOR = PRIMARY_COLOR

# Fonts (Same as ManAndMachine)
FONT_FAMILY = "SimHei"
pygame.font.init()
FONT_SMALL = pygame.font.SysFont(FONT_FAMILY, 24)
FONT_MEDIUM = pygame.font.SysFont(FONT_FAMILY, 36)
FONT_LARGE = pygame.font.SysFont(FONT_FAMILY, 48)
# --- End Unified Style Constants ---

# --- Redefine Chessman at module level with unified colors ---
if B_Orig and W_Orig and Chessman:
    BLACK_CHESSMAN = Chessman(B_Orig.Name, B_Orig.Value, PLAYER1_COLOR) # Uses new Black
    WHITE_CHESSMAN = Chessman(W_Orig.Name, W_Orig.Value, PLAYER2_COLOR) # Uses new White
else:
    print("Error: Could not load Chessman definitions from checkerboard.py")
    sys.exit()
# --- End Redefinition ---

RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10

# --- Add Missing Drawing Functions (Copied from ManAndMachine.py) ---
def _draw_checkerboard(screen):
    # Use unified colors for board background and lines
    # screen.fill(BACKGROUND_COLOR) # Filling handled in main loop now
    pygame.draw.rect(screen, GRID_LINE_COLOR, (Outer_Width, Outer_Width, Border_Length, Border_Length), Border_Width)
    for i in range(Line_Points):
        pygame.draw.line(screen, GRID_LINE_COLOR,
                         (Start_Y, Start_Y + SIZE * i),
                         (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i), 1)
    for j in range(Line_Points):
        pygame.draw.line(screen, GRID_LINE_COLOR,
                         (Start_X + SIZE * j, Start_X),
                         (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)), 1)
    star_point_color = TEXT_COLOR # Use standard text color for star points
    for i in (3, 9, 15):
        for j in (3, 9, 15):
            radius = 5 if i == j == 9 else 3
            pygame.gfxdraw.aacircle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, star_point_color)
            pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, star_point_color)

def _draw_chessman(screen, point, stone_color):
    # This function is fine, uses the passed (unified) color
    pygame.gfxdraw.aacircle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)
    pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)

def _draw_chessman_pos(screen, pos, stone_color):
    # This function is fine, uses the passed (unified) color
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
# --- End Add Missing Drawing Functions ---

# Updated click detection (same as ManAndMachine)
def _get_clickpoint(click_pos):
    board_start_x = Outer_Width
    board_start_y = Outer_Width
    board_end_x = board_start_x + Border_Length
    board_end_y = board_start_y + Border_Length
    if not (board_start_x <= click_pos[0] <= board_end_x and 
            board_start_y <= click_pos[1] <= board_end_y):
        return None
    pos_x = click_pos[0] - Start_X
    pos_y = click_pos[1] - Start_Y
    x = round(pos_x / SIZE)
    y = round(pos_y / SIZE)
    if 0 <= x < Line_Points and 0 <= y < Line_Points:
         click_radius_sq = (pos_x - x * SIZE)**2 + (pos_y - y * SIZE)**2
         if click_radius_sq <= (SIZE // 2)**2:
              return Point(x, y)
    return None

# Updated show_end_screen (Similar to ManAndMachine)
def show_end_screen(screen, winner):
    screen.fill(BACKGROUND_COLOR)
    win_text = "平局"
    if winner:
        player_name = getattr(winner, 'Name', '获胜方') 
        win_text = f"{player_name} 获胜"
    text_surface = FONT_LARGE.render(win_text, True, WINNER_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(text_surface, text_rect)

    button_width = 250
    button_height = 50
    restart_button_y = SCREEN_HEIGHT // 2
    exit_button_y = restart_button_y + button_height + 20

    restart_rect = draw_button(
        screen, "重新开始 (R)", FONT_MEDIUM,
        SCREEN_WIDTH // 2 - button_width // 2, restart_button_y, button_width, button_height,
        PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR
    )
    exit_rect = draw_button(
        screen, "退出游戏 (Q)", FONT_MEDIUM,
        SCREEN_WIDTH // 2 - button_width // 2, exit_button_y, button_width, button_height,
        PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR
    )
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return True # Indicate restart
                elif event.key == K_q or event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                 if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):
                        return True # Indicate restart
                    elif exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
        pygame.time.Clock().tick(15)
    # Should not be reached if loop is exited via return True
    # If loop exits otherwise (e.g., bug), default to not restarting
    return False 

# --- Standardized Button Function ---
def draw_button(surface, text, font, x, y, width, height, color, hover_color, text_color):
    """Draws a button on the screen."""
    mouse_pos = pygame.mouse.get_pos()
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

# Updated function for drawing info panel in Man vs Man mode
def _draw_right_info_pvp(screen, font, cur_runner):
    """Draws the information panel on the right for Player vs Player mode."""
    panel_x_start = SCREEN_HEIGHT # Start of the info panel area
    padding = 15
    y_pos = Start_Y # Start drawing from same top alignment as board grid

    # Player 1 Info
    p1_indicator_pos = (panel_x_start + Stone_Radius2 + padding, y_pos + Stone_Radius2)
    _draw_chessman_pos(screen, p1_indicator_pos, PLAYER1_COLOR) # Use Black
    p1_text_surf = font.render('玩家 1', True, INFO_TEXT_COLOR)
    p1_text_rect = p1_text_surf.get_rect(midleft=(p1_indicator_pos[0] + Stone_Radius2 + 10, p1_indicator_pos[1]))
    screen.blit(p1_text_surf, p1_text_rect)
    y_pos += Stone_Radius2 * 3 # Move y_pos down for next item

    # Player 2 Info
    p2_indicator_pos = (panel_x_start + Stone_Radius2 + padding, y_pos + Stone_Radius2)
    _draw_chessman_pos(screen, p2_indicator_pos, PLAYER2_COLOR) # Use White
    p2_text_surf = font.render('玩家 2', True, INFO_TEXT_COLOR)
    p2_text_rect = p2_text_surf.get_rect(midleft=(p2_indicator_pos[0] + Stone_Radius2 + 10, p2_indicator_pos[1]))
    screen.blit(p2_text_surf, p2_text_rect)
    
    # Current Turn Indicator
    if cur_runner.Value == BLACK_CHESSMAN.Value:
        turn_indicator_rect = p1_text_rect
    else:
        turn_indicator_rect = p2_text_rect
    turn_text_surf = font.render('<-', True, ACCENT_COLOR)
    turn_text_rect = turn_text_surf.get_rect(midleft=(turn_indicator_rect.right + 10, turn_indicator_rect.centery))
    screen.blit(turn_text_surf, turn_text_rect)
    
    # No score tracking in PvP mode

def main():
    """Main game loop for the Player vs Player mode."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('五子棋 (双人)')

    font_info = FONT_MEDIUM # Use standard medium font for info

    checkerboard = Checkerboard(Line_Points)
    cur_runner = BLACK_CHESSMAN # Start with Black (global, now black color)
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if winner is None and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    click_point = _get_clickpoint(mouse_pos)
                    if click_point is not None:
                        if checkerboard.can_drop(click_point):
                            winner = checkerboard.drop(cur_runner, click_point)
                            if winner is None:
                                # Switch player using global objects
                                if cur_runner.Value == BLACK_CHESSMAN.Value:
                                    cur_runner = WHITE_CHESSMAN
                                else:
                                    cur_runner = BLACK_CHESSMAN
                        else:
                             print('不可落子')
                    else:
                        print('超出棋盘区域')

        # Draw background first
        screen.fill(BACKGROUND_COLOR)
        # Draw checkerboard on top
        _draw_checkerboard(screen)

        # Draw pieces using global colors
        for i, row in enumerate(checkerboard.checkerboard):
            for j, cell in enumerate(row):
                if cell == BLACK_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                elif cell == WHITE_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)

        # Draw PvP info panel
        _draw_right_info_pvp(screen, font_info, cur_runner)

        if winner:
            if show_end_screen(screen, winner): # Returns True if Restart selected
                 # Reset game state
                winner = None
                cur_runner = BLACK_CHESSMAN # Reset to player 1 (global)
                checkerboard = Checkerboard(Line_Points)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == '__main__':
    main()