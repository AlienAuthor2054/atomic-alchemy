from __future__ import annotations

import tkinter as tk
from time import perf_counter, time
from typing import TYPE_CHECKING, Callable, Literal
from random import choices

from constants import WINDOW_X, WINDOW_Y, ATOM_SPAWN_WEIGHTS
from core.element import ELEMENTS_BY_NUM
from util.point import Point

from ui import GameDisplay, Options
from style import *
from .scene import Scene
from .atom import Atom
from .lab import Lab
from .scoring import score_bond_change
from .db import Database
from .audio import AudioManager

if TYPE_CHECKING:
    from .bond import Bond

class Game(Scene):
    CONVEYOR_Y = 95
    SPAWN_Y = 130
    LAB_Y = 165
    BG_COLOR = "#FFF6E7"

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root, Game.BG_COLOR)
        self.prev_time: float = 0.0
        self.physics_objects = set()
        self._atoms_by_item_id: dict[int, Atom] = {} # For atom collision detection
        self.lab = Lab(self)
        self._points = 0
        self.points_var = tk.IntVar()

        self.options = Options(self)

        self.game_started = False
        self.game_paused = False

        self.loop_game = None
        self.loop_atom = None

        self.time_var = tk.StringVar()
        self.time_started = int(time())
        self._time_finished = False
        self.time_set = 180

        self.on_end = None

        self.init_ui()

    @property
    def points(self) -> int:
        return self._points
    
    @points.setter
    def points(self, new: int) -> None:
        self._points = new
        self.points_var.set(new)

    @property
    def time_finished(self):
        return self._time_finished
    
    @time_finished.setter
    def time_finished(self, value: bool):
        if value != self._time_finished:
            self.on_timer_end()
        
        self._time_finished = value

    def init_ui(self):
        points_frame = GameDisplay(self.canvas, self.points_var,
            "assets\\textures\\texture_Points.png", 0, 0.02, 'nw'
        )
        timer_frame = GameDisplay(self.canvas, self.time_var,
            "assets\\textures\\texture_Timer.png", 1, 0.02, 'ne'
        )

        conveyor_id = self.canvas.create_rectangle(
            0, Game.CONVEYOR_Y, WINDOW_X, Game.LAB_Y,
            fill=BG_COLOR_2,
            outline="",
        )
        self.canvas.lower(conveyor_id)

    def start(self, timer: int = 180, on_end: Callable[[], None] | None = None):
        self.game_started = True

        self.prev_time = perf_counter()
        self.time_started = int(time())
        self.time_set = timer
        self.on_end = on_end
        
        self.canvas.pack(fill='both')

        self.atom_spawn_loop()

        AudioManager.play_dynamic_bgm("assets/audio/song/song_game.ogg", "assets/audio/song/song_end.ogg")

        self.root.after(0, self.loop)

    def stop(self):
        self.game_started = False

        AudioManager.set_active_dynamic_track(2)

        if self.loop_game:
            self.root.after_cancel(self.loop_game)
            self.loop_game = None

        if self.loop_atom:
            self.root.after_cancel(self.loop_atom)
            self.loop_atom = None

    def pause(self):
        self.game_paused = True

        self.time_paused_at = int(time())

        AudioManager.pause_bgm()
        AudioManager.play_sfx("game_pause")

        if self.loop_game:
            self.root.after_cancel(self.loop_game)
            self.loop_game = None

        if self.loop_atom:
            self.root.after_cancel(self.loop_atom)
            self.loop_atom = None

    def unpause(self):
        self.game_paused = False

        time_spent_paused = int(time()) - self.time_paused_at
        self.time_started += time_spent_paused
        
        AudioManager.unpause_bgm()
        AudioManager.play_sfx("game_unpause")

        self.prev_time = perf_counter()
        
        self.loop_atom = self.root.after(2000, self.atom_spawn_loop)
        self.loop_game = self.root.after(0, self.loop)

    def loop(self):
        if self.game_started and not self.game_paused:
            delta = perf_counter() - self.prev_time
            self.tick(delta)
            self.prev_time = perf_counter()
            self.update_time()
            self.loop_game = self.root.after(8, lambda: self.loop())

    def unload(self):
        self.stop()
        
        self.physics_objects.clear()
        self._atoms_by_item_id.clear()
        
        if self.canvas:
            self.canvas.destroy()
    
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
        if self.game_started and not self.game_paused:
            self.spawn_atom()
            self.loop_atom = self.root.after(2000, lambda: self.atom_spawn_loop())
    
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
            self.time_finished = True
            return

        m, s = divmod(seconds, 60)

        self.time_var.set(f"{m:02d}:{s:02d}")

    def on_timer_end(self):
        self.stop()
        
        if self.on_end:
            self.on_end()
