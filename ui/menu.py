from core.scene import Scene
from core.audio import AudioManager

from constants import WINDOW_X, WINDOW_Y
from style import *

from ui.options import Options

import tkinter as tk
from tkinter.font import Font

class Menu(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.canvas.config(
            bg=BG_COLOR_1
        )

        self.frame_root = tk.Frame(self.canvas)
        self.frame_root.config(
            bg=BG_COLOR_1
        )

        self.options = Options(self)

        self.texture_title = tk.PhotoImage(file = "assets/textures/texture_title.png")

        self.frame_title = tk.Frame(self.frame_root)
        self.frame_title.pack()

        self.label_title = tk.Label(self.frame_title)
        self.label_title.config(
            image=self.texture_title,
            bg=BG_COLOR_1
        )
        self.label_title.pack()

        self.frame_button = tk.Frame(self.frame_root)
        self.frame_button.config(
            bg=BG_COLOR_1
        )
        self.frame_button.pack(pady=10)

        self.button_start = tk.Button(self.frame_button)
        self.button_start.config(
            text="Start",
            font=font_button_small,
            width=25,
            height=1,
            bg=BUTTON_BG,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_ACTIVE_BG, 
            activeforeground="white", 
            relief="flat",
            command=lambda:self.start()
        )
        self.button_start.pack(side=tk.TOP, padx=5, pady=5)

        self.button_opt = tk.Button(self.frame_button)
        self.button_opt.config(
            text="Options",
            font=font_button_small,
            width=25,
            height=1,
            bg=BUTTON_BG,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_ACTIVE_BG, 
            activeforeground="white", 
            relief="flat",
            command=lambda:self.options.open()
        )
        self.button_opt.pack(side=tk.TOP, padx=5, pady=5)

        self.button_lb = tk.Button(self.frame_button)
        self.button_lb.config(
            text="Leaderboard",
            font=font_button_small,
            width=25,
            height=1,
            bg=BUTTON_BG_GREEN,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_ACTIVE_BG_GREEN, 
            activeforeground="white", 
            relief="flat",
            command=lambda:self.view_leaderboard()
        )
        self.button_lb.pack(side=tk.TOP, padx=5, pady=5)

        self.button_exit = tk.Button(self.frame_button)
        self.button_exit.config(
            text="Exit",
            font=font_button_small,
            width=25,
            height=1,
            bg=BUTTON_BG_RED,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_ACTIVE_BG_RED, 
            activeforeground="white", 
            relief="flat",
            command=lambda:exit()
        )
        self.button_exit.pack(side=tk.TOP, padx=5, pady=5)

        self.add_widget(self.frame_root, 0.5, 0.5, "center")

    def start(self):
        self.root.event_generate("<<MenuStart>>")
    
    def view_leaderboard(self, *args):
        self.root.event_generate("<<LeaderboardOpen>>")

    def load(self):
        super().load()

        AudioManager.play_bgm("assets/audio/song/song_menu.ogg")

    def unload(self):
        super().unload()

        AudioManager.stop_bgm()
