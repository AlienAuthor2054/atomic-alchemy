from __future__ import annotations

import tkinter as tk
from time import perf_counter
from random import choices

from constants import WINDOW_X, WINDOW_Y, ATOM_SPAWN_WEIGHTS
from core.element import ELEMENTS_BY_NUM

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
    
    def spawn_atom(self):
        Atom(self, ELEMENTS_BY_NUM[choices(
            list(ATOM_SPAWN_WEIGHTS.keys()),
            list(ATOM_SPAWN_WEIGHTS.values()),
            k=1
        )[0]])

    def atom_spawn_loop(self):
        self.spawn_atom()
        self.root.after(2000, lambda: self.atom_spawn_loop())
