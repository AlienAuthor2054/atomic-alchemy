from core.scene import Scene
from constants import WINDOW_X, WINDOW_Y

import tkinter as tk
from tkinter.font import Font

class Menu(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        h1 = Font(family="Comic Sans MS", size=20)
        h3 = Font(family="Comic Sans MS", size=10)

        frame_root = tk.Frame(self.canvas)

        frame_title = tk.Frame(frame_root)
        frame_title.pack()

        label = tk.Label(frame_title, text="Atomic Alchemy", font=h1)
        label.pack()

        frame_button = tk.Frame(frame_root)
        frame_button.pack(pady=10)

        button_start = tk.Button(frame_button, text="Start", font=h3, width=10, command=lambda:self.start())
        button_start.pack(side=tk.LEFT, padx=5)

        button_opt = tk.Button(frame_button, text="Options", font=h3, width=10)
        button_opt.pack(side=tk.LEFT, padx=5)

        button_exit = tk.Button(frame_button, text="Exit", font=h3, width=10, command=lambda:exit())
        button_exit.pack(side=tk.LEFT, padx=5)

        self.add_widget(frame_root, 0.5, 0.5, "center")

    def start(self):
        self.root.event_generate("<<MenuStart>>")

    def opt_open(self):
        pass

    def opt_close(self):
        pass