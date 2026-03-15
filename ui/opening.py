from core.scene import Scene
from core.audio import AudioManager

from constants import WINDOW_X, WINDOW_Y

import tkinter as tk
from tkinter.font import Font

class Opening(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        BG_COLOR = "black"

        font_opening = Font(family="Comic Sans MS", size=24, weight="bold")

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

        self.label_text = tk.Label(self.frame_end)
        self.label_text.config(
            text="",
            font=font_opening,
            bg=BG_COLOR,
            fg="white"
        )
        self.label_text.pack()

        self.timeline = [
            (0, "The"),
            (850, "The Radi"),
            (1500, "The Radicals"),
        ]

        self.scheduled_events = []

        self.add_widget(self.frame_root, 0.5, 0.5, "center")

    def load(self):
        super().load()

        AudioManager.play_sfx("game_opening")

        for delay_ms, text in self.timeline:
            event_id = self.root.after(delay_ms, lambda t=text: self.update_text(t))
            self.scheduled_events.append(event_id)

        end_event = self.root.after(3000, self.on_finish)
        self.scheduled_events.append(end_event)

    def unload(self):
        super().unload()
        AudioManager.stop_sfx("game_opening")

        for event_id in self.scheduled_events:
            self.root.after_cancel(event_id)
        self.scheduled_events.clear()

    def update_text(self, new_text: str):
        self.label_text.config(text=new_text)

    def on_finish(self):
        self.root.event_generate("<<OpeningSkip>>")