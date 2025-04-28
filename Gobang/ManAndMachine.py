import sys
import random
import pygame
from pygame.locals import *
import pygame.gfxdraw
from checkerboard import Checkerboard, Point, offset
from checkerboard import BLACK_CHESSMAN as B_Orig, WHITE_CHESSMAN as W_Orig, Chessman

# --- Unified Style Constants ---
SIZE = 30  # Grid spacing
Line_Points = 19
Outer_Width = 20
Border_Width = 4
Inside_Width = 4
Border_Length = SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width
Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width
# Adjust screen height if necessary, keeping width for info panel
SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2
SCREEN_WIDTH = SCREEN_HEIGHT + 200 # Keep the info panel width

Stone_Radius = SIZE // 2 - 3
Stone_Radius2 = SIZE // 2 + 3 # For info panel display

# Colors (Matching Snake/2048)
BACKGROUND_COLOR = (200, 200, 200) # Light Gray
PRIMARY_COLOR = (50, 50, 150)      # Medium Blue (Used for UI elements)
SECONDARY_COLOR = (100, 100, 200) # Lighter Blue
ACCENT_COLOR = (255, 215, 0)       # Gold
TEXT_COLOR = (0, 0, 0)             # Black
BUTTON_TEXT_COLOR = (255, 255, 255) # White
GRID_LINE_COLOR = (100, 100, 100) # Dark Gray
# --- Modify Piece Colors --- 
PLAYER1_COLOR = (0, 0, 0) # Black pieces
PLAYER2_COLOR = (255, 255, 255) # White pieces (AI)
# --- End Piece Color Modification ---
INFO_TEXT_COLOR = PRIMARY_COLOR # Keep UI text blue
WINNER_TEXT_COLOR = PRIMARY_COLOR

# Fonts (Matching Snake/2048)
FONT_FAMILY = "SimHei"
pygame.font.init() # Ensure font system is initialized
FONT_SMALL = pygame.font.SysFont(FONT_FAMILY, 24)
FONT_MEDIUM = pygame.font.SysFont(FONT_FAMILY, 36)
FONT_LARGE = pygame.font.SysFont(FONT_FAMILY, 48)
# --- End Unified Style Constants ---

# --- Redefine Chessman at module level with unified colors ---
# Check if original Chessman objects exist before redefining
if B_Orig and W_Orig and Chessman:
    BLACK_CHESSMAN = Chessman(B_Orig.Name, B_Orig.Value, PLAYER1_COLOR) # Use new Black
    WHITE_CHESSMAN = Chessman(W_Orig.Name, W_Orig.Value, PLAYER2_COLOR) # Use new White
else:
    # Fallback or error if checkerboard didn't load correctly
    print("Error: Could not load Chessman definitions from checkerboard.py")
    sys.exit()
# --- End Redefinition ---

RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10

def print_text(screen, font, x, y, text, fcolor=TEXT_COLOR): # Default to TEXT_COLOR
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

# --- Standardized Button Function ---
def draw_button(surface, text, font, x, y, width, height, color, hover_color, text_color):
    text_surf_temp = font.render(text, True, text_color)
    text_width, text_height = text_surf_temp.get_size()
    padded_width = max(width, text_width + 40) 
    button_rect = pygame.Rect(0, 0, padded_width, height)
    button_rect.center = (x + width // 2, y + height // 2)
    mouse_pos = pygame.mouse.get_pos()
    current_color = color
    if button_rect.collidepoint(mouse_pos):
        current_color = hover_color
    pygame.draw.rect(surface, current_color, button_rect, border_radius=5)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    return button_rect
# --- End Standardized Button Function ---

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
                    return True
                elif event.key == K_q or event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                 if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):
                        return True
                    elif exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
        pygame.time.Clock().tick(15)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('五子棋 (人机)')

    font_info = FONT_SMALL # Use standard small font for info

    checkerboard = Checkerboard(Line_Points)
    cur_runner = BLACK_CHESSMAN # Use globally defined BLACK_CHESSMAN
    winner = None
    computer = AI(Line_Points, WHITE_CHESSMAN) # Use globally defined WHITE_CHESSMAN

    black_win_count = 0 # Corresponds to PLAYER1
    white_win_count = 0 # Corresponds to PLAYER2

    while True:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() # Quit pygame cleanly
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if winner is None and event.button == 1: # Check left click
                    if cur_runner.Value == BLACK_CHESSMAN.Value: # Only allow clicks if it's Player 1's turn
                        mouse_pos = pygame.mouse.get_pos()
                        click_point = _get_clickpoint(mouse_pos)
                        if click_point is not None:
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(cur_runner, click_point)
                                if winner is None:
                                    # Player move complete, switch to AI
                                    computer.get_opponent_drop(click_point) # Update AI's board
                                    cur_runner = _get_next(cur_runner)
                                    # --- AI Turn Trigger --- 
                                    # AI makes its move immediately after player
                                else:
                                    black_win_count += 1 # Player 1 wins
                            else:
                                print('不可落子') # More user-friendly message
                        else:
                            print('超出棋盘区域')
                    else:
                        print("现在是电脑的回合") # Inform user it's not their turn
                        
        # --- AI Turn Logic (if it's AI's turn and game is not over) ---
        if winner is None and cur_runner.Value == WHITE_CHESSMAN.Value:
            pygame.time.wait(100) # Small delay to simulate thinking
            print("电脑正在思考...")
            AI_point = computer.AI_drop()
            if AI_point and checkerboard.can_drop(AI_point): # Check if AI returned a valid and droppable point
                winner = checkerboard.drop(cur_runner, AI_point)
                if winner is not None:
                    white_win_count += 1 # AI (Player 2) wins
                # AI move complete, switch back to Player
                cur_runner = _get_next(cur_runner)
            elif AI_point is None:
                # AI couldn't find any move (e.g., board full - draw?)
                print("AI无法移动 - 可能平局?")
                # Implement draw logic if needed
                # For now, maybe just pass the turn back? Or declare draw.
                # Let's just skip the turn switch if AI returns None
                pass 
            else: # AI chose an invalid spot (shouldn't happen with can_drop check in AI, but safety)
                 print(f"AI 选择了无效位置: {AI_point} - 跳过回合")
                 # Switch turn back to player if AI messes up badly
                 cur_runner = _get_next(cur_runner)

        # --- Drawing --- 
        screen.fill(BACKGROUND_COLOR)
        _draw_checkerboard(screen)
        for i, row in enumerate(checkerboard.checkerboard):
            for j, cell in enumerate(row):
                if cell == BLACK_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                elif cell == WHITE_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)
        _draw_right_info(screen, font_info, cur_runner, black_win_count, white_win_count)

        # --- Game Over Check --- 
        if winner:
            if show_end_screen(screen, winner):
                # Reset game state
                winner = None
                cur_runner = BLACK_CHESSMAN
                checkerboard = Checkerboard(Line_Points)
                computer = AI(Line_Points, WHITE_CHESSMAN)
                # Reset win counts or keep them?
                # black_win_count = 0
                # white_win_count = 0
            else: # If show_end_screen returns False (e.g. closed window) 
                break # Exit main loop

        pygame.display.flip()
        pygame.time.Clock().tick(30) # Lower tick rate slightly
    
    pygame.quit() # Quit pygame if main loop exits
    sys.exit()


def _get_next(cur_runner):
    # Compares against globally defined Chessman objects
    if cur_runner.Value == BLACK_CHESSMAN.Value:
        return WHITE_CHESSMAN
    else:
        return BLACK_CHESSMAN


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

# Renamed from _draw_left_info - Revised Positioning
def _draw_right_info(screen, font, cur_runner, player1_wins, player2_wins):
    panel_x_start = SCREEN_HEIGHT # Start of the info panel area
    padding = 15
    y_pos = Start_Y # Start drawing from same top alignment as board grid

    # Player 1 Info
    p1_indicator_pos = (panel_x_start + Stone_Radius2 + padding, y_pos + Stone_Radius2)
    _draw_chessman_pos(screen, p1_indicator_pos, PLAYER1_COLOR)
    p1_text_surf = font.render('玩家', True, INFO_TEXT_COLOR)
    p1_text_rect = p1_text_surf.get_rect(midleft=(p1_indicator_pos[0] + Stone_Radius2 + 10, p1_indicator_pos[1]))
    screen.blit(p1_text_surf, p1_text_rect)
    y_pos += Stone_Radius2 * 3 # Move y_pos down for next item

    # Player 2 Info
    p2_indicator_pos = (panel_x_start + Stone_Radius2 + padding, y_pos + Stone_Radius2)
    _draw_chessman_pos(screen, p2_indicator_pos, PLAYER2_COLOR)
    p2_text_surf = font.render('电脑', True, INFO_TEXT_COLOR)
    p2_text_rect = p2_text_surf.get_rect(midleft=(p2_indicator_pos[0] + Stone_Radius2 + 10, p2_indicator_pos[1]))
    screen.blit(p2_text_surf, p2_text_rect)
    
    # Current Turn Indicator
    if cur_runner.Value == BLACK_CHESSMAN.Value:
        turn_indicator_rect = p1_text_rect
    else:
        turn_indicator_rect = p2_text_rect
    turn_text_surf = font.render('<-', True, ACCENT_COLOR)
    # Position indicator to the right of the player text
    turn_text_rect = turn_text_surf.get_rect(midleft=(turn_indicator_rect.right + 10, turn_indicator_rect.centery))
    screen.blit(turn_text_surf, turn_text_rect)

    y_pos += Stone_Radius2 * 4 # Add more space before scores

    # Scores Title
    score_title_surf = font.render('战况:', True, INFO_TEXT_COLOR)
    score_title_rect = score_title_surf.get_rect(topleft=(panel_x_start + padding, y_pos))
    screen.blit(score_title_surf, score_title_rect)
    y_pos += score_title_rect.height + 10 # Move down below title

    # P1 Score
    p1_score_indicator_pos = (panel_x_start + Stone_Radius2 + padding, y_pos + Stone_Radius2)
    _draw_chessman_pos(screen, p1_score_indicator_pos, PLAYER1_COLOR)
    p1_score_surf = font.render(f'{player1_wins} 胜', True, INFO_TEXT_COLOR)
    p1_score_rect = p1_score_surf.get_rect(midleft=(p1_score_indicator_pos[0] + Stone_Radius2 + 10, p1_score_indicator_pos[1]))
    screen.blit(p1_score_surf, p1_score_rect)
    y_pos += Stone_Radius2 * 3 # Move down for P2 score

    # P2 Score
    p2_score_indicator_pos = (panel_x_start + Stone_Radius2 + padding, y_pos + Stone_Radius2)
    _draw_chessman_pos(screen, p2_score_indicator_pos, PLAYER2_COLOR)
    p2_score_surf = font.render(f'{player2_wins} 胜', True, INFO_TEXT_COLOR)
    p2_score_rect = p2_score_surf.get_rect(midleft=(p2_score_indicator_pos[0] + Stone_Radius2 + 10, p2_score_indicator_pos[1]))
    screen.blit(p2_score_surf, p2_score_rect)

def _draw_chessman_pos(screen, pos, stone_color):
    # This function is fine, uses the passed (unified) color
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Stone_Radius2, stone_color)


def _get_clickpoint(click_pos):
    # Check bounds relative to the checkerboard area only
    board_start_x = Outer_Width
    board_start_y = Outer_Width
    board_end_x = board_start_x + Border_Length
    board_end_y = board_start_y + Border_Length

    if not (board_start_x <= click_pos[0] <= board_end_x and 
            board_start_y <= click_pos[1] <= board_end_y):
        return None # Click is outside the board border

    # Calculate relative position and grid index
    pos_x = click_pos[0] - Start_X
    pos_y = click_pos[1] - Start_Y
    
    # Determine closest intersection point
    x = round(pos_x / SIZE)
    y = round(pos_y / SIZE)

    # Check if calculated indices are within valid range
    if 0 <= x < Line_Points and 0 <= y < Line_Points:
         # Check if the click is close enough to the intersection point
         click_radius_sq = (pos_x - x * SIZE)**2 + (pos_y - y * SIZE)**2
         if click_radius_sq <= (SIZE // 2)**2: # Click within half grid size radius
              return Point(x, y)

    return None # Click not close enough to an intersection or out of bounds


class AI:
    def __init__(self, line_points, chessman):
        self._line_points = line_points
        self._my = chessman # Should be WHITE_CHESSMAN (global)
        # Use global objects for comparison
        self._opponent = BLACK_CHESSMAN if chessman.Value == WHITE_CHESSMAN.Value else WHITE_CHESSMAN
        self._checkerboard = [[0] * line_points for _ in range(line_points)]

    def get_opponent_drop(self, point):
        if 0 <= point.Y < self._line_points and 0 <= point.X < self._line_points:
             self._checkerboard[point.Y][point.X] = self._opponent.Value
        else:
             print(f"AI Error: Opponent drop out of bounds: {point}")


    def AI_drop(self):
        point = None
        score = -1 # Initialize score to allow 0-score moves if necessary
        empty_cells = []

        for i in range(self._line_points):
            for j in range(self._line_points):
                if self._checkerboard[j][i] == 0:
                    cell_point = Point(i, j)
                    empty_cells.append(cell_point)
                    _score = self._get_point_score(cell_point)
                    # Simple Tie-breaking: Prefer center-ish moves for same score
                    is_better_tiebreak = False
                    if _score == score and point is not None:
                         # Calculate distance from center (9, 9)
                         dist_sq_new = (i - (self._line_points // 2))**2 + (j - (self._line_points // 2))**2
                         dist_sq_old = (point.X - (self._line_points // 2))**2 + (point.Y - (self._line_points // 2))**2
                         if dist_sq_new < dist_sq_old: # Prefer closer to center
                              is_better_tiebreak = True

                    if _score > score or is_better_tiebreak:
                        score = _score
                        point = cell_point
        
        # Fallback: If no move found with score > -1 (or preferred tiebreak)
        if point is None:
            if empty_cells:
                # Choose randomly from available cells as last resort
                point = random.choice(empty_cells)
                print("AI choosing random move.")
            else:
                print("AI Error: No empty cells found!")
                return None

        # Ensure point is valid before updating internal board and returning
        if point and 0 <= point.Y < self._line_points and 0 <= point.X < self._line_points:
             self._checkerboard[point.Y][point.X] = self._my.Value
             print(f"AI chooses: ({point.X}, {point.Y}) with score {score}")
             return point
        else:
             print(f"AI Error: Invalid point selected: {point}")
             # Try random again if point became invalid? Or just fail.
             if empty_cells: return random.choice(empty_cells) 
             return None


    def _get_point_score(self, point):
        score = 0
        for os in offset:
            score += self._get_direction_score(point, os[0], os[1])
        # Add a small bonus for center positions
        center_bonus = 0
        center_dist_sq = (point.X - self._line_points // 2)**2 + (point.Y - self._line_points // 2)**2
        max_dist_sq = (self._line_points // 2)**2 * 2
        center_bonus = (1 - (center_dist_sq / max_dist_sq)) * 5 # Max bonus of 5 for exact center
        return score + center_bonus

    # --- Scoring logic based on counts and blocking ---
    # (This detailed scoring logic seems complex and might need tweaking for balance)
    # Keeping the original scoring logic for now. 
    def _get_direction_score(self, point, x_offset, y_offset):
        count = 0   # My continuous stones including the potential drop point (starts at 1 conceptually)
        _count = 0  # Opponent continuous stones adjacent to potential drop point
        my_blocked = 0    # Ends blocked for my potential line
        opp_blocked = 0   # Ends blocked for opponent's adjacent line

        # Check one direction
        live_ends_my = 0
        empty_in_line_my = 0
        consecutive_my = 0
        for i in range(1, 5): # Check up to 4 spaces away for potential 5-in-a-row
            x = point.X + i * x_offset
            y = point.Y + i * y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points:
                if self._checkerboard[y][x] == self._my.Value:
                    consecutive_my += 1
                elif self._checkerboard[y][x] == 0:
                    live_ends_my +=1
                    break # Found an empty space, line is 'live' on this end
                else: # Opponent's stone
                    my_blocked += 1
                    break # Blocked on this end
            else: # Off board
                my_blocked += 1
                break
        count += consecutive_my
        
        # Check opposite direction
        consecutive_my = 0 # Reset for opposite direction
        for i in range(1, 5):
            x = point.X - i * x_offset
            y = point.Y - i * y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points:
                if self._checkerboard[y][x] == self._my.Value:
                     consecutive_my += 1
                elif self._checkerboard[y][x] == 0:
                    live_ends_my += 1
                    break
                else:
                    my_blocked += 1
                    break
            else:
                my_blocked += 1
                break
        count += consecutive_my

        # --- Calculate My Score based on count and blocks ---
        # (Using original game's logic structure for scoring mapping)
        # This needs careful mapping to prioritize winning/blocking moves
        my_score = 0
        if count >= 4: # Forms 5-in-a-row
             my_score = 10000
        elif count == 3: 
             if live_ends_my == 2: my_score = 1000 # Live four
             elif live_ends_my == 1: my_score = 100 # Dead four
        elif count == 2:
             if live_ends_my == 2: my_score = 100 # Live three
             elif live_ends_my == 1: my_score = 10 # Dead three
        elif count == 1:
             if live_ends_my == 2: my_score = 10 # Live two
             elif live_ends_my == 1: my_score = 1 # Dead two
        
        # --- Check Opponent Threat ---
        # Check opponent's potential lines if we *don't* place here
        # This is complex - the original code seems to calculate this differently.
        # Let's adapt the opponent check similar to how 'my' check was done.
        
        live_ends_opp = 0
        consecutive_opp = 0
        # Check one direction for opponent stones adjacent to the potential drop point
        for i in range(1, 5): 
            x = point.X + i * x_offset
            y = point.Y + i * y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points:
                if self._checkerboard[y][x] == self._opponent.Value:
                    consecutive_opp += 1
                elif self._checkerboard[y][x] == 0:
                    live_ends_opp +=1
                    break 
                else: # My stone
                    opp_blocked += 1
                    break 
            else: # Off board
                opp_blocked += 1
                break
        _count += consecutive_opp

        # Check opposite direction for opponent
        consecutive_opp = 0 
        for i in range(1, 5):
            x = point.X - i * x_offset
            y = point.Y - i * y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points:
                if self._checkerboard[y][x] == self._opponent.Value:
                     consecutive_opp += 1
                elif self._checkerboard[y][x] == 0:
                    live_ends_opp += 1
                    break
                else:
                    opp_blocked += 1
                    break
            else:
                opp_blocked += 1
                break
        _count += consecutive_opp
        
        # --- Calculate Opponent Score (Threat level) ---
        opp_score = 0
        if _count >= 4: # Block opponent's 5-in-a-row
             opp_score = 9000 
        elif _count == 3: 
             if live_ends_opp == 2: opp_score = 900 # Block live four
             elif live_ends_opp == 1: opp_score = 90 # Block dead four
        elif _count == 2:
             if live_ends_opp == 2: opp_score = 90 # Block live three
             elif live_ends_opp == 1: opp_score = 9 # Block dead three
        elif _count == 1:
             if live_ends_opp == 2: opp_score = 9 # Block live two
             # elif live_ends_opp == 1: opp_score = 1 # Block dead two (less important)

        # Return the higher score (either my offensive score or defensive score)
        return max(my_score, opp_score)


    # This helper seems unused or less useful with the revised scoring logic
    def _get_stone_color(self, point, x_offset, y_offset, next):
        x = point.X + x_offset
        y = point.Y + y_offset
        if 0 <= x < self._line_points and 0 <= y < self._line_points:
            if self._checkerboard[y][x] == self._my.Value:
                return 1
            elif self._checkerboard[y][x] == self._opponent.Value:
                return 2
            else: # Empty
                 # Original logic recursively checked next empty, might be complex/slow
                 return 0 
        else: # Off board
            return -1 # Indicate blocked/off board


if __name__ == '__main__':
    main()