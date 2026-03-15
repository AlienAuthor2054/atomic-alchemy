from core.scene import Scene
from core.db import Database
from core.audio import AudioManager

from constants import WINDOW_X, WINDOW_Y
from style import *

import tkinter as tk
from tkinter.font import Font

from datetime import datetime

class Leaderboard(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.db = Database()
        self.data = self.db.get_lb()
        self.leaderboard = self.data["leaderboard"]

        self.frame_root = tk.Frame(self.canvas, width=WINDOW_X, height=WINDOW_Y)
        self.frame_root.config(
            bg=BG_COLOR_1,
        )
        self.frame_root.pack_propagate(False) 

        self.frame_lb = tk.Frame(self.frame_root)
        self.frame_lb.config(
            bg=BG_COLOR_1
        )
        self.frame_lb.pack(pady=20) 

        self.label_title = tk.Label(self.frame_lb)
        self.label_title.config(
            text="LEADERBOARD",
            font=font_medium,
            bg=BG_COLOR_1,
            fg=TEXT_TITLE
        )
        self.label_title.pack()

        ## PODIUM
        self.frame_podiums = tk.Frame(self.frame_lb)
        self.frame_podiums.config(
            bg=BG_COLOR_1,
        )
        self.frame_podiums.pack(fill='x', pady=10)

        first = self.leaderboard[0] if len(self.leaderboard) > 0 else None
        second = self.leaderboard[1] if len(self.leaderboard) > 1 else None
        third = self.leaderboard[2] if len(self.leaderboard) > 2 else None

        self.create_podium_spot(2, second)
        self.create_podium_spot(1, first)
        self.create_podium_spot(3, third)

        ## TOP 4-10
        self.frame_lists = tk.Frame(self.frame_lb)
        self.frame_lists.config(
            bg=BG_COLOR_2,
            bd=1,
            relief="solid"
        )
        self.frame_lists.pack(fill="both")

        for i in range(3, 10):
            data = self.leaderboard[i] if len(self.leaderboard) > i else None
            self.create_list_row(i + 1, data)
            
        self.add_widget(self.frame_root, 0.5, 0.5, "center")

        self.add_widget(self.frame_root, 0.5, 0.5, "center")

    def create_podium_spot(self, rank: int, data: dict = None):
        name = data["name"] if data and data.get("name") else "---"
        points = f"{data['points']} POINTS" if data else "---"
        timestamp_unix = data["timestamp"] if data else "---"
        timestamp = "---"

        if timestamp_unix != "---":
            timestamp = datetime.fromtimestamp(timestamp_unix).strftime('%Y-%m-%d %H:%M')

        frame = tk.Frame(self.frame_podiums)
        frame.config(
            bg=BG_COLOR_1,
        )
        frame.pack(fill="both", expand=True, side=tk.LEFT)

        frame_podium = tk.Frame(frame)
        frame_podium.config(
            bg=BG_COLOR_1,
        )
        frame_podium.pack(side=tk.BOTTOM)

        frame_labels = tk.Frame(frame_podium)
        frame_labels.config(
            bg=BG_COLOR_1,
        )
        frame_labels.pack()

        label_name = tk.Label(frame_labels)
        label_name.config(
            text=name,
            font=font_button_large,
            bg=BG_COLOR_1
        )
        label_name.pack()

        label_points = tk.Label(frame_labels)
        label_points.config(
            text=points,
            font=font_normal_normal,
            bg=BG_COLOR_1
        )
        label_points.pack()

        label_time = tk.Label(frame_labels)
        label_time.config(
            text=timestamp,
            font=font_normal_normal,
            bg=BG_COLOR_1
        )
        label_time.pack()

        block = tk.Frame(frame_podium)
        block.config(
            width=50,
            height=100,
            bg=TEXT_SUBTITLE,
        )
        block.pack()

        if rank == 1:
            block.config(
                height=100
            )
        elif rank == 2:
            block.config(
                height=75
            )
        elif rank == 3:
            block.config(
                height=50
            )
        else:
            block.config(
                height=100
            )

    def create_list_row(self, rank: int = 0, data: dict = None):
        name = data["name"] if data and data.get("name") else "---"
        points = f"{data['points']} POINTS" if data else "---"
        timestamp_unix = data["timestamp"] if data else "---"
        timestamp = "---"

        if timestamp_unix != "---":
            timestamp = datetime.fromtimestamp(timestamp_unix).strftime('%Y-%m-%d %H:%M')

        row = tk.Frame(self.frame_lists)
        row.config(
            bg=BG_COLOR_1, 
            pady=5
        )
        row.pack(fill="x")
        
        border = tk.Frame(self.frame_lists, bg="black")
        border.config(
            bg="black", 
            height=1
        )
        border.pack(fill="x")

        rank_lbl = tk.Label(row)
        rank_lbl.config(
            text=f"{rank}",
            font=font_normal,
            bg=BG_COLOR_1,
            fg=TEXT_NORMAL,
            width=4,
            anchor="w"
        )
        rank_lbl.pack(side="left")

        name_lbl = tk.Label(row)
        name_lbl.config(
            text=name,
            font=font_normal,
            bg=BG_COLOR_1,
            fg=TEXT_NORMAL,
            width=20,
            anchor="w"
        )
        name_lbl.pack(side="left", padx=10)

        score_lbl = tk.Label(row)
        score_lbl.config(
            text=points,
            font=font_normal,
            bg=BG_COLOR_1,
            fg=TEXT_NORMAL,
            width=10, 
            anchor="w"
        )
        score_lbl.pack(side="left", padx=10)

        dt_lbl = tk.Label(row)
        dt_lbl.config(
            text=timestamp,
            font=font_normal,
            bg=BG_COLOR_1,
            fg=TEXT_NORMAL,
            anchor="e"
        )
        dt_lbl.pack(side="right", padx=10)

    def load(self):
        super().load()

        AudioManager.play_bgm("assets/audio/song/song_leaderboard.ogg")

    def unload(self):
        AudioManager.stop_bgm()

        if self.canvas:
            self.canvas.destroy()