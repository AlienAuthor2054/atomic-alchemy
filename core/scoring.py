from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bond import Bond

def _get_score_list(symbol_list: list[str]) -> list[int]:
    score_list = BOND_SCORES.get(''.join(symbol_list))
    if score_list is None:
        symbol_list.reverse()
        score_list = BOND_SCORES[''.join(symbol_list)]
    return score_list

def score_bond(bond: Bond) -> int:
    symbol_list = [bond.atom1.element.symbol, bond.atom2.element.symbol]
    return _get_score_list(symbol_list)[bond.order-1]

def score_bond_change(bond: Bond, prev_order: int, new_order: int) -> int:
    symbol_list = [bond.atom1.element.symbol, bond.atom2.element.symbol]
    score_list = _get_score_list(symbol_list)
    prev_energy = score_list[prev_order-1] if prev_order > 0 else 0
    new_energy = score_list[new_order-1] if new_order > 0 else 0
    return new_energy - prev_energy

BOND_SCORES: dict[str, list[int]] = {
    'CC': [10, 17, 24],
    'CH': [12],
    'CN': [9, 18, 26],
    'CO': [10, 23],
    'HH': [12],
    'HN': [11],
    'HO': [13],
    'NN': [5, 12, 27],
    'NO': [6, 18],
    'OO': [4, 14],
}
