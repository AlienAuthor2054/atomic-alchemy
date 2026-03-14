from core.scene import Scene
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

        self.sfx = self.mixer.Sound(file="assets\\audio\sfx\sfx_game_opening.ogg")
        self.sfx.set_volume(0.3)

        self.sfx_length = int(self.sfx.get_length() * 1000) + 1000

        self.timeline = [
            (0, "The"),
            (850, "The Radi"),
            (1500, "The Radicals"),
        ]

        self.scheduled_events = []

        self.add_widget(self.frame_root, 0.5, 0.5, "center")

    def load(self):
        super().load()

        self.sfx.play()

        for delay_ms, text in self.timeline:
            event_id = self.root.after(delay_ms, lambda t=text: self.update_text(t))
            self.scheduled_events.append(event_id)

        end_event = self.root.after(self.sfx_length, self.on_finish)
        self.scheduled_events.append(end_event)

    def unload(self):
        super().unload()
        self.sfx.stop()

        for event_id in self.scheduled_events:
            self.root.after_cancel(event_id)
        self.scheduled_events.clear()

    def update_text(self, new_text: str):
        """Updates the label on the screen."""
        self.label_text.config(text=new_text)

    def on_finish(self):
        self.root.event_generate("<<OpeningSkip>>")