from __future__ import annotations

from abc import ABC

from typing import TYPE_CHECKING

from constants import WINDOW_X, WINDOW_Y
from util.point import Point

if TYPE_CHECKING:
    from .game import Game

class Draggable(ABC):
    def __init__(self, game: Game, tag: str, pos: Point, limit_to_window: bool = False):
        self.game = game
        canvas = game.canvas
        self.canvas = canvas
        self.tag = tag
        self.dragging = False
        self.pos = pos
        self.drag_pos = pos
        self.limit_to_window = limit_to_window
        self.outside_window = False
        self.last_mouse_pos = Point(0, 0)
        canvas.tag_bind(tag, "<ButtonPress-1>", self.on_click)
        canvas.tag_bind(tag, "<ButtonRelease-1>", self.on_release)
        canvas.tag_bind(tag, "<B1-Motion>", self.on_drag)
        game.physics_objects.add(self)
    
    def on_click(self, event):
        if self.game.game_paused:
            return

        self.dragging = True
        self.drag_pos = self.pos
        self.last_mouse_pos = Point(event.x, event.y)
    
    def on_release(self, event):
        self.dragging = False
    
    def on_drag(self, event) -> Point:
        if self.game.game_paused or not self.dragging:
            return Point(0, 0)
        
        mouse_pos = Point(event.x, event.y)
        mouse_offset = mouse_pos - self.last_mouse_pos
        self.drag_pos += mouse_offset
        self.last_mouse_pos = mouse_pos
        offset = self.drag_pos - self.pos
        if not self.limit_to_window or self.is_on_window(offset, 50):
            self.drag(offset)
            return offset
        else:
            return Point(0, 0)
    
    def drag(self, offset: Point):
        """
        Allows overriding dragging behavior while still encapsulating offset calculation.
        """
        self.move(offset)

    def move_to(self, pos):
        self.pos = pos
        self.canvas.moveto(
            self.tag, pos.x, pos.y
        )
    
    def move(self, offset: Point):
        self.move_to(self.pos + offset)

    def is_on_window(self, offset: Point = Point(0, 0), padding: int = 0):
        x1, y1, x2, y2 = self.canvas.bbox(self.tag)
        x1 += offset.x + padding
        x2 += offset.x - padding
        y1 += offset.y + padding
        y2 += offset.y - padding
        return x1 < WINDOW_X and y1 < WINDOW_Y and x2 > 0 and y2 > 0

    def physics_process(self, delta):
        if self.dragging:
            return
        bbox = self.canvas.bbox(self.tag)
        if bbox is None:
            return
        x1, y1, x2, y2 = bbox
        if x1 > WINDOW_X or y1 > WINDOW_Y or x2 < 0 or y2 < 0:
            was_inside_window = not self.outside_window
            self.outside_window = True
            if was_inside_window:
                self.on_exit_window()
        else:
            self.outside_window = False
    
    def on_exit_window(self) -> None:
        self.remove()

    def remove(self) -> None:
        self.game.physics_objects.remove(self)
        self.canvas.delete(self.tag)
        del self
