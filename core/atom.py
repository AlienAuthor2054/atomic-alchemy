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
    from .element import Element
    from .game import Game

class Atom(Draggable):
    next_id = 1

    def __init__(self, game: Game, element: Element):
        self.id = Atom.next_id
        Atom.next_id += 1
        tag = "atom" + str(self.id)
        radius = 30
        self.radius = radius
        pad = radius
        center = Point(-pad, randrange(pad, WINDOW_Y - pad))
        pos = Point(center.x - radius, center.y - radius)
        vel = Point(randrange(75, 200), 0)
        super().__init__(game, tag, pos, vel)
        self.molecule = Molecule({self,})
        self.bonds: dict[Atom, Bond] = {}
        self.valency = element.valency
        item_id = self.canvas.create_rectangle(
            center.x - radius, center.y - radius,
            center.x + radius, center.y + radius,
            fill=element.color,
            tags=(tag, "atom"),
        )
        label_font = TkFont(size=radius)
        self.canvas.create_text(
            center.x,
            center.y,
            text=element.symbol,
            font=label_font,
            fill=element.text_color,
            tags=(tag, "atom"),
            state=tk.DISABLED,
        )
        self.canvas.tag_lower(tag, "lab")
        self.game.register_atom(self, item_id)
    
    def physics_process(self, delta):
        if self.molecule.in_lab or self.molecule.dragging:
            return
        super().physics_process(delta)

    def on_click(self, event):
        super().on_click(event)
        self.molecule.dragging = True
        self.canvas.tag_raise(self.tag)
    
    def attempt_bond(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.tag)
        bbox_expand = Bond.LENGTH - self.radius
        near_atoms = [
            atom
            for atom in self.game.find_overlapping_atoms(   
                x1 - bbox_expand, y1 - bbox_expand,
                x2 + bbox_expand, y2 + bbox_expand,
                self
            )
            if atom.molecule.in_lab and atom not in self.bonds
        ]
        if len(near_atoms) == 0:
            return
        other = near_atoms[0]
        try:
            self.add_bond(other, 1)
        except ValueError:
            pass
        else:
            # Reposition dragged atom on sucessful bond to maintain constant bond length
            # Measures Chebyshev (chessboard) distance since atoms are squares
            offset = self.center - other.center
            if offset.is_zero():
                offset = Point(1, 0)
            offset *= (Bond.LENGTH / max(abs(offset.x), abs(offset.y)))
            self.center = other.center + offset
    
    def drag(self, offset: Point):
        self.molecule.drag(offset)

    def on_mol_drag(self, offset: Point):
        self.move(offset)

    def on_mol_release_in_lab(self, was_outside_lab: bool):
        if was_outside_lab:
            self.game.lab.contents.add(self)
            self.game.physics_objects.remove(self)
            self.canvas.addtag_withtag("lab_obj", self.tag)
            self.vel = Point(0, 0)
        self.canvas.tag_raise(self.tag, "lab")
        self.attempt_bond()
        self.on_mol_release()
    
    def on_mol_release_outside_lab(self, was_inside_lab: bool):
        if was_inside_lab:
            self.game.lab.contents.remove(self)
            self.game.physics_objects.add(self)
            self.canvas.dtag(self.tag, "lab_obj")
            self.vel = Point(100, 0)
        self.canvas.tag_lower(self.tag, "lab")
        self.on_mol_release()

    def on_mol_release(self):
        for bond in self.bonds.values():
            bond.update_layering()
        if len(self.canvas.find_withtag("bond")) > 0:
            self.canvas.tag_raise(self.tag, "bond")
    
    def on_release(self, event):
        super().on_release(event)
        self.molecule.dragging = False
        x1, y1, x2, y2 = self.canvas.bbox("lab")
        if x1 < event.x < x2 and y1 < event.y < y2:
            self.molecule.on_release_in_lab()
        else:
            self.molecule.on_release_outside_lab()

    def on_exit_window(self) -> None:
        self.molecule.on_atom_exit_window()

    def move_to(self, pos) -> None:
        super().move_to(pos)
        for bond in self.bonds.values():
            bond.update_display()

    @property
    def center(self) -> Point:
        return Point(self.pos.x + self.radius, self.pos.y + self.radius)

    @center.setter
    def center(self, new: Point) -> None:
        self.move_to(Point(
            new.x - self.radius,
            new.y - self.radius
        ))

    @property
    def bond_orders(self) -> dict[Atom, int]:
        return {atom: bond.order for atom, bond in self.bonds.items()}

    @property
    def bonds_formed(self):
        return sum(self.bond_orders.values())
    
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
            new_order = self.bonds[other].order + bond_order
        else:
            new_order = bond_order
        if new_order > self.bonds_left or new_order > other.bonds_left:
            raise ValueError("New bond order exceeds valency of atom(s).")
        if other in self.bonds:
            self.bonds[other].order = new_order
        else:
            bond = Bond(self, other, new_order)
            self.bonds[other] = bond
            other.bonds[self] = bond
            self.molecule.merge(self, other)

    def remove_bond(self, other: Atom, bond_order: int = 1):
        if other not in self.bonds:
            raise ValueError("No bond to remove between these atoms.")
        new_order = self.bonds[other].order - bond_order
        if new_order < 0:
            raise ValueError("Bond order to remove is more than existing bond order.")
        if new_order > 0:
            self.bonds[other].order = new_order
        else:
            self.bonds[other].remove()
            del self.bonds[other]
            del other.bonds[self]
            self.molecule.split(self, other)
    
    def remove(self) -> None:
        for other in self.bonds.copy():
            self.remove_bond(other, self.bonds[other].order)
        self.game.lab.contents.discard(self)
        self.game.deregister_atom(self)
        self.molecule.remove_atom(self)
        super().remove()

class Bond():
    LENGTH = 75
    next_id = 1

    def __init__(self, atom1: Atom, atom2: Atom, bond_order: int) -> None:
        self.id = Bond.next_id
        Bond.next_id += 1
        self.tag = "bond" + str(self.id)
        self.canvas = atom1.canvas
        self.atom1 = atom1
        self.atom2 = atom2
        self.order = bond_order
        self.canvas.create_line(
            *atom1.center, *atom2.center, 
            fill="black",
            width=10,
            tags=(self.tag, "bond"),
        )
        self.update_layering()
    
    def update_layering(self) -> None:
        self.canvas.tag_lower(self.tag, "atom")
        self.canvas.tag_raise(self.tag, "lab")

    def update_display(self) -> None:
        self.canvas.coords(self.tag, *self.atom1.center, *self.atom2.center)
        self.update_layering()
    
    def remove(self) -> None:
        self.canvas.delete(self.tag)
        del self
