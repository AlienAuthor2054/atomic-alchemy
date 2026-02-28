from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .atom import Atom

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
