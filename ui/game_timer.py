import tkinter as tk

from core import Game

class TimerFrame(tk.Frame):
    def __init__(self, game: Game):
        super().__init__(game.canvas)
        label = tk.Label(self, textvariable=game.time_var, font="TkFixedFont 60",
            bg="white", bd=10, relief="ridge"
        )
        label.grid(column=0, row=0)
