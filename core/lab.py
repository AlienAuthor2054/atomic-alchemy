from __future__ import annotations

from typing import TYPE_CHECKING
from util.point import Point

from constants import WINDOW_X, WINDOW_Y
if TYPE_CHECKING:
    from .draggable import Draggable
    from .game import Game

class Lab():
    def __init__(self, game: Game):
        tag = "lab"
        self.contents: set[Draggable] = set()

        game.canvas.create_rectangle(
            0, game.LAB_Y, WINDOW_X, WINDOW_Y,
            tags=tag,
            fill="",
            outline="",
        )
