from __future__ import annotations
import tkinter as tk
from tkinter.font import Font as TkFont
from random import randrange
from typing import NamedTuple
from time import perf_counter
from dataclasses import dataclass, astuple
from random import randrange
from abc import ABC

WINDOW_X = 960
WINDOW_Y = 540

@dataclass
class Point():
    x: float
    y: float

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Point):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Point(self.x * other, self.y * other)
    
    def __truediv__(self, other: float):
        return Point(self.x / other, self.y / other)
    
    def __len__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __iter__(self):
        # Return an iterator from astuple to enable tuple unpacking
        return iter(astuple(self))

    def unit(self, mul: float = 1.0):
        return self / len(self) * mul

class Draggable(ABC):
    def __init__(self, game: Game, tag: str, pos: Point, vel: Point = Point(0, 0)):
        self.game = game
        canvas = game.canvas
        self.canvas = canvas
        self.tag = tag
        self.dragging = False
        self.pos = pos
        self.vel = vel
        self.last_mouse_pos = Point(0, 0)
        canvas.tag_bind(tag, "<ButtonPress-1>", self.on_click)
        canvas.tag_bind(tag, "<ButtonRelease-1>", self.on_release)
        canvas.tag_bind(tag, "<B1-Motion>", self.on_drag)
        game.physics_objects.add(self)
    
    def on_click(self, event):
        self.dragging = True
        self.last_mouse_pos = Point(event.x, event.y)
    
    def on_release(self, event):
        self.dragging = False
    
    def on_drag(self, event):
        if not self.dragging:
            return
        self.move_to(self.pos + Point(event.x, event.y) - self.last_mouse_pos)
        self.last_mouse_pos = Point(event.x, event.y)
    
    def move_to(self, pos):
        self.pos = pos
        self.canvas.moveto(
            self.tag, pos.x, pos.y
        )
        self.canvas.update_idletasks()

    def physics_process(self, delta):
        if self.dragging:
            return
        self.move_to(self.pos + self.vel * delta)
        x1, y1, x2, y2 = self.canvas.bbox(self.tag)
        if x1 > WINDOW_X or y1 > WINDOW_Y or x2 < 0 or y2 < 0:
            self.remove()
    
    def remove(self):
        self.game.physics_objects.remove(self)
        self.canvas.delete(self.tag)
        del self

class Atom(Draggable):
    next_id = 1

    def __init__(self, game: Game):
        self.id = Atom.next_id
        Atom.next_id += 1
        tag = "atom" + str(self.id)
        radius = 36
        pad = radius
        center = Point(-pad, randrange(pad, WINDOW_Y - pad))
        pos = Point(center.x - radius, center.y - radius)
        vel = Point(randrange(75, 200), 0)
        super().__init__(game, tag, pos, vel)
        self.canvas.create_rectangle(
            center.x - radius, center.y - radius,
            center.x + radius, center.y + radius,
            fill="black",
            tags=tag,
        )
        label_font = TkFont(size=radius)
        self.canvas.create_text(
            center.x,
            center.y,
            text="H",
            font=label_font,
            fill="gray",
            tags=tag,
            state=tk.DISABLED,
        )

class Game():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.prev_time: float = 0.0
        self.physics_objects = set()
        canvas = tk.Canvas(root, width=WINDOW_X, height=WINDOW_Y)
        canvas.pack()
        self.canvas = canvas

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
        Atom(self)
        self.root.after(2000, lambda: self.atom_spawn_loop())

def main():
    root = tk.Tk()
    root.title("Atomic Alchemy")
    root.geometry(f"{WINDOW_X}x{WINDOW_Y}")
    root.resizable(width=False, height=False)
    game = Game(root)

    DEFAULT_FONT = TkFont(size=20)

    button = tk.Button(root, text="Spawn Atom", command=lambda: Atom(game), font=DEFAULT_FONT)
    button.place(x=0, y=0)

    game.start()
    root.mainloop()
    
main()
