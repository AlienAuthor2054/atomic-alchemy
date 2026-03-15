from constants import WINDOW_X, WINDOW_Y

from core.scene import Scene
from core.window import Window
from core.db import Database
from core.audio import AudioManager

import tkinter as tk
from tkinter.font import Font

class Options(Window):
    def __init__(self, scene: Scene):
        super().__init__(scene)

        self.db = Database()

        h1 = Font(family="Comic Sans MS", size=20)
        h3 = Font(family="Comic Sans MS", size=10)

        ## OPTIONS

        self.value_vol_music = tk.IntVar()
        self.value_vol_sfx = tk.IntVar()

        options = self.db.get_options()
        
        volume_music = options.get("volume_music")
        volume_sfx = options.get("volume_sfx")

        self.value_vol_music.set(volume_music)
        self.value_vol_sfx.set(volume_sfx)

        self.frame_opt = self.window
        self.frame_opt.config(bd=1, relief="solid", width=500, height=250)

        self.frame_opt_title = tk.Frame(self.frame_opt)
        self.frame_opt_title.pack(fill = "both")

        self.label_opt_title = tk.Label(self.frame_opt_title, text="Options", font=h1)
        self.label_opt_title.pack(padx=5, pady=5, fill = "both")

        # MUSIC VOLUME

        self.frame_opt_volume_music = tk.Frame(self.frame_opt)
        self.frame_opt_volume_music.pack(fill="both", padx=5)

        self.frame_opt_volume_music_title = tk.Frame(self.frame_opt_volume_music)
        self.frame_opt_volume_music_title.pack(fill="both")

        self.label_opt_volume_music_title = tk.Label(self.frame_opt_volume_music_title, text="Music Volume")
        self.label_opt_volume_music_title.pack(side="left")

        self.frame_opt_volume_music_slider = tk.Frame(self.frame_opt_volume_music)
        self.frame_opt_volume_music_slider.pack(fill="x", expand=True, side="left")

        self.label_opt_volume_music = tk.Label(self.frame_opt_volume_music_slider, text="0")
        self.label_opt_volume_music.pack(side="left", padx=10)
        
        self.slider_opt_volume_music = tk.Scale(self.frame_opt_volume_music_slider, from_=0, to=100, orient="horizontal", showvalue=0, variable=self.value_vol_music)
        self.slider_opt_volume_music.pack(fill="x", expand=True, side="left")

        # SFX VOLUME

        self.frame_opt_volume_sfx = tk.Frame(self.frame_opt)
        self.frame_opt_volume_sfx.pack(fill="both", padx=5)

        self.frame_opt_volume_sfx_title = tk.Frame(self.frame_opt_volume_sfx)
        self.frame_opt_volume_sfx_title.pack(fill="both")

        self.label_opt_volume_sfx_title = tk.Label(self.frame_opt_volume_sfx_title, text="Sound Effects Volume")
        self.label_opt_volume_sfx_title.pack(side="left")

        self.frame_opt_volume_sfx_slider = tk.Frame(self.frame_opt_volume_sfx)
        self.frame_opt_volume_sfx_slider.pack(fill="x", expand=True, side="left")

        self.label_opt_volume_sfx = tk.Label(self.frame_opt_volume_sfx_slider, text="0")
        self.label_opt_volume_sfx.pack(side="left", padx=10)
        
        self.slider_opt_volume_sfx = tk.Scale(self.frame_opt_volume_sfx_slider, from_=0, to=100, orient="horizontal", showvalue=0, variable=self.value_vol_sfx)
        self.slider_opt_volume_sfx.pack(fill="x", expand=True, side="left")

        self.update_music_label()
        self.update_sfx_label()

        self.value_vol_music.trace_add("write", self.update_music_label)
        self.value_vol_sfx.trace_add("write", self.update_sfx_label)
    
    def open(self):
        super().open()

        options = self.db.get_options()

        volume_music = options.get("volume_music")
        volume_sfx = options.get("volume_sfx")

        self.slider_opt_volume_music.set(volume_music)
        self.slider_opt_volume_sfx.set(volume_sfx)

    def close(self, *args):
        super().close(*args)

        data = {
            "volume_music": self.value_vol_music.get(),
            "volume_sfx": self.value_vol_sfx.get()
        }

        self.db.set_options(data)
    
    def update_music_label(self, *args):
        current_volume = self.value_vol_music.get()
        self.label_opt_volume_music.config(text=str(current_volume))

        mixer_volume = current_volume / 100.0
        AudioManager.set_bgm_volume(mixer_volume)
        

    def update_sfx_label(self, *args):
        current_volume = self.value_vol_sfx.get()
        self.label_opt_volume_sfx.config(text=str(current_volume))

        mixer_volume = current_volume / 100.0
        AudioManager.set_sfx_volume(mixer_volume)