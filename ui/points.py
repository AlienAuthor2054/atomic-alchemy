import tkinter as tk

from core import Game

class PointsFrame(tk.Frame):
    def __init__(self, game: Game):
        super().__init__(game.canvas)
        label = tk.Label(self, textvariable=game.points, font="TkFixedFont 60",
            bg="yellow", bd=10, relief="ridge"
        )
        label.grid(column=0, row=0)
