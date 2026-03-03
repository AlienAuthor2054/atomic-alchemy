from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING
from random import randrange

from util.point import Point

if TYPE_CHECKING:
    from .atom import Atom
    from .game import Game

class Molecule():
    def __init__(self, game: Game, atoms: set[Atom]) -> None:
        self.game = game
        self.atoms = atoms
        self.dragging = False
        self.in_lab = False
        self.vel = Point(randrange(75, 200), 0)
        game.physics_objects.add(self)
    
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
        other_mol.remove()
    
    def split(self, splitter: Atom, split: Atom):
        if split.molecule != self or splitter.is_indirectly_bonded(split):
            return
        staying_atoms = Molecule.constuct_graph(splitter)
        leaving_atoms = self.atoms - staying_atoms
        self.atoms = staying_atoms
        new_mol = Molecule(self.game, leaving_atoms)
        new_mol.in_lab = True
        for atom in leaving_atoms:
            atom.molecule = new_mol
    
    def move(self, offset: Point):
        for atom in self.atoms:
            atom.move(offset)
    
    def physics_process(self, delta: float):
        if self.in_lab or self.dragging or self.vel.is_zero():
            return
        self.move(self.vel * delta)

    def on_release_in_lab(self):
        self.vel = Point(0, 0)
        was_outside_lab = not self.in_lab
        self.in_lab = True
        for atom in self.atoms.copy():
            atom.on_mol_release_in_lab(was_outside_lab)
    
    def on_release_outside_lab(self):
        self.vel = Point(100, 0)
        was_inside_lab = self.in_lab
        self.in_lab = False
        for atom in self.atoms:
            atom.on_mol_release_outside_lab(was_inside_lab)
        
    def on_atom_exit_window(self):
        for atom in self.atoms:
            if not atom.outside_window:
                return
        for atom in self.atoms.copy():
            atom.remove()

    def remove_atom(self, atom: Atom):
        self.atoms.remove(atom)
        if len(self.atoms) == 0:
            self.remove()
    
    def remove(self) -> None:
        self.game.physics_objects.remove(self)
        del self
