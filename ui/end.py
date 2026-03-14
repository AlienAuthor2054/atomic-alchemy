from __future__ import annotations
from typing import TYPE_CHECKING

from constants import WINDOW_X, WINDOW_Y
from core.scene import Scene

import tkinter as tk
from tkinter.font import Font

if TYPE_CHECKING:
    from core.game import Game

class GameOver(Scene):
    def __init__(self, root, game: Game):
        super().__init__(root)

        self.game = game

        font_title = Font(family="Courier", size=70, weight="bold")
        font_points = Font(family="Courier", size=24, weight="bold")
        font_normal = Font(family="Courier", size=10, weight="bold")
        font_button_large = Font(family="Courier", size=16, weight="bold")

        BG_COLOR = "#FDF6E3"     
        TEXT_COLOR = "#333333"    
        TITLE_COLOR = "#FA5C5C"    
        POINTS_COLOR = "#909B4E"   
        self.btn_BG = "#3A8686"       
        self.btn_FG = "white"          
        self.btn_ACTIVE_BG = "#2B6666"

        self.frame_root = tk.Frame(self.canvas, width=WINDOW_X, height=WINDOW_Y)
        self.frame_root.config(
            bg=BG_COLOR,
        )
        self.frame_root.pack_propagate(False) 

        self.frame_end = tk.Frame(self.frame_root)
        self.frame_end.config(
            bg=BG_COLOR,
        )
        self.frame_end.pack(expand=True)

        ## GAME OVER
        self.label_end_tltle = tk.Label(self.frame_end)
        self.label_end_tltle.config(
            text="GAME OVER",
            font=font_title,
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        self.label_end_tltle.pack()

        ## POINTS
        self.label_points = tk.Label(self.frame_end)
        self.label_points.config(
            text="0 POINTS",
            font=font_points,
            bg=BG_COLOR,
            fg=POINTS_COLOR,
        )
        self.label_points.pack(pady=(0, 20))

        ## BUTTONS
        self.frame_buttons = tk.Frame(self.frame_end)
        self.frame_buttons.pack()

        ## BUTTONS LEFT
        self.frame_left = tk.Frame(self.frame_buttons, width=288, height=100)
        self.frame_left.pack_propagate(False)
        self.frame_left.config(
            bg=BG_COLOR,
        )
        self.frame_left.pack(side=tk.LEFT)

        self.label_end_submit = tk.Label(self.frame_left)
        self.label_end_submit.config(
            text="ENTER YOUR NAME\nAND SUBMIT YOUR SCORE\nTO THE LEADERBOARD",
            font=font_normal,
            bg=BG_COLOR
        )
        self.label_end_submit.pack()

        self.entry_name = tk.Entry(self.frame_left)
        self.entry_name.config(
            font=font_normal, 
            justify="center", 
            width=18, fg="#333333", 
            bg="white", 
            insertbackground="black"
        )
        self.entry_name.pack()

        self.button_end_submit = tk.Button(self.frame_left)
        self.button_end_submit.config(
            text="SUBMIT",
            font=font_normal,
            width=8,
            bg=self.btn_BG,
            fg=self.btn_FG,
            activebackground=self.btn_ACTIVE_BG, 
            activeforeground="white", 
            relief="flat"
        )
        self.button_end_submit.pack()

        ## BUTTONS MIDDLE
        self.frame_middle = tk.Frame(self.frame_buttons, width=288, height=100)
        self.frame_middle.pack_propagate(False)
        self.frame_middle.config(
            bg=BG_COLOR,
        )
        self.frame_middle.pack(side=tk.LEFT)

        self.button_end_retry = tk.Button(self.frame_middle)
        self.button_end_retry.config(
            text="RETRY",
            font=font_button_large,
            width=15,
            bg=self.btn_BG,
            fg=self.btn_FG,
            activebackground=self.btn_ACTIVE_BG,
            activeforeground="white",
            relief="flat"
        )
        self.button_end_retry.pack(pady=5)

        self.button_end_menu = tk.Button(self.frame_middle)
        self.button_end_menu.config(
            text="RETURN TO MENU",
            font=font_button_large,
            width=15,
            bg="#FA5C5C", 
            fg="white",
            activebackground="#D94C4C", 
            activeforeground="white", 
            relief="flat"
        )
        self.button_end_menu.pack(pady=5)

        ## BUTTONS RIGHT
        self.frame_right = tk.Frame(self.frame_buttons, width=288, height=100)
        self.frame_right.pack_propagate(False)
        self.frame_right.config(
            bg=BG_COLOR,
        )
        self.frame_right.pack(side=tk.LEFT)

        self.button_end_lb = tk.Button(self.frame_right)
        self.button_end_lb.config(
            text="VIEW LEADERBOARD",
            font=font_normal,
            width=15,
            padx=5,
            pady=5,
            bg=self.btn_BG, 
            fg=self.btn_FG,
            activebackground=self.btn_ACTIVE_BG, 
            activeforeground="white", 
            relief="flat"
        )
        self.button_end_lb.pack(expand=True, pady=5)

        self.add_widget(self.frame_root, 0.5, 0.5, "center")

    def update_points(self):
        points = self.game.points_var.get()
        self.label_points.config(
            text = f"{points} POINTS"
        )