from __future__ import annotations
import tkinter as tk
from tkinter.font import Font as TkFont
from random import randrange
from typing import NamedTuple
from time import perf_counter
from dataclasses import dataclass, astuple
from random import randrange
from abc import ABC
import math
from collections import deque

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
    
    def is_zero(self):
        return math.isclose(self.x, 0) and math.isclose(self.y, 0)

class Draggable(ABC):
    def __init__(self, game: Game, tag: str, pos: Point, vel: Point = Point(0, 0), limit_to_window: bool = False):
        self.game = game
        canvas = game.canvas
        self.canvas = canvas
        self.tag = tag
        self.dragging = False
        self.pos = pos
        self.drag_pos = pos
        self.vel = vel
        self.limit_to_window = limit_to_window
        self.last_mouse_pos = Point(0, 0)
        canvas.tag_bind(tag, "<ButtonPress-1>", self.on_click)
        canvas.tag_bind(tag, "<ButtonRelease-1>", self.on_release)
        canvas.tag_bind(tag, "<B1-Motion>", self.on_drag)
        game.physics_objects.add(self)
    
    def on_click(self, event):
        self.dragging = True
        self.drag_pos = self.pos
        self.last_mouse_pos = Point(event.x, event.y)
    
    def on_release(self, event):
        self.dragging = False
    
    def on_drag(self, event) -> Point:
        if not self.dragging:
            return Point(0, 0)
        mouse_pos = Point(event.x, event.y)
        mouse_offset = mouse_pos - self.last_mouse_pos
        self.drag_pos += mouse_offset
        self.last_mouse_pos = mouse_pos
        offset = self.drag_pos - self.pos
        if not self.limit_to_window or self.is_on_window(offset, 50):
            self.move_to(self.drag_pos)
            return offset
        else:
            return Point(0, 0)
    
    def move_to(self, pos):
        self.pos = pos
        self.canvas.moveto(
            self.tag, pos.x, pos.y
        )
        self.canvas.update_idletasks()
    
    def move(self, offset: Point):
        self.move_to(self.pos + offset)

    def is_on_window(self, offset: Point = Point(0, 0), padding: int = 0):
        x1, y1, x2, y2 = self.canvas.bbox(self.tag)
        x1 += offset.x + padding
        x2 += offset.x - padding
        y1 += offset.y + padding
        y2 += offset.y - padding
        return x1 < WINDOW_X and y1 < WINDOW_Y and x2 > 0 and y2 > 0

    def physics_process(self, delta):
        if self.dragging:
            return
        self.move_to(self.pos + self.vel * delta)
        x1, y1, x2, y2 = self.canvas.bbox(self.tag)
        if x1 > WINDOW_X or y1 > WINDOW_Y or x2 < 0 or y2 < 0:
            self.remove()
    
    def remove(self) -> None:
        self.game.physics_objects.remove(self)
        self.canvas.delete(self.tag)
        del self

class Atom(Draggable):
    next_id = 1

    def __init__(self, game: Game, valency: int):
        self.id = Atom.next_id
        Atom.next_id += 1
        tag = "atom" + str(self.id)
        radius = 30
        pad = radius
        center = Point(-pad, randrange(pad, WINDOW_Y - pad))
        pos = Point(center.x - radius, center.y - radius)
        vel = Point(randrange(75, 200), 0)
        super().__init__(game, tag, pos, vel)
        self.molecule = Molecule({self,})
        self.bonds: dict[Atom, int] = {}
        self.valency = valency
        self.in_lab = False
        self.canvas.create_rectangle(
            center.x - radius, center.y - radius,
            center.x + radius, center.y + radius,
            fill="black",
            tags=(tag, "atom"),
        )
        label_font = TkFont(size=radius)
        self.canvas.create_text(
            center.x,
            center.y,
            text="H",
            font=label_font,
            fill="gray",
            tags=(tag, "atom"),
            state=tk.DISABLED,
        )
        self.canvas.tag_lower(tag, "lab")
    
    def on_click(self, event):
        super().on_click(event)
        self.canvas.tag_raise(self.tag)
    
    def on_release(self, event):
        super().on_release(event)
        x1, y1, x2, y2 = self.canvas.bbox("lab")
        if x1 < event.x < x2 and y1 < event.y < y2:
            if not self.in_lab:
                self.in_lab = True
                self.game.lab.contents.add(self)
                self.game.physics_objects.remove(self)
                self.canvas.addtag_withtag("lab_obj", self.tag)
                self.vel = Point(0, 0)
            self.canvas.tag_raise(self.tag, "lab")
        else:
            if self.in_lab:
                self.in_lab = False
                self.game.lab.contents.remove(self)
                self.game.physics_objects.add(self)
                self.canvas.dtag(self.tag, "lab_obj")
                self.vel = Point(100, 0)
            self.canvas.tag_lower(self.tag, "lab")
    
    @property
    def bonds_formed(self):
        return sum(self.bonds.values())
    
    @property
    def bonds_left(self):
        return self.valency - self.bonds_formed

    def is_indirectly_bonded(self, other: Atom) -> bool:
        """
        When other is directly bonded to self, result is equivalent to:
        'Does breaking this bond keep the molecule intact?'
        """
        traversed: set[Atom] = {self,}
        queue = deque([self])
        while len(queue) > 0:
            atom = queue.popleft()
            for bonded in atom.bonds:
                if bonded == other:
                    # Ignore direct bond to other
                    if not (atom == self and bonded == other):
                        return True
                if bonded in traversed:
                    continue
                traversed.add(bonded)
                queue.append(self)
        return False
    
    def add_bond(self, other: Atom, bond_order: int = 1):
        if other in self.bonds:
            new_order = self.bonds[other] + bond_order
        else:
            new_order = bond_order
        if new_order > self.bonds_left or new_order > other.bonds_left:
            raise ValueError("New bond order exceeds valency of atom(s).")
        self.bonds[other] = new_order
        other.bonds[self] = new_order

    def remove_bond(self, other: Atom, bond_order: int = 1):
        if other not in self.bonds:
            raise ValueError("No bond to remove between these atoms.")
        new_order = self.bonds[other] - bond_order
        if new_order < 0:
            raise ValueError("Bond order to remove is more than existing bond order.")
        if new_order > 0:
            self.bonds[other] = new_order
            other.bonds[self] = new_order
        else:
            del self.bonds[other]
            del other.bonds[self]
    
    def remove(self) -> None:
        for other in self.bonds:
            self.remove_bond(other, self.bonds[other])
        self.game.lab.contents.discard(self)
        super().remove()

class Molecule():
    def __init__(self, atoms: set[Atom]) -> None:
        self.atoms = atoms
    
    @staticmethod
    def constuct_graph(origin: Atom) -> set[Atom]:
        traversed: set[Atom] = {origin,}
        queue = deque([origin])
        while len(queue) > 0:
            atom = queue.popleft()
            for other in atom.bonds:
                if other in traversed:
                    continue
                traversed.add(other)
                queue.append(other)
        return traversed
    
    def merge(self, merger: Atom, merged: Atom):
        if merged.molecule == self or merger.is_indirectly_bonded(merged):
            return
        other_mol = merged.molecule
        for atom in other_mol.atoms:
            atom.molecule = self
        self.atoms.update(other_mol.atoms)
        del other_mol
    
    def split(self, splitter: Atom, split: Atom):
        if split.molecule != self or not splitter.is_indirectly_bonded(split):
            return
        staying_atoms = Molecule.constuct_graph(splitter)
        leaving_atoms = self.atoms - staying_atoms
        self.atoms = staying_atoms
        new_mol = Molecule(leaving_atoms)
        for atom in leaving_atoms:
            atom.molecule = new_mol
            
class Lab(Draggable):
    def __init__(self, game: Game):
        tag = "lab"
        super().__init__(game, tag, Point(0, 0), Point(0, 0), True)
        self.contents: set[Draggable] = set()
        self.canvas.create_rectangle(
            0, 0,
            600, 300,
            fill="gray",
            tags=tag,
        )
    
    def on_drag(self, event):
        offset = super().on_drag(event)
        if offset.is_zero():
            return offset
        for obj in self.contents:
            obj.move(offset)
        return offset

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

def main():
    root = tk.Tk()
    root.title("Atomic Alchemy")
    root.geometry(f"{WINDOW_X}x{WINDOW_Y}")
    root.resizable(width=False, height=False)
    game = Game(root)

    DEFAULT_FONT = TkFont(size=20)

    button = tk.Button(root, text="Spawn Atom", command=lambda: Atom(game, 1), font=DEFAULT_FONT)
    button.place(x=0, y=0)

    game.start()
    root.mainloop()
    
main()
