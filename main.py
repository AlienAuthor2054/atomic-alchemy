from __future__ import annotations
import tkinter as tk
from tkinter.font import Font as TkFont

from constants import WINDOW_X, WINDOW_Y
from core import Game, Menu, Scene
from ui import PointsFrame, GameTimer

def main():
    root = tk.Tk()
    root.title("Atomic Alchemy")
    root.geometry(f"{WINDOW_X}x{WINDOW_Y}")
    root.resizable(width=False, height=False)

    menu = Menu(root)

    def game_start(event):
        menu.unload()

        game = Game(root)
        game.load()

        spawn_button = tk.Button(game.canvas, text="Spawn Atom", command=game.spawn_atom)
        game.add_widget(spawn_button, 0, 0, 'nw')

        points_frame = PointsFrame(game)
        game.add_widget(points_frame, 0.5, 1, 's')

        timer = GameTimer(game, 1, 0.05, 'ne')

        game.start(3, lambda:game_end(game))

    def game_end(game: Game):
        game.unload()
        menu.load()

    menu.load()

    root.bind("<<MenuStart>>", game_start)
    root.mainloop()

if __name__ == "__main__":
    main()
