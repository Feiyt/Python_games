# 项目开发说明

[English](Readme-en.md)


本项目是一个包含多个经典小游戏的 Python 应用合集，通过一个图形化的启动器界面进行访问。目前包含贪吃蛇、2048、五子棋和扫雷游戏。

## 1. 项目结构

```
.
├── 2048/
│   ├── 2048.py            # 2048 游戏逻辑与 UI
│   └── high_score.txt     # 2048 最高分记录文件
├── Gobang/
│   ├── ManAndMachine.py   # 五子棋人机对战逻辑与 UI
│   ├── ManAndMan.py       # 五子棋人人对战逻辑与 UI
│   └── checkerboard.py    # 五子棋共享棋盘逻辑与棋子定义
├── Minesweeper/
│   └── Minesweeper.py     # 扫雷游戏逻辑与 UI
├── Snake/
│   └── Snake-eating.py    # 贪吃蛇游戏逻辑与 UI
├── resource/
│   ├── fonts/
│   │   └── simsun.ttc     # 启动器使用的字体文件 (宋体)
│   └── images/
│       ├── 2048.ico       # 2048 图标
│       ├── gobang.ico     # 五子棋图标
│       ├── minesweeper.ico # 扫雷图标
│       └── snake.ico      # 贪吃蛇图标
├── .idea/                   # IDE 配置文件 (例如 PyCharm, VSCode)
├── game_launcher.py       # 主入口 - 基于 Tkinter 的游戏选择器 UI
├── Readme.md         # 本文件 - 项目文档 (中文)
├── Readme-en.md      # 项目文档 (英文)
├── .gitignore             # Git 忽略文件
└── requirements.txt       # 项目依赖库
```

## 2. 核心技术

*   **Python 3:** 主要编程语言。
*   **Pygame:** 用于开发各个游戏（贪吃蛇、2048、五子棋、扫雷）的核心玩法、图形渲染、事件处理。
*   **Tkinter:** 用于创建 `game_launcher.py` 的图形用户界面 (GUI)，允许用户选择并启动不同的游戏。
*   **PIL (Pillow):** Tkinter 启动器 (`game_launcher.py`) 使用该库加载并显示按钮上的游戏图标 (`.ico` 文件)。
*   **标准库:** `os`, `sys`, `random`, `subprocess`, `ctypes`, `math` 用于各种任务，如文件路径操作、系统交互、随机数生成、启动游戏进程、DPI 感知 (Windows) 和计算。

## 3. 统一 UI 风格 (Pygame 游戏)

为了提供统一的外观和体验，所有基于 Pygame 的游戏（贪吃蛇、2048、五子棋、扫雷）都应用了一致的视觉风格。

*   **目标:** 提供统一的用户体验。
*   **实现:** 在每个游戏的 Python 文件中定义常量和绘图函数。
*   **调色板:**
    *   `BACKGROUND_COLOR`: `(200, 200, 200)` (浅灰色) - 主背景。
    *   `PRIMARY_COLOR`: `(50, 50, 150)` (中蓝色) - 主要 UI 元素、按钮、部分文本。
    *   `SECONDARY_COLOR`: `(100, 100, 200)` (亮蓝色) - 次要元素。
    *   `ACCENT_COLOR`: `(255, 215, 0)` (金色) - 高亮、按钮悬停效果、食物/分数元素。
    *   `TEXT_COLOR`: `(0, 0, 0)` (黑色) - 默认文本颜色。
    *   `BUTTON_TEXT_COLOR`: `(255, 255, 255)` (白色) - 按钮上的文本。
    *   `GRID_LINE_COLOR`: `(100, 100, 100)` (深灰色) - 五子棋、2048、扫雷中的网格线/边框。
    *   *五子棋棋子颜色:* 明确指定为黑色 `(0,0,0)` 和白色 `(255,255,255)`。
    *   *扫雷数字颜色:* 1-8 分别使用不同的颜色（蓝、绿、红、深蓝、棕、青、黑、灰）。
    *   *扫雷旗帜/地雷颜色:* 红色 `(255,0,0)`。
*   **字体:**
    *   `FONT_FAMILY`: `"SimHei"` - 在所有游戏中统一使用。
    *   `FONT_SMALL`: 字号 20 或 24
    *   `FONT_MEDIUM`: 字号 30 或 36
    *   `FONT_LARGE`: 字号 48
    *   特定字体（例如 2048 中的 `FONT_TILE`）可能使用不同字号，但保持同一字体家族。
*   **按钮 (`draw_button` 函数):**
    *   带圆角的矩形 (`border_radius=5`)。
    *   背景使用 `PRIMARY_COLOR`。
    *   悬停效果将背景变为 `ACCENT_COLOR`。
    *   文本使用 `BUTTON_TEXT_COLOR` 和标准字体。
    *   在文本周围添加了内边距，以获得更好的视觉效果。

## 4. 游戏模块

*   **贪吃蛇 (`Snake/Snake-eating.py`):**
    *   经典的贪吃蛇游戏，玩家控制一条不断增长的蛇。
    *   目标：吃食物（金色圆圈）得分并变长。
    *   失败条件：撞到屏幕边界或蛇自身。
    *   控制：方向键 或 WASD。
    *   速度：由 `FPS` 常量控制（当前为 `6.48`）。
*   **2048 (`2048/2048.py`):**
    *   合并数字方块的益智游戏。
    *   目标：滑动网格上的数字方块，将它们合并，最终得到数字为 2048 的方块。
    *   玩法：使用方向键或 WASD 移动方块。相同数字的方块会合并成一个数字翻倍的方块。每次移动后会随机出现一个新的方块（2 或 4）。
    *   特色：记录当前分数和最高分（保存在 `2048/high_score.txt` 文件中）。
*   **五子棋 (`Gobang/`):**
    *   目标：率先将五个自己的棋子连成一线（横、竖、斜）。
    *   棋子：黑色和白色（黑棋先走）。
    *   共享逻辑： `checkerboard.py` 包含棋盘状态管理和胜利条件检查逻辑，供两种模式使用。
    *   模式：
        *   `ManAndMachine.py`：玩家 vs AI。包含基本的 AI 评分和走棋选择逻辑。显示玩家/AI 信息和胜负统计。
        *   `ManAndMan.py`：玩家 vs 玩家（本地轮流）。显示玩家信息。
*   **扫雷 (`Minesweeper/Minesweeper.py`):**
    *   经典的逻辑解谜游戏。
    *   目标：找出所有没有地雷的方块，避免点开地雷。
    *   玩法：鼠标左键点击揭开方块。方块上的数字表示周围八个格子中地雷的数量。鼠标右键点击可以标记或取消标记疑似有地雷的方块。
    *   特色：首次点击保证安全。包含游戏结束和胜利判断。提供重新开始和退出选项。

## 5. 如何运行

1.  确保已安装 **Python 3**。
2.  根据 `requirements.txt` 安装必要的库：
    ```bash
    pip install -r requirements.txt
    # 或者手动安装:
    # pip install Pillow pygame
    ```
3.  在终端中，切换到项目的根目录。
4.  运行游戏启动器：
    ```bash
    python game_launcher.py
    ```
    （根据你的系统配置，也可能是 `python3 game_launcher.py`）。
5.  启动器窗口将会出现。点击所需游戏的按钮。
6.  选定的游戏将在新窗口中启动。启动器使用 `subprocess.Popen` 独立运行游戏脚本。

## 6. 资源 (`resource/`)

*   **`fonts/`:** 包含应用程序使用的字体文件（当前为供 Tkinter 启动器使用的 `simsun.ttc`）。
*   **`images/`:** 包含 Tkinter 启动器中按钮使用的图标文件 (`.ico`)。确保为每个游戏提供对应的图标 (例如 `minesweeper.ico`)。

