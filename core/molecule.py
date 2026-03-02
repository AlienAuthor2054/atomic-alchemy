from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from util.point import Point

if TYPE_CHECKING:
    from .atom import Atom

class Molecule():
    def __init__(self, atoms: set[Atom]) -> None:
        self.atoms = atoms
        self.dragging = False
        self.in_lab = False
    
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
    
    def move(self, offset: Point):
        for atom in self.atoms:
            atom.move(offset)

    def on_release_in_lab(self):
        was_outside_lab = not self.in_lab
        self.in_lab = True
        for atom in self.atoms.copy():
            atom.on_mol_release_in_lab(was_outside_lab)
    
    def on_release_outside_lab(self):
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
            del self
