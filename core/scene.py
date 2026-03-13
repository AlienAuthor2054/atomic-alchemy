import tkinter as tk

from constants import WINDOW_X, WINDOW_Y
from typing import Literal

from pygame import mixer

class Scene():
    def __init__(self, root: tk.Tk):
        self.root = root

        self.canvas = tk.Canvas(root, width=WINDOW_X, height=WINDOW_Y)

        self.mixer = mixer
        self.mixer.pre_init(44100, -16, 2, 512)
        self.mixer.init()

    def add_widget(self, widget: tk.Widget, norm_x: float, norm_y: float,
        anchor: Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se']
    ):
        """
        Embeds a `widget` onto the game canvas.

        Only use for adding gameplay UI,
        not out-of-game UI like title screen, game over screen, etc.

        `norm_x` and `norm_y` are values from 0 to 1
        describing the widget's position relative to the window.
        """
        window_id = self.canvas.create_window(
            norm_x * WINDOW_X,
            norm_y * WINDOW_Y,
            window=widget,
            anchor=anchor,
        )

        return window_id

    def load(self):
        self.canvas.pack(fill='both')

    def unload(self):
        self.canvas.pack_forget()