from __future__ import annotations
import tkinter as tk
from tkinter.font import Font as TkFont

from constants import WINDOW_X, WINDOW_Y
from core import Game, Scene
from ui import Menu

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Atomic Alchemy")
        self.geometry(f"{WINDOW_X}x{WINDOW_Y}")
        self.resizable(width=False, height=False)
        self.active_scene: Scene | None = None

        self.menu = Menu(self)
        self.game = Game(self)
        self.switch_scene(self.menu)
        self.bind("<<MenuStart>>", self.on_start_btn_pressed)
    
    def on_start_btn_pressed(self, event) -> None:
        self.switch_scene(self.game)
        self.game.start(180, self.on_game_over)
    
    def on_game_over(self) -> None:
        # switch to game over scene here
        pass

    def switch_scene(self, scene: Scene) -> None:
        if self.active_scene is not None:
            self.active_scene.unload()
        scene.load()
        self.active_scene = scene

    def esc_pressed(self, event):
        if self.active_scene == self.menu:
            print("Menu")
        elif self.active_scene == self.game:
            if self.game.game_paused:
                self.game.unpause()
            else:
                self.game.pause()
        else:
            print(self.active_scene)

def main():
    root = App()
    root.bind('<Escape>', root.esc_pressed)
    root.mainloop()

if __name__ == "__main__":
    main()
