from __future__ import annotations
import tkinter as tk
from tkinter.font import Font as TkFont

from constants import WINDOW_X, WINDOW_Y
from core import Atom, Game

def main():
    root = tk.Tk()
    root.title("Atomic Alchemy")
    root.geometry(f"{WINDOW_X}x{WINDOW_Y}")
    root.resizable(width=False, height=False)
    game = Game(root)

    DEFAULT_FONT = TkFont(size=20)

    button = tk.Button(root, text="Spawn Atom", command=lambda: Atom(game, 1), font=DEFAULT_FONT)
    button.place(x=0, y=0)

    game.start()
    root.mainloop()

if __name__ == "__main__":
    main()
