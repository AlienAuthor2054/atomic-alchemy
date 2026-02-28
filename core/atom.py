from __future__ import annotations

import tkinter as tk
from collections import deque
from tkinter.font import Font as TkFont
from typing import TYPE_CHECKING
from random import randrange

from util.point import Point
from constants import WINDOW_Y

from .draggable import Draggable
from .molecule import Molecule
if TYPE_CHECKING:
    from .game import Game

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
