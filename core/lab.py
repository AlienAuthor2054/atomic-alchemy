from __future__ import annotations

from typing import TYPE_CHECKING
from util.point import Point

from tkinter import PhotoImage

from .draggable import Draggable
if TYPE_CHECKING:
    from .game import Game

class Lab(Draggable):
    def __init__(self, game: Game):
        tag = "lab"
        super().__init__(game, tag, Point(0, 0), True)
        self.contents: set[Draggable] = set()

        self.texture = PhotoImage(file = f"assets\\textures\\texture_Tray.png")

        self.canvas.create_image(480, 270, image=self.texture, tags=tag)
        """
            self.canvas.create_rectangle(
            0, 0,
            600, 300,
            fill="gray",
            tags=tag,
            )
        """
    
    def on_drag(self, event):
        offset = super().on_drag(event)
        if offset.is_zero():
            return offset
        for obj in self.contents:
            obj.move(offset)
        return offset
    