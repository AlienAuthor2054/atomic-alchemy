from __future__ import annotations

import tkinter as tk
from time import perf_counter, time
from typing import TYPE_CHECKING, Callable, Literal
from random import choices

from constants import WINDOW_X, WINDOW_Y, ATOM_SPAWN_WEIGHTS
from core.element import ELEMENTS_BY_NUM
from util.point import Point

from .atom import Atom
from .lab import Lab
from .scoring import score_bond_change
if TYPE_CHECKING:
    from .bond import Bond

from .audio import Audio

class Game():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.prev_time: float = 0.0
        self.physics_objects = set()
        self._atoms_by_item_id: dict[int, Atom] = {} # For atom collision detection
        canvas = tk.Canvas(root, width=WINDOW_X, height=WINDOW_Y)
        canvas.pack(fill='both')
        self.canvas = canvas
        self.lab = Lab(self)
        self._points = 0
        self.points_var = tk.IntVar()

        self.time_var = tk.StringVar()
        self.time_started = int(time())
        self.time_finished = False
        self.time_set = 180

        self.mixer = Audio().mixer
        self.mixer.music.load(filename='assets\\audio\song\song_placeholder.ogg') # not actual song lol
        self.mixer.music.set_volume(0.25)
        self.mixer.music.play(-1)
        
    @property
    def points(self) -> int:
        return self._points
    
    @points.setter
    def points(self, new: int) -> None:
        self._points = new
        self.points_var.set(new)

    def add_widget(self, widget: tk.Widget, norm_x: float, norm_y: float,
        anchor: Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se']
    ) -> None:
        """
        Embeds a `widget` onto the game canvas.

        Only use for adding gameplay UI,
        not out-of-game UI like title screen, game over screen, etc.

        `norm_x` and `norm_y` are values from 0 to 1
        describing the widget's position relative to the window.
        """
        self.canvas.create_window(
            norm_x * WINDOW_X,
            norm_y * WINDOW_Y,
            window=widget,
            anchor=anchor,
        )

    def start(self):
        self.atom_spawn_loop()
        self.root.after(0, self.loop)

    def loop(self):
        delta = perf_counter() - self.prev_time
        self.tick(delta)
        self.prev_time = perf_counter()
        self.update_time()
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
        
        self.mixer.Sound('assets\\audio\sfx\sfx_placeholder.wav').play()

    def atom_spawn_loop(self):
        self.spawn_atom()
        self.root.after(2000, lambda: self.atom_spawn_loop())
    
    def register_atom(self, atom: Atom, item_id: int):
        self._atoms_by_item_id[item_id] = atom
    
    def deregister_atom(self, atom: Atom):
        item_id = {atom: item_id for item_id, atom in self._atoms_by_item_id.items()}[atom]
        del self._atoms_by_item_id[item_id]
    
    def find_overlapping_atoms(self,
        x1: float, y1: float, x2: float, y2: float, exclude: Atom | None = None
    ) -> list[Atom]:
        item_ids = self.canvas.find_overlapping(x1, y1, x2, y2)
        return [
            self._atoms_by_item_id[id]
            for id in item_ids
            if id in self._atoms_by_item_id and self._atoms_by_item_id[id] != exclude
        ]
    
    def find_atoms_in_circle(self, center: Point, radius: float,
        exclude: Atom | None = None, filter: Callable[[Atom], bool] = lambda _: True
    ) -> dict[Atom, float]:
        near_atoms: dict[Atom, float] = {
            other: distance
            for other in self.find_overlapping_atoms(   
                center.x - radius, center.y - radius,
                center.x + radius, center.y + radius,
                exclude
            )
            if (distance := (other.center - center).length()) < radius and filter(other)
        }
        return near_atoms
    
    def find_closest_atom(self, center: Point, max_dist: float,
        exclude: Atom | None = None, filter: Callable[[Atom], bool] = lambda _: True
    ) -> Atom | None:
        near_atoms = self.find_atoms_in_circle(center, max_dist, exclude, filter)
        if len(near_atoms) == 0:
            return
        return min(near_atoms, key=lambda atom: near_atoms[atom])

    def score_bond_change(self, bond: Bond, prev_order: int, new_order: int):
        change = score_bond_change(bond, prev_order, new_order)
        self.points += change
    
    def update_time(self):
        time_current = int(time())
        elapsed = time_current - self.time_started

        seconds = max(0, self.time_set - elapsed)

        if seconds <= 0:
            self.time_var.set(f"00:00")
            self.on_timer_end()
            return

        m, s = divmod(seconds, 60)

        self.time_var.set(f"{m:02d}:{s:02d}")

    def on_timer_end(self):
        if self.time_finished: return

        self.time_finished = True

        print("Timer end")
