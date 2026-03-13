import tkinter as tk

class PointsFrame(tk.Frame):
    def __init__(self, root, points_var):
        super().__init__(root)
        label = tk.Label(self, textvariable=points_var, font="TkFixedFont 60",
            bg="yellow", bd=10, relief="ridge"
        )
        label.grid(column=0, row=0)
