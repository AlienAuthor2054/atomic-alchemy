from constants import WINDOW_X, WINDOW_Y

from core.scene import Scene

import tkinter as tk

class Window():
    def __init__(self, scene: Scene):
        self.scene = scene
        self.canvas = self.scene.canvas

        self.is_open = False

        self.window = tk.Frame(self.canvas)
        self.window.pack_propagate(False)

        self.id_window = self.scene.add_widget(self.window, 0.5, 0.5, "center")
        self.canvas.itemconfigure(self.id_window, state='hidden')

    def open(self):
        self.is_open = True
        self.canvas.itemconfigure(self.id_window, state='normal')
        self.canvas.bind("<ButtonPress-1>", self.close)

    def close(self, *args):
        self.is_open = False
        self.canvas.itemconfigure(self.id_window, state='hidden')
        self.canvas.unbind("<ButtonPress-1>")