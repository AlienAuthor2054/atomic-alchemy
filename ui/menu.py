from core.scene import Scene
from constants import WINDOW_X, WINDOW_Y

from ui.options import Options

import tkinter as tk
from tkinter.font import Font

class Menu(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        h1 = Font(family="Comic Sans MS", size=20)
        h3 = Font(family="Comic Sans MS", size=10)

        BG_COLOR = "#FDF6E3"

        self.canvas.config(bg=BG_COLOR)

        self.frame_root = tk.Frame(self.canvas, bg=BG_COLOR)

        self.options = Options(self)

        self.texture_title = tk.PhotoImage(file = f"assets\\textures\\texture_title.png")

        self.frame_title = tk.Frame(self.frame_root)
        self.frame_title.pack()

        self.label_title = tk.Label(self.frame_title, image=self.texture_title, bg=BG_COLOR)
        self.label_title.pack()

        self.frame_button = tk.Frame(self.frame_root, bg=BG_COLOR)
        self.frame_button.pack(pady=10)

        self.button_start = tk.Button(self.frame_button, text="Start", font=h3, width=25, height=1, command=lambda:self.start())
        self.button_start.pack(side=tk.TOP, padx=5, pady=5)

        self.button_opt = tk.Button(self.frame_button, text="Options", font=h3, width=25, height=1, command=lambda:self.options.open())
        self.button_opt.pack(side=tk.TOP, padx=5, pady=5)

        self.button_exit = tk.Button(self.frame_button, text="Exit", font=h3, width=25, height=1, command=lambda:exit())
        self.button_exit.pack(side=tk.TOP, padx=5, pady=5)

        self.add_widget(self.frame_root, 0.5, 0.5, "center")

    def start(self):
        self.root.event_generate("<<MenuStart>>")
