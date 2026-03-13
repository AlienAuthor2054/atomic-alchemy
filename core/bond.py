from __future__ import annotations

from typing import TYPE_CHECKING

from util.point import Point
from constants import BOND_LENGTH

from .scoring import score_bond
if TYPE_CHECKING:
    from .atom import Atom

class Bond():
    LENGTH = BOND_LENGTH
    LINE_SEPERATION = 20
    LINE_OFFSETS = [
        [0.0],
        [-0.5, 0.5], 
        [-1.0, 0.0, 1.0],
    ]
    BASE_LINE_WIDTH = 15
    HITBOX_WIDTH = (
        (LINE_OFFSETS[-1][-1] - LINE_OFFSETS[-1][0]) * LINE_SEPERATION + BASE_LINE_WIDTH
    )
    HITBOX_ATOM_OVERLAP = 0.15
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
        self._order = bond_order
        game = atom1.game
        game.score_bond_change(self, 0, bond_order)
        self.game = game
        self.points = score_bond(self)
        self.lines: list[int | None] = [None, None, None]
        self.hitbox_id = self.canvas.create_line(
            0, 0, 0, 0, # update these on update_hitbox()
            fill="",
            width=Bond.HITBOX_WIDTH,
            tags=(self.tag, "bond_hitbox", "bond"),
        )
        self.update_lines()
        self.update_display()
        canvas.tag_bind(tag, "<ButtonPress-1>", self.on_left_click)
        canvas.tag_bind(tag, "<ButtonPress-3>", self.on_right_click)
    
    @property
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, new: int) -> None:
        self.game.score_bond_change(self, self._order, new)
        self._order = new
        self.points = score_bond(self)
        self.update_lines()

    def on_left_click(self, event) -> None:
        if not self.atom1.molecule.in_lab:
            print("Cannot form bonds outside of the lab!")
            return
        try:
            self.atom1.add_bond(self.atom2, 1)
        except ValueError as e:
            print(e)

    def on_right_click(self, event) -> None:
        if not self.atom1.molecule.in_lab:
            print("Cannot break bonds outside of the lab!")
            return
        self.atom1.remove_bond(self.atom2, 1)

    def update_layering(self) -> None:
        self.canvas.tag_lower(self.tag, "atom")
        self.canvas.tag_raise(self.tag, "lab")
        self.canvas.tag_raise(self.hitbox_id, "atom")

    def update_lines(self) -> None:
        line_width = self.points * Bond.BASE_LINE_WIDTH / 10 / self.order
        for i in range(len(self.lines)):
            line_id = self.lines[i]
            if line_id is None:
                if i >= self.order:
                    continue
                line_id = self.canvas.create_line(
                    *self.atom1.center, *self.atom2.center, 
                    fill="black",
                    tags=(self.tag, "bond"),
                )
                self.lines[i] = line_id
            self.canvas.itemconfigure(
                line_id,
                state="normal" if i < self.order else "hidden",
                width=line_width
            )
        self.update_display()

    def update_hitbox(self) -> None:
        atom_diff = self.atom2.center - self.atom1.center
        if atom_diff.is_zero():
            atom_diff = Point(1, 0)
        self.hitbox_inset = atom_diff.unit(
            (((2 - Bond.HITBOX_ATOM_OVERLAP) * (self.atom1.radius + self.atom2.radius))
            - Bond.LENGTH) / 2
        )
        self.canvas.coords(self.hitbox_id,
            *(self.atom1.center + self.hitbox_inset), *(self.atom2.center - self.hitbox_inset)
        )

    def update_display(self) -> None:
        atom_diff = self.atom2.center - self.atom1.center
        if atom_diff.is_zero():
            atom_diff = Point(1, 0)
        offset_unit = Point(atom_diff.y, atom_diff.x).unit(Bond.LINE_SEPERATION)
        line_offsets = Bond.LINE_OFFSETS[self.order - 1]
        for i in range(self.order):
            line_id = self.lines[i]
            if line_id is None:
                break
            offset = offset_unit * line_offsets[i]
            self.canvas.coords(line_id,
                *(self.atom1.center + offset), *(self.atom2.center + offset)
            )
        self.update_hitbox()
        self.update_layering()
    
    def remove(self, is_scored: bool = True) -> None:
        if is_scored:
            self.game.score_bond_change(self, self.order, 0)
        self.canvas.delete(self.tag)
        del self