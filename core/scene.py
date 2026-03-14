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
    ) -> None:
        """
        Embeds a `widget` onto the scene canvas.

        Previously reserved for gameplay UI, its anchor-based placement system 
        was found useful for positioning UI elements in general.

        `norm_x` and `norm_y` are values from 0 to 1
        describing the widget's position relative to the window.
        """
        self.canvas.create_window(
            norm_x * WINDOW_X,
            norm_y * WINDOW_Y,
            window=widget,
            anchor=anchor,
        )

    def load(self):
        self.canvas.pack(fill='both')

    def unload(self):
        self.canvas.pack_forget()