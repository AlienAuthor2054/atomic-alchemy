from __future__ import annotations
import tkinter as tk
from tkinter.font import Font as TkFont

from constants import WINDOW_X, WINDOW_Y
from core import Game, Scene
from ui import Menu, GameOver, TestScene, Opening

GAME_TIMER = 180

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Atomic Alchemy")
        self.geometry(f"{WINDOW_X}x{WINDOW_Y}")
        self.resizable(width=False, height=False)
        self.active_scene: Scene | None = None

        self.opening = Opening(self)
        self.menu = Menu(self)

        self.bind("<<OpeningSkip>>", self.on_open_finish)
        self.bind("<<MenuStart>>", self.game_start)

        self.bind("<<EndRetry>>", self.game_start)
        self.bind("<<EndMenu>>", self.on_return)

        self.switch_scene(self.opening)
    
    def game_start(self, event) -> None:
        self.game = Game(self)
        self.end = GameOver(self, self.game)

        self.switch_scene(self.game)
        self.game.start(GAME_TIMER, self.on_game_over)

    def on_return(self, event) -> None:
        self.switch_scene(self.menu)

    def on_game_over(self) -> None:
        self.end.update_points()
        self.switch_scene(self.end)

    def on_open_finish(self, *args):
        self.switch_scene(self.menu)

    def switch_scene(self, scene: Scene) -> None:
        if self.active_scene is not None:
            self.active_scene.unload()
        scene.load()
        self.active_scene = scene

    def pressed_esc(self, event):
        if self.active_scene == self.opening:
            self.on_open_finish()
        elif self.active_scene == self.menu:
            if self.menu.options.is_open:
                self.menu.options.close()
        elif self.active_scene == self.game:
            if self.game.game_paused:
                self.game.unpause()
            else:
                self.game.pause()
        else:
            print(self.active_scene)

def main():
    root = App()
    root.bind('<Escape>', root.pressed_esc)
    root.mainloop()

if __name__ == "__main__":
    main()
