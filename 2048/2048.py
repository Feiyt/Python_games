import pygame
import random
import sys # Import sys for exit
import math # For tile color calculation
import os # For file operations

# 初始化 Pygame
pygame.init()
# pygame.font.init() is called by pygame.init()

# --- Unified Style Constants ---
# Game constants
GRID_COLUMNS = 4
GRID_ROWS = 4
BLOCK_SIZE = 100
HEADER_HEIGHT = 70 # Increased header height for score/buttons
INFO_PANEL_HEIGHT = HEADER_HEIGHT
GAME_GRID_HEIGHT = GRID_ROWS * BLOCK_SIZE
SCREEN_WIDTH = GRID_COLUMNS * BLOCK_SIZE
SCREEN_HEIGHT = GAME_GRID_HEIGHT + INFO_PANEL_HEIGHT

# Colors
BACKGROUND_COLOR = (200, 200, 200) # Light Gray
PRIMARY_COLOR = (50, 50, 150)      # Medium Blue
SECONDARY_COLOR = (100, 100, 200) # Lighter Blue
ACCENT_COLOR = (255, 215, 0)       # Gold
TEXT_COLOR = (0, 0, 0)             # Black
BUTTON_TEXT_COLOR = (255, 255, 255) # White
GRID_LINE_COLOR = (100, 100, 100) # Dark Gray
TILE_TEXT_COLOR = TEXT_COLOR # Use standard text color for tiles
EMPTY_TILE_COLOR = (180, 180, 180) # Slightly darker gray for empty cells

# Fonts
FONT_FAMILY = "SimHei"
FONT_SMALL = pygame.font.SysFont(FONT_FAMILY, 24)
FONT_MEDIUM = pygame.font.SysFont(FONT_FAMILY, 36)
FONT_LARGE = pygame.font.SysFont(FONT_FAMILY, 48)
# Specific font for tile numbers, adjust size as needed
FONT_TILE = pygame.font.SysFont(FONT_FAMILY, 40)
# --- End Unified Style Constants ---

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")

# Clock for FPS control
clock = pygame.time.Clock()

# --- Tile Color Calculation ---
def get_tile_color(value):
    """Generates a color for a tile based on its value.
       Uses SECONDARY_COLOR as a base and darkens it for higher values.
    """
    if value == 0:
        return EMPTY_TILE_COLOR
    # Logarithmic scale for color variation (or simple mapping)
    # Simple approach: Start with SECONDARY, shift towards PRIMARY/ACCENT?
    # Let's try interpolating towards ACCENT_COLOR for higher values
    log_val = math.log2(value) if value > 0 else 0
    # Max value approx log2(2048) = 11. Scale factor 0 to 1.
    factor = min(log_val / 11.0, 1.0)
    r = int(SECONDARY_COLOR[0] * (1 - factor) + ACCENT_COLOR[0] * factor)
    g = int(SECONDARY_COLOR[1] * (1 - factor) + ACCENT_COLOR[1] * factor)
    b = int(SECONDARY_COLOR[2] * (1 - factor) + ACCENT_COLOR[2] * factor)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

# --- Game Logic Functions (mostly unchanged) ---
def move_row_left(row):
    filtered = [num for num in row if num != 0]
    new_row = []
    i = 0
    while i < len(filtered):
        if i < len(filtered) - 1 and filtered[i] == filtered[i + 1]:
            new_row.append(filtered[i] * 2)
            i += 2
        else:
            new_row.append(filtered[i])
            i += 1
    new_row += [0] * (GRID_COLUMNS - len(new_row))  # 补齐列数
    return new_row


def transpose(grid):
    return [list(row) for row in zip(*grid)]


def reverse(grid):
    return [row[::-1] for row in grid]


def add_new_tile(grid):
    empty_cells = []
    for i in range(GRID_ROWS):
        for j in range(GRID_COLUMNS):
            if grid[i][j] == 0:
                empty_cells.append((i, j))
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[x][y] = random.choice([2, 4])


def check_win(grid):
    for row in grid:
        if 2048 in row:
            return True
    return False


def check_lose(grid):
    for row in grid:
        if 0 in row:
            return False
    for i in range(GRID_ROWS):
        for j in range(GRID_COLUMNS):
            if (i < GRID_ROWS - 1 and grid[i][j] == grid[i + 1][j]) or (
                    j < GRID_COLUMNS - 1 and grid[i][j] == grid[i][j + 1]):
                return False
    return True


def calculate_score(grid):
    # Simple score: sum of all tiles
    score = 0
    for r in range(GRID_ROWS):
        for c in range(GRID_COLUMNS):
            score += grid[r][c]
    return score

# --- Drawing Functions (Updated Styles) ---
def draw_grid_and_tiles(grid):
    """Draws the background grid and the tiles.
       Assumes the screen background (header area) is already filled.
    """
    # Draw background grid squares
    for r in range(GRID_ROWS):
        for c in range(GRID_COLUMNS):
            rect = pygame.Rect(c * BLOCK_SIZE, INFO_PANEL_HEIGHT + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            tile_val = grid[r][c]
            tile_color = get_tile_color(tile_val) 
            pygame.draw.rect(screen, tile_color, rect)
            # Draw tile value
            if tile_val != 0:
                text_surface = FONT_TILE.render(str(tile_val), True, TILE_TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    # Draw grid lines over the tiles
    line_width = 5
    for i in range(GRID_ROWS + 1):
        y = INFO_PANEL_HEIGHT + i * BLOCK_SIZE
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, y), (SCREEN_WIDTH, y), line_width)
    for i in range(GRID_COLUMNS + 1):
        x = i * BLOCK_SIZE
        pygame.draw.line(screen, GRID_LINE_COLOR, (x, INFO_PANEL_HEIGHT), (x, SCREEN_HEIGHT), line_width)

# Standardized Button Function (Updated Padding Logic)
def draw_button(surface, text, font, x, y, width, height, color, hover_color, text_color):
    # Calculate text size for padding
    text_surf_temp = font.render(text, True, text_color)
    text_width, text_height = text_surf_temp.get_size()
    
    # Add padding to the provided width, or use text width + padding
    padded_width = max(width, text_width + 40) 
    
    button_rect = pygame.Rect(0, 0, padded_width, height) # Create rect with 0,0 first
    # Center the button based on the original x, y and width provided
    # (Assuming x, y here refers to the *center* of the desired button area)
    button_rect.center = (x, y) # Center rect around x,y 
    
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouse_pos)
    current_color = hover_color if is_hovered else color
    
    pygame.draw.rect(surface, current_color, button_rect, border_radius=5)
    
    # Render text again
    text_surface = font.render(text, True, text_color)
    # Center text in the potentially wider button_rect
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    
    # Return the actual drawn rect and hover state (useful for click detection)
    return button_rect, is_hovered 

# --- Game State Functions (Movement unchanged, High Score Added) ---
def move_up(grid):
    transposed = transpose(grid)
    new_transposed = []
    changed = False
    for row in transposed:
        new_row = move_row_left(row)
        new_transposed.append(new_row)
        if new_row != row:
            changed = True
    new_grid = transpose(new_transposed)
    return new_grid, changed


def move_down(grid):
    transposed = transpose(grid)
    new_transposed = []
    changed = False
    for row in transposed:
        row = row[::-1]
        new_row = move_row_left(row)
        new_row = new_row[::-1]
        new_transposed.append(new_row)
        if new_row != row[::-1]:
            changed = True
    new_grid = transpose(new_transposed)
    return new_grid, changed


def move_left(grid):
    new_grid = []
    changed = False
    for row in grid:
        new_row = move_row_left(row)
        new_grid.append(new_row)
        if new_row != row:
            changed = True
    return new_grid, changed


def move_right(grid):
    new_grid = []
    changed = False
    for row in grid:
        row = row[::-1]
        new_row = move_row_left(row)
        new_row = new_row[::-1]
        new_grid.append(new_row)
        if new_row != row[::-1]:
            changed = True
    return new_grid, changed

def load_high_score():
    # Define the correct path relative to the project root or script location
    # Assuming the script runs from the project root, the path is '2048/high_score.txt'
    # If the script's CWD is uncertain, build an absolute path
    try:
        script_dir = os.path.dirname(__file__) # Get directory of the current script
        file_path = os.path.join(script_dir, "high_score.txt") # Path relative to script dir
        # Or if you are sure CWD is project root:
        # file_path = "2048/high_score.txt"
        with open(file_path, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    except ValueError:
        print(f"Warning: Could not parse high score from {file_path}")
        return 0
    except Exception as e:
        print(f"Error loading high score: {e}")
        return 0


def save_high_score(score):
    try:
        script_dir = os.path.dirname(__file__) # Get directory of the current script
        file_path = os.path.join(script_dir, "high_score.txt") # Path relative to script dir
        # Or if you are sure CWD is project root:
        # file_path = "2048/high_score.txt"
        with open(file_path, "w") as file:
            file.write(str(score))
    except Exception as e:
        print(f"Error saving high score to {file_path}: {e}")

# --- Main Menu (Updated Style) ---
def main_menu():
    button_width = 200
    button_height = 50
    # Define button center positions
    start_button_center_x = SCREEN_WIDTH // 2
    start_button_center_y = SCREEN_HEIGHT // 2 - button_height // 2 # Adjust y slightly
    exit_button_center_y = start_button_center_y + button_height + 20

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Title
        title_surf = FONT_LARGE.render("2048 Game", True, PRIMARY_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_surf, title_rect)

        # Buttons - Pass center coordinates to draw_button
        start_button_rect, start_hover = draw_button(
            screen, "开始游戏", FONT_MEDIUM,
            start_button_center_x, start_button_center_y, # Pass center X, Y
            button_width, button_height,
            PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR
        )
        exit_button_rect, exit_hover = draw_button(
            screen, "退出游戏", FONT_MEDIUM,
            start_button_center_x, exit_button_center_y, # Pass center X, Y
            button_width, button_height,
            PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR
        )

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # Exit cleanly
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button_rect.collidepoint(event.pos):
                        return True  # Start game
                    elif exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit() # Exit cleanly

        pygame.display.flip()
        clock.tick(30) # Lower tick rate for menu

    # Should only be reached if loop broken unexpectedly
    pygame.quit()
    sys.exit()

# --- Game Over Screen (Updated Style) ---
def game_over_screen(score, high_score):
    button_width = 200
    button_height = 50
    # Define button center positions
    restart_button_center_x = SCREEN_WIDTH // 2
    restart_button_center_y = SCREEN_HEIGHT * 0.6 + button_height // 2
    menu_button_center_y = restart_button_center_y + button_height + 20

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Game Over Text
        go_text = FONT_LARGE.render("游戏结束!", True, PRIMARY_COLOR)
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.2))
        screen.blit(go_text, go_rect)

        # Score Text
        score_text = FONT_MEDIUM.render(f"得分: {score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.35))
        screen.blit(score_text, score_rect)
        
        hs_text = FONT_MEDIUM.render(f"最高分: {high_score}", True, TEXT_COLOR)
        hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.45))
        screen.blit(hs_text, hs_rect)

        # Buttons - Pass center coordinates
        restart_button_rect, _ = draw_button(
            screen, "重新开始 (R)", FONT_MEDIUM,
            restart_button_center_x, restart_button_center_y, # Pass center X, Y
            button_width, button_height,
            PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR
        )
        menu_button_rect, _ = draw_button(
            screen, "返回菜单 (M)", FONT_MEDIUM,
            restart_button_center_x, menu_button_center_y, # Pass center X, Y
            button_width, button_height,
            PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR
        )

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_m:
                    return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if restart_button_rect.collidepoint(event.pos):
                        return "restart"
                    elif menu_button_rect.collidepoint(event.pos):
                        return "menu"

        pygame.display.flip()
        clock.tick(30)

# --- Main Game Loop (Updated Style and Logic) ---
def main():
    while True: # Outer loop to handle returning to menu
        if not main_menu(): # Show main menu, exit if it returns False
             break

        # --- Initialize Game State ---
        grid = [[0] * GRID_COLUMNS for _ in range(GRID_ROWS)]
        add_new_tile(grid)
        add_new_tile(grid)
        high_score = load_high_score()
        current_score = 0
        game_over = False
        # No separate show_menu flag needed now, handled by game_over state
        
        # --- Inner Game Loop ---
        running_game = True
        while running_game:
            changed = False # Track if a move happened
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and not game_over:
                    new_grid = grid # Keep pylint happy
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        new_grid, changed = move_up(grid)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        new_grid, changed = move_down(grid)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        new_grid, changed = move_left(grid)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        new_grid, changed = move_right(grid)
                    # Add key for reset?
                    # elif event.key == pygame.K_n:
                    #     running_game = False # Go back to menu to restart
                    
                    if changed:
                        grid = new_grid
                        add_new_tile(grid)
                        current_score = calculate_score(grid) # Update score
                        if current_score > high_score:
                            high_score = current_score # Update high score live
                        # Check game end conditions after move
                        if check_win(grid):
                            # Simple win message for now
                            print("You reached 2048!") 
                            # game_over = True # Could set game over on win
                        if check_lose(grid):
                            game_over = True
                            save_high_score(high_score) # Save score on lose

            # --- Drawing --- 
            screen.fill(BACKGROUND_COLOR) # Fill whole background
            
            # Draw Header/Info Panel
            score_text = FONT_MEDIUM.render(f"得分: {current_score}", True, TEXT_COLOR)
            score_rect = score_text.get_rect(midleft=(10, INFO_PANEL_HEIGHT // 4))
            screen.blit(score_text, score_rect)
            
            hs_text = FONT_MEDIUM.render(f"最高分: {high_score}", True, TEXT_COLOR)
            hs_rect = hs_text.get_rect(midleft=(10, INFO_PANEL_HEIGHT * 0.75))
            screen.blit(hs_text, hs_rect)
            
            # Optional: Add a small 'New Game' button in header?
            # new_game_button, _ = draw_button(screen, "New", FONT_SMALL, SCREEN_WIDTH - 70, 10, 60, 30, PRIMARY_COLOR, ACCENT_COLOR, BUTTON_TEXT_COLOR)
            # Check new_game_button click here if added

            # Draw Grid and Tiles
            draw_grid_and_tiles(grid)

            # --- Game Over Handling ---
            if game_over:
                action = game_over_screen(current_score, high_score)
                if action == "restart":
                    running_game = False # Break inner loop to restart
                elif action == "menu":
                    running_game = False # Break inner loop
                    # Need a way to signal outer loop to not call main_menu again? 
                    # Or just let it call main_menu again. Simpler.
                    break # Exit inner loop, outer loop will call main_menu()

            pygame.display.flip()
            clock.tick(60)
            
# Start the game
if __name__ == "__main__":
    main()