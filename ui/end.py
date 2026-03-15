from __future__ import annotations
from typing import TYPE_CHECKING

from constants import WINDOW_X, WINDOW_Y

from core.scene import Scene
from core.db import Database
from core.audio import AudioManager

from style import *

import tkinter as tk
from tkinter.font import Font

from time import time

if TYPE_CHECKING:
    from core.game import Game

class GameOver(Scene):
    def __init__(self, root, game: Game):
        super().__init__(root)

        self.game = game
        self.db = Database()

        self.score_submitted = False

        self.entry_text = tk.StringVar()
        self.entry_text.trace("w", self.entry_validate)

        self.frame_root = tk.Frame(self.canvas, width=WINDOW_X, height=WINDOW_Y)
        self.frame_root.config(
            bg=BG_COLOR_1,
        )
        self.frame_root.pack_propagate(False) 

        self.frame_end = tk.Frame(self.frame_root)
        self.frame_end.config(
            bg=BG_COLOR_1,
        )
        self.frame_end.pack(expand=True)

        ## GAME OVER
        self.label_end_title = tk.Label(self.frame_end)
        self.label_end_title.config(
            text="GAME OVER",
            font=font_title,
            bg=BG_COLOR_1,
            fg=TEXT_TITLE,
        )
        self.label_end_title.pack()

        ## POINTS
        self.label_points = tk.Label(self.frame_end)
        self.label_points.config(
            text="0 POINTS",
            font=font_subtitle,
            bg=BG_COLOR_1,
            fg=TEXT_SUBTITLE,
        )
        self.label_points.pack(pady=(0, 20))

        ## BUTTONS
        self.frame_buttons = tk.Frame(self.frame_end)
        self.frame_buttons.pack()

        ## BUTTONS LEFT
        self.frame_left = tk.Frame(self.frame_buttons, width=288, height=100)
        self.frame_left.pack_propagate(False)
        self.frame_left.config(
            bg=BG_COLOR_1,
        )
        self.frame_left.pack(side=tk.LEFT)

        self.label_end_submit = tk.Label(self.frame_left)
        self.label_end_submit.config(
            text="ENTER YOUR NAME\nAND SUBMIT YOUR SCORE\nTO THE LEADERBOARD",
            font=font_normal,
            bg=BG_COLOR_1
        )
        self.label_end_submit.pack()

        self.entry_name = tk.Entry(self.frame_left)
        self.entry_name.config(
            font=font_normal, 
            justify="center", 
            width=24, 
            fg=TEXT_NORMAL, 
            bg="white", 
            insertbackground="black",
            textvariable=self.entry_text
        )
        self.entry_name.pack()

        self.button_end_submit = tk.Button(self.frame_left)
        self.button_end_submit.config(
            text="SUBMIT",
            font=font_normal,
            width=10,
            bg=BUTTON_BG,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_ACTIVE_BG, 
            activeforeground="white", 
            relief="flat",
            command=self.entry_submit
        )
        self.button_end_submit.pack()

        ## BUTTONS MIDDLE
        self.frame_middle = tk.Frame(self.frame_buttons, width=288, height=100)
        self.frame_middle.pack_propagate(False)
        self.frame_middle.config(
            bg=BG_COLOR_1,
        )
        self.frame_middle.pack(side=tk.LEFT)

        self.button_end_retry = tk.Button(self.frame_middle)
        self.button_end_retry.config(
            text="RETRY",
            font=font_button_large,
            width=15,
            bg=BUTTON_BG,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_ACTIVE_BG,
            activeforeground=BUTTON_TEXT,
            relief="flat",
            command=self.game_retry
        )
        self.button_end_retry.pack(pady=5)

        self.button_end_menu = tk.Button(self.frame_middle)
        self.button_end_menu.config(
            text="RETURN TO MENU",
            font=font_button_large,
            width=15,
            bg=BUTTON_BG_RED, 
            fg=BUTTON_TEXT,
            activebackground=BUTTON_ACTIVE_BG_RED, 
            activeforeground=BUTTON_TEXT, 
            relief="flat",
            command=self.return_to_menu
        )
        self.button_end_menu.pack(pady=5)

        ## BUTTONS RIGHT
        self.frame_right = tk.Frame(self.frame_buttons, width=288, height=100)
        self.frame_right.pack_propagate(False)
        self.frame_right.config(
            bg=BG_COLOR_1,
        )
        self.frame_right.pack(side=tk.LEFT)

        self.button_end_lb = tk.Button(self.frame_right)
        self.button_end_lb.config(
            text="VIEW LEADERBOARD",
            font=font_normal,
            width=15,
            padx=5,
            pady=5,
            bg=BUTTON_BG, 
            fg=BUTTON_TEXT,
            activebackground=BUTTON_ACTIVE_BG, 
            activeforeground="white", 
            relief="flat",
            command=self.view_leaderboard
        )
        self.button_end_lb.pack(expand=True, pady=5)

        self.add_widget(self.frame_root, 0.5, 0.5, "center")

    def game_retry(self):
        self.root.event_generate("<<EndRetry>>")

    def return_to_menu(self):
        self.root.event_generate("<<EndMenu>>")

    def entry_submit(self):
        if not self.score_submitted:
            self.score_submitted = True

            name = self.entry_name.get()
            points = self.game.points_var.get()
            timestamp = int(time())

            new_data = {
                "name": name,
                "points": points,
                "timestamp": timestamp,
            }

            data = self.db.get_lb()
            leaderboard = data["leaderboard"]

            leaderboard.append(new_data)
            leaderboard.sort(key=lambda x: x["points"], reverse=True)
            data["leaderboard"] = leaderboard[:10]

            self.db.set_lb(data)

            self.button_end_submit.config(
                text="SUBMITTED",
            )     
        else:
            print("Submitted")                                    

    def entry_validate(self, *args):
        value = self.entry_text.get()
        if len(value) > 20:
            self.entry_text.set(value[:20])

    def view_leaderboard(self, *args):
        self.root.event_generate("<<LeaderboardOpen>>")

    def update_points(self):
        points = self.game.points_var.get()
        self.label_points.config(
            text = f"{points} POINTS"
        )

    def unload(self):
        super().unload()

        AudioManager.stop_dynamic_bgm()

        

    