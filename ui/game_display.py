import tkinter as tk

from typing import Literal
from constants import WINDOW_X, WINDOW_Y

class GameDisplay:
    def __init__(self, canvas, str_var, texture, norm_x: float, norm_y: float, anchor: Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se']):
        self.canvas = canvas
        self.str_var = str_var

        self.x = norm_x * WINDOW_X
        self.y = norm_y * WINDOW_Y

        self.texture = tk.PhotoImage(file=texture)
        self.image = self.canvas.create_image(
            self.x,
            self.y,
            image=self.texture,
            anchor=anchor
        )

        img_w = self.texture.width()  
        img_h = self.texture.height()

        center_x = self.x
        center_y = self.y

        if 'w' in anchor: 
            center_x += img_w / 2
        elif 'e' in anchor: 
            center_x -= img_w / 2

        if 'n' in anchor: 
            center_y += img_h / 2
        elif 's' in anchor: 
            center_y -= img_h / 2

        offset_x = 5

        self.text = self.canvas.create_text(
            center_x + offset_x,
            center_y,
            text=self.str_var.get(),
            font=("TkFixedFont", 35),
            fill = "black",
        )

        self.str_var.trace_add("write", self.update_text)
    
    def update_text(self, *args):
        self.canvas.itemconfig(self.text, text=self.str_var.get())
