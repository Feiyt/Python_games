# Project Development Guide

[中文说明](Readme.md)
## 1. Introduction

This project is a collection of classic mini-games in Python, accessible via a graphical launcher interface. Currently, it includes Snake, 2048, Gobang (Five-in-a-Row), and Minesweeper.

## 2. Project Structure

```
.
├── 2048/
│   ├── 2048.py            # 2048 game logic and UI
│   └── high_score.txt     # 2048 high score record
├── Gobang/
│   ├── ManAndMachine.py   # Gobang (PvE) logic and UI
│   ├── ManAndMan.py       # Gobang (PvP) logic and UI
│   └── checkerboard.py    # Shared board logic and piece definitions
├── Minesweeper/
│   └── Minesweeper.py     # Minesweeper game logic and UI
├── Snake/
│   └── Snake-eating.py    # Snake game logic and UI
├── resource/
│   ├── fonts/
│   │   └── simsun.ttc     # Font file used by the launcher (SimSun)
│   └── images/
│       ├── 2048.ico       # 2048 icon
│       ├── gobang.ico     # Gobang icon
│       ├── minesweeper.ico # Minesweeper icon
│       └── snake.ico      # Snake icon
├── .idea/                   # IDE config files (e.g., PyCharm, VSCode)
├── game_launcher.py       # Main entry - Tkinter-based game selector UI
├── Readme.md         # Project documentation (Chinese)
├── Readme-en.md      # This file - Project documentation (English)
├── .gitignore             # Git ignore file
└── requirements.txt       # Project dependencies
```

## 3. Core Technologies

*   **Python 3:** Main programming language.
*   **Pygame:** Used for core gameplay, graphics rendering, and event handling in all games (Snake, 2048, Gobang, Minesweeper).
*   **Tkinter:** Used to create the GUI for `game_launcher.py`, allowing users to select and launch games.
*   **PIL (Pillow):** Used by the Tkinter launcher (`game_launcher.py`) to load and display game icons (`.ico` files).
*   **Standard Library:** `os`, `sys`, `random`, `subprocess`, `ctypes`, `math` for tasks like file path operations, system interaction, random number generation, launching game processes, DPI awareness (Windows), and calculations.

## 4. Unified UI Style (Pygame Games)

To provide a consistent look and feel, all Pygame-based games (Snake, 2048, Gobang, Minesweeper) use a unified visual style.

*   **Goal:** Deliver a consistent user experience.
*   **Implementation:** Constants and drawing functions are defined in each game's Python file.
*   **Palette:**
    *   `BACKGROUND_COLOR`: `(200, 200, 200)` (light gray) - main background.
    *   `PRIMARY_COLOR`: `(50, 50, 150)` (medium blue) - main UI elements, buttons, some text.
    *   `SECONDARY_COLOR`: `(100, 100, 200)` (light blue) - secondary elements.
    *   `ACCENT_COLOR`: `(255, 215, 0)` (gold) - highlights, button hover, food/score elements.
    *   `TEXT_COLOR`: `(0, 0, 0)` (black) - default text color.
    *   `BUTTON_TEXT_COLOR`: `(255, 255, 255)` (white) - button text.
    *   `GRID_LINE_COLOR`: `(100, 100, 100)` (dark gray) - grid lines/borders in Gobang, 2048, and Minesweeper.
    *   *Gobang piece colors:* Explicitly black `(0,0,0)` and white `(255,255,255)`.
    *   *Minesweeper number colors:* 1-8 use distinct colors (blue, green, red, dark blue, brown, teal, black, gray).
    *   *Minesweeper flag/mine color:* Red `(255,0,0)`.
*   **Fonts:**
    *   `FONT_FAMILY`: `"SimHei"` - unified across all games.
    *   `FONT_SMALL`: size 20 or 24
    *   `FONT_MEDIUM`: size 30 or 36
    *   `FONT_LARGE`: size 48
    *   Specific fonts (e.g., `FONT_TILE` in 2048) may use different sizes but the same family.
*   **Buttons (`draw_button` function):**
    *   Rounded rectangles (`border_radius=5`).
    *   Background uses `PRIMARY_COLOR`.
    *   Hover effect changes background to `ACCENT_COLOR`.
    *   Text uses `BUTTON_TEXT_COLOR` and standard font.
    *   Padding around text for better visuals.

## 5. Game Modules

*   **Snake (`Snake/Snake-eating.py`):**
    *   Classic snake game where the player controls a growing snake.
    *   Goal: Eat food (gold circles) to score and grow longer.
    *   Lose: Hitting the wall or itself.
    *   Controls: Arrow keys or WASD.
    *   Speed: Controlled by `FPS` constant (currently `6.48`).
*   **2048 (`2048/2048.py`):**
    *   Puzzle game merging numbered tiles.
    *   Goal: Slide and merge tiles to reach 2048.
    *   Play: Use arrow keys or WASD to move tiles. Same numbers merge into double. A new tile (2 or 4) appears after each move.
    *   Feature: Tracks current and high score (saved in `2048/high_score.txt`).
*   **Gobang (`Gobang/`):**
    *   Goal: First to connect five pieces in a row (horizontal, vertical, diagonal).
    *   Pieces: Black and white (black goes first).
    *   Shared logic: `checkerboard.py` manages board state and win checks for both modes.
    *   Modes:
        *   `ManAndMachine.py`: Player vs AI. Basic AI scoring and move selection. Shows player/AI info and win/loss stats.
        *   `ManAndMan.py`: Player vs Player (local turn-based). Shows player info.
*   **Minesweeper (`Minesweeper/Minesweeper.py`):**
    *   Classic logic puzzle game.
    *   Goal: Uncover all squares that do not contain mines, avoiding clicking on mines.
    *   Play: Left-click reveals a square. Numbers on squares indicate the count of adjacent mines. Right-click flags/unflags a square suspected of containing a mine.
    *   Features: First click is guaranteed safe. Includes game over and win condition checks. Offers "Restart" and "Exit" options upon game completion.

## 6. How to Run

1.  Make sure **Python 3** is installed.
2.  Install necessary libraries listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    # Or manually install:
    # pip install Pillow pygame
    ```
3.  In your terminal, navigate to the project's root directory.
4.  Run the game launcher:
    ```bash
    python game_launcher.py
    ```
    (Depending on your system configuration, it might be `python3 game_launcher.py`).
5.  The launcher window will appear. Click the button for the game you want to play.
6.  The selected game will start in a new window. The launcher uses `subprocess.Popen` to run the game scripts independently.

## 7. Resources (`resource/`)

*   **`fonts/`:** Contains font files used by the application (currently `simsun.ttc` for the Tkinter launcher).
*   **`images/`:** Contains icon files (`.ico`) used by the buttons in the Tkinter launcher. Ensure a corresponding icon is provided for each game (e.g., `minesweeper.ico`).
