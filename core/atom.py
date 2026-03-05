from __future__ import annotations

import tkinter as tk
from collections import deque
from tkinter.font import Font as TkFont
from typing import TYPE_CHECKING
from random import randrange

from util.point import Point
from constants import WINDOW_Y, BOND_LENGTH

from .draggable import Draggable
from .molecule import Molecule
if TYPE_CHECKING:
    from .element import Element
    from .game import Game

class Atom(Draggable):
    MAX_BONDING_DIST = 100
    BONDING_SITES = {
        "right": Point(BOND_LENGTH, 0),
        "down": Point(0, BOND_LENGTH),
        "left": Point(-BOND_LENGTH, 0),
        "up": Point(0, -BOND_LENGTH),
    }
    BONDING_SITE_CONVERSION = {
        "right": "left",
        "down": "up",
        "left": "right",
        "up": "down",
    }

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
        super().__init__(game, tag, pos)
        self.molecule = Molecule(game, {self,})
        self.bonds: dict[Atom, Bond] = {}
        self.bonding_sites: dict[str, Atom | None] = dict.fromkeys(Atom.BONDING_SITES)
        self.valency = element.valency
        item_id = self.canvas.create_oval(
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
    
    def get_clear_bonding_sites(self, other: Atom, prev_atoms: set[Atom]) -> dict[str, Point]:
        """
        Returns available bonding sites on the `other` atom.

        Also accounts for atom collisions on bonding.
        """
        bonding_sites: dict[str, Point] = {
            site: other.center + Atom.BONDING_SITES[site]
            for site in other.bonding_sites
            if other.bonding_sites[site] is None
            and self.bonding_sites[Atom.BONDING_SITE_CONVERSION[site]] is None
        }
        for site in bonding_sites.copy():
            offset = bonding_sites[site] - self.center
            other_atoms = other.molecule.atoms - prev_atoms
            for atom in prev_atoms:
                if self.game.find_closest_atom(
                    atom.center + offset, self.radius, None,
                    lambda atom: atom in other_atoms
                ) is None:
                    continue
                del bonding_sites[site]
                break
        return bonding_sites

    def snap_to_bonding_site(self, other: Atom, prev_atoms: set[Atom],
        bonding_sites: dict[str, Point] | None = None
    ) -> None:
        """
        Used to reposition dragged atom on sucessful bond
        to the nearest available bonding site of the `other` atom.
        
        `prev_atoms` is used to drag along previously bonded atoms.\n
        `bonding_sites` assumes sites are clear, like from `Atom.get_clear_bonding_sites`
        """
        if bonding_sites is None:
            bonding_sites = self.get_clear_bonding_sites(other, prev_atoms)
        if len(bonding_sites) == 0:
            return
        bonding_site = min(bonding_sites, key=lambda site:
            (self.center - bonding_sites[site]).length()
        )
        other.bonding_sites[bonding_site] = self
        self.bonding_sites[Atom.BONDING_SITE_CONVERSION[bonding_site]] = other
        bonding_pos = other.center + Atom.BONDING_SITES[bonding_site]
        offset = bonding_pos - self.center
        for atom in prev_atoms:
            atom.move(offset)
    
    def clear_bonding_site(self, other: Atom):
        site = next((
            site for site, atom 
            in self.bonding_sites.items()
            if atom is other)
        )
        self.bonding_sites[site] = None
        other.bonding_sites[Atom.BONDING_SITE_CONVERSION[site]] = None

    def attempt_bond(self):
        other = self.game.find_closest_atom(self.center, Atom.MAX_BONDING_DIST, self,
            lambda other: other.molecule.in_lab and other.molecule != self.molecule
        )
        if other is None:
            return
        prev_atoms = self.molecule.atoms.copy()
        bonding_sites = self.get_clear_bonding_sites(other, prev_atoms)
        if len(bonding_sites) == 0:
            print("Unavoidable atom collision within merged molecule on bond formation!")
            return
        try:
            self.add_bond(other, 1)
        except ValueError:
            pass
        else:
            self.snap_to_bonding_site(other, prev_atoms, bonding_sites)
    
    def drag(self, offset: Point):
        self.molecule.move(offset)

    def on_mol_drag(self, offset: Point):
        self.move(offset)

    def on_mol_release_in_lab(self, was_outside_lab: bool):
        if was_outside_lab:
            self.game.lab.contents.add(self)
            self.game.physics_objects.remove(self)
            self.canvas.addtag_withtag("lab_obj", self.tag)
        self.canvas.tag_raise(self.tag, "lab")
        self.on_mol_release()
    
    def on_mol_release_outside_lab(self, was_inside_lab: bool):
        if was_inside_lab:
            self.game.lab.contents.remove(self)
            self.game.physics_objects.add(self)
            self.canvas.dtag(self.tag, "lab_obj")
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
            self.attempt_bond()
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
        if bond_order > self.bonds_left or bond_order > other.bonds_left:
            raise ValueError("New bond order exceeds valency of atom(s).")
        if other in self.bonds:
            new_order = self.bonds[other].order + bond_order
        else:
            new_order = bond_order
        if new_order > 3:
            raise ValueError("New bond order exceeds maximum of 3.")
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
            self.clear_bonding_site(other)
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
    LENGTH = BOND_LENGTH
    next_id = 1

    def __init__(self, atom1: Atom, atom2: Atom, bond_order: int) -> None:
        self.id = Bond.next_id
        Bond.next_id += 1
        tag = "bond" + str(self.id)
        self.tag = tag
        canvas = atom1.canvas
        self.canvas = canvas
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
        canvas.tag_bind(tag, "<ButtonPress-3>", self.on_right_click)
    
    def on_right_click(self, event) -> None:
        self.atom1.remove_bond(self.atom2, 1)

    def update_layering(self) -> None:
        self.canvas.tag_lower(self.tag, "atom")
        self.canvas.tag_raise(self.tag, "lab")

    def update_display(self) -> None:
        self.canvas.coords(self.tag, *self.atom1.center, *self.atom2.center)
        self.update_layering()
    
    def remove(self) -> None:
        self.canvas.delete(self.tag)
        del self
