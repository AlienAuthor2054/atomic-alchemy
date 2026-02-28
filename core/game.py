from __future__ import annotations

import tkinter as tk
from time import perf_counter

from constants import WINDOW_X, WINDOW_Y

from .atom import Atom
from .lab import Lab

class Game():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.prev_time: float = 0.0
        self.physics_objects = set()
        canvas = tk.Canvas(root, width=WINDOW_X, height=WINDOW_Y)
        canvas.pack()
        self.canvas = canvas
        self.lab = Lab(self)

    def start(self):
        self.atom_spawn_loop()
        self.root.after(0, self.loop)

    def loop(self):
        delta = perf_counter() - self.prev_time
        self.tick(delta)
        self.prev_time = perf_counter()
        self.root.after(8, lambda: self.loop())
    
    def tick(self, delta):
        for obj in self.physics_objects.copy():
            obj.physics_process(delta)
    
    def atom_spawn_loop(self):
        Atom(self, 1)
        self.root.after(2000, lambda: self.atom_spawn_loop())
