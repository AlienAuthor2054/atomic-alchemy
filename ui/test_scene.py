from core.scene import Scene
from core.db import Database

from constants import WINDOW_X, WINDOW_Y
from style import *

import tkinter as tk
from tkinter.font import Font

class TestScene(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)