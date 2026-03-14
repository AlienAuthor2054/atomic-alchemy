from constants import WINDOW_X, WINDOW_Y

from core.scene import Scene

import tkinter as tk

class Window():
    def __init__(self, scene: Scene):
        self.scene = scene
        self.canvas = self.scene.canvas

        self.window = tk.Frame(self.canvas)
        self.window.pack_propagate(False)

        self.id_window = self.scene.add_widget(self.window, 0.5, 0.5, "center")
        self.canvas.itemconfigure(self.id_window, state='hidden')

        print("Window Init")

    def open(self):
        self.canvas.itemconfigure(self.id_window, state='normal')
        self.canvas.bind("<ButtonPress-1>", self.close)

        print("Window Open")

    def close(self, event):
        self.canvas.itemconfigure(self.id_window, state='hidden')
        self.canvas.unbind("<ButtonPress-1>")

        print("Window Close")