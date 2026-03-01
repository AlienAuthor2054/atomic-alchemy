from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Element():
    number: int
    symbol: str
    name: str
    valency: int
    color: str
    text_color: str

ELEMENT_LIST = [
    Element(number=1, symbol="H", name="Hydrogen", valency=1, color="#FFFFFF", text_color="#000000"),
    Element(number=6, symbol="C", name="Carbon",   valency=4, color="#222222", text_color="#FFFFFF"),
    Element(number=7, symbol="N", name="Nitrogen", valency=3, color="#0000FF", text_color="#FFFFFF"),
    Element(number=8, symbol="O", name="Oxygen",   valency=2, color="#FF0000", text_color="#FFFFFF"),
]

ELEMENTS_BY_NUM: dict[int, Element] = {
    element.number: element for element in ELEMENT_LIST
}
