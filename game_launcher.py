import tkinter as tk
from PIL import Image, ImageTk
import os
import platform
import subprocess  # 导入 subprocess 模块
import ctypes  # 用于设置字体 DPI 感知

# 设置字体 DPI 感知，确保字体显示正常
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass

# 确定操作系统并选择合适的启动方式
def run_game(file_path):
    try:
        # 获取当前脚本所在目录的绝对路径
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建游戏的完整路径
        game_path = os.path.join(base_dir, file_path)

        # 检查游戏文件是否存在
        if not os.path.exists(game_path):
            tk.messagebox.showerror("游戏路径错误", f"找不到游戏文件: {game_path}")
            return

        # 使用 subprocess 运行游戏，避免打开终端窗口
        if platform.system() == "Windows":
            subprocess.Popen(['python', game_path], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen(['python3', game_path])

    except Exception as e:
        tk.messagebox.showerror("启动游戏错误", f"启动游戏时发生错误: {str(e)}")


class GameLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏选择器")
        self.root.geometry("800x600")  # 增大初始窗口尺寸
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)  # 允许窗口调整大小

        # 设置自定义字体
        self.set_custom_font()

        # 加载图标
        self.load_icons()

        # 标题
        self.title_label = tk.Label(
            root,
            text="点击开始游戏",
            font=self.title_font,
            bg="#f0f0f0"
        )
        self.title_label.pack(pady=30)

        # 主菜单框架
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=10)

        # 创建带有图标的按钮
        self.create_button_with_icon(
            self.main_frame,
            self.snake_icon,
            "贪吃蛇",
            "#4CAF50",
            lambda: run_game("Snake/Snake-eating.py")
        )

        self.create_button_with_icon(
            self.main_frame,
            self.twenty_icon,
            "2048",
            "#2196F3",
            lambda: run_game("2048/2048.py")
        )

        self.create_button_with_icon(
            self.main_frame,
            self.gobang_icon,
            "五子棋",
            "#9C27B0",
            lambda: self.show_gomoku_options()
        )

        # 退出按钮
        self.exit_button = tk.Button(
            self.main_frame,
            text="退出",
            font=self.button_font,
            bg="#f44336",
            fg="white",
            padx=20,
            pady=1,
            command=self.root.destroy
        )
        self.exit_button.pack(fill="x", pady=50)

        # 五子棋选项框架（初始隐藏）
        self.gomoku_frame = tk.Frame(root, bg="#f0f0f0")

    def set_custom_font(self):
        # 设置自定义字体
        try:
            # 获取当前脚本所在目录的绝对路径
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建字体文件的完整路径
            font_path = os.path.join(base_dir, "resource", "fonts", "simsun.ttc")

            # 检查字体文件是否存在
            if os.path.exists(font_path):
                # 创建自定义字体
                self.title_font = ("SimSun", 25, "bold")
                self.button_font = ("SimSun", 16)
                self.label_font = ("SimSun", 20, "bold")
            else:
                tk.messagebox.showerror("字体文件错误", f"找不到字体文件: {font_path}")
                # 如果字体文件不存在，使用默认字体
                self.title_font = ("Arial", 25, "bold")
                self.button_font = ("Arial", 16)
                self.label_font = ("Arial", 20, "bold")
        except Exception as e:
            tk.messagebox.showerror("设置字体时发生错误", f"设置字体时发生错误: {str(e)}")
            # 如果发生错误，使用默认字体
            self.title_font = ("Arial", 25, "bold")
            self.button_font = ("Arial", 16)
            self.label_font = ("Arial", 20, "bold")

    def load_icons(self):
        # 图标路径（相对于当前脚本目录）
        size = (48, 48)

        # 获取当前脚本所在目录的绝对路径
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建图标文件的完整路径
        snake_icon_path = os.path.join(base_dir, "resource", "images", "snake.ico")
        gobang_icon_path = os.path.join(base_dir, "resource", "images", "gobang.ico")
        twenty_icon_path = os.path.join(base_dir, "resource", "images", "2048.ico")

        # 检查图标文件是否存在
        if not os.path.exists(snake_icon_path):
            tk.messagebox.showerror("图标路径错误", f"找不到图标文件: {snake_icon_path}")
            # 如果图标不存在，创建一个默认图标
            self.snake_icon = None
        else:
            # 打开图标文件并调整大小
            self.snake_icon = Image.open(snake_icon_path)
            self.snake_icon.thumbnail(size, Image.Resampling.LANCZOS)
            self.snake_icon = ImageTk.PhotoImage(self.snake_icon)

        if not os.path.exists(gobang_icon_path):
            tk.messagebox.showerror("图标路径错误", f"找不到图标文件: {gobang_icon_path}")
            self.gobang_icon = None
        else:
            self.gobang_icon = Image.open(gobang_icon_path)
            self.gobang_icon.thumbnail(size, Image.Resampling.LANCZOS)
            self.gobang_icon = ImageTk.PhotoImage(self.gobang_icon)

        if not os.path.exists(twenty_icon_path):
            tk.messagebox.showerror("图标路径错误", f"找不到图标文件: {twenty_icon_path}")
            self.twenty_icon = None
        else:
            self.twenty_icon = Image.open(twenty_icon_path)
            self.twenty_icon.thumbnail(size, Image.Resampling.LANCZOS)
            self.twenty_icon = ImageTk.PhotoImage(self.twenty_icon)

    def create_button_with_icon(self, parent, icon, text, color, command):
        # 创建一个水平布局的框架
        button_frame = tk.Frame(parent, bg="#f0f0f0")
        button_frame.pack(fill="x", pady=10)

        # 创建按钮（实际按钮将覆盖整个框架）
        button = tk.Button(
            button_frame,
            text=text,
            font=self.button_font,
            bg=color,
            fg="white",
            padx=20,
            pady=15,
            command=command,
            compound="left",  # 图标在左侧
            image=icon
        )
        button.pack(fill="x")

        # 保存对图像的引用，防止被垃圾回收
        button.image = icon

    def show_gomoku_options(self):
        # 切换到五子棋选项界面
        self.main_frame.pack_forget()

        # Clear any previous widgets in the gomoku frame
        for widget in self.gomoku_frame.winfo_children():
            widget.destroy()

        # 创建返回按钮
        back_button = tk.Button(
            self.gomoku_frame,
            text="返回主菜单",
            font=self.button_font,
            bg="#607D8B",
            fg="white",
            padx=10,
            pady=5,
            command=self.return_to_main
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        # 五子棋标题
        title_label = tk.Label(
            self.gomoku_frame,
            text="请选择五子棋模式",
            font=self.label_font,
            bg="#f0f0f0"
        )
        title_label.pack(pady=30)

        # 创建带有图标的按钮
        self.create_button_with_icon(
            self.gomoku_frame,
            self.gobang_icon,
            "人机对战",
            "#3F51B5",
            lambda: run_game("Gobang/ManAndMachine.py")
        )

        self.create_button_with_icon(
            self.gomoku_frame,
            self.gobang_icon,
            "真人对战",
            "#673AB7",
            lambda: run_game("Gobang/ManAndMan.py")
        )

        # 显示五子棋选项界面
        self.gomoku_frame.pack(expand=True, fill="both", padx=40, pady=10)

    def return_to_main(self):
        # Clear gomoku frame before hiding
        for widget in self.gomoku_frame.winfo_children():
            widget.destroy()
        # 返回主菜单
        self.gomoku_frame.pack_forget()
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncherApp(root)
    root.mainloop()