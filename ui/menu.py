from core.scene import Scene
from constants import WINDOW_X, WINDOW_Y

import tkinter as tk
from tkinter.font import Font

import csv

class Menu(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        h1 = Font(family="Comic Sans MS", size=20)
        h3 = Font(family="Comic Sans MS", size=10)

        self.frame_root = tk.Frame(self.canvas)

        self.frame_title = tk.Frame(self.frame_root)
        self.frame_title.pack()

        ## OPTIONS ##

        self.value_vol_music = tk.IntVar()
        self.value_vol_sfx = tk.IntVar()

        options = self.get_options()

        self.value_vol_music.set(options[0])
        self.value_vol_sfx.set(options[1])

        self.frame_opt = tk.Frame(self.canvas)
        self.frame_opt.config(bd=1, relief="solid", width=500, height=250)
        self.frame_opt.pack_propagate(False)

        self.frame_opt_title = tk.Frame(self.frame_opt)
        self.frame_opt_title.pack(fill = "both")

        self.label_opt_title = tk.Label(self.frame_opt_title, text="Options", font=h1)
        self.label_opt_title.pack(padx=5, pady=5, fill = "both")

        # MUSIC VOLUME

        self.frame_opt_volume_music = tk.Frame(self.frame_opt)
        self.frame_opt_volume_music.pack()

        self.frame_opt_volume_music_title = tk.Frame(self.frame_opt_volume_music)
        self.frame_opt_volume_music_title.pack(fill="both")

        self.label_opt_volume_music_title = tk.Label(self.frame_opt_volume_music_title, text="Music Volume")
        self.label_opt_volume_music_title.pack(side="left")

        self.frame_opt_volume_music_slider = tk.Frame(self.frame_opt_volume_music)
        self.frame_opt_volume_music_slider.pack()

        self.label_opt_volume_music = tk.Label(self.frame_opt_volume_music_slider, text="0")
        self.label_opt_volume_music.pack(side="left", padx=10)
        
        self.slider_opt_volume_music = tk.Scale(self.frame_opt_volume_music_slider, from_=0, to=100, orient="horizontal", showvalue=0, variable=self.value_vol_music)
        self.slider_opt_volume_music.pack(side="left")

        # SFX VOLUME

        self.frame_opt_volume_sfx = tk.Frame(self.frame_opt)
        self.frame_opt_volume_sfx.pack()

        self.frame_opt_volume_sfx_title = tk.Frame(self.frame_opt_volume_sfx)
        self.frame_opt_volume_sfx_title.pack(fill="both")

        self.label_opt_volume_sfx_title = tk.Label(self.frame_opt_volume_sfx_title, text="Sound Effects Volume")
        self.label_opt_volume_sfx_title.pack(side="left")

        self.frame_opt_volume_sfx_slider = tk.Frame(self.frame_opt_volume_sfx)
        self.frame_opt_volume_sfx_slider.pack()

        self.label_opt_volume_sfx = tk.Label(self.frame_opt_volume_sfx_slider, text="0")
        self.label_opt_volume_sfx.pack(side="left", padx=10)
        
        self.slider_opt_volume_sfx = tk.Scale(self.frame_opt_volume_sfx_slider, from_=0, to=100, orient="horizontal", showvalue=0, variable=self.value_vol_sfx)
        self.slider_opt_volume_sfx.pack(side="left")

        ## HOME SCREEN ##

        self.label_title = tk.Label(self.frame_title, text="Atomic Alchemy", font=h1,)
        self.label_title.pack()

        self.frame_button = tk.Frame(self.frame_root)
        self.frame_button.pack(pady=10)

        self.button_start = tk.Button(self.frame_button, text="Start", font=h3, width=10, command=lambda:self.start())
        self.button_start.pack(side=tk.LEFT, padx=5)

        self.button_opt = tk.Button(self.frame_button, text="Options", font=h3, width=10, command=lambda:self.opt_open())
        self.button_opt.pack(side=tk.LEFT, padx=5)

        self.button_exit = tk.Button(self.frame_button, text="Exit", font=h3, width=10, command=lambda:exit())
        self.button_exit.pack(side=tk.LEFT, padx=5)

        self.add_widget(self.frame_root, 0.5, 0.5, "center")

        self.id_opt = self.add_widget(self.frame_opt, 0.5, 0.5, "center")
        self.canvas.itemconfigure(self.id_opt, state='hidden')

        self.value_vol_music.trace_add("write", self.update_music_label)
        self.value_vol_sfx.trace_add("write", self.update_sfx_label)

    def start(self):
        self.root.event_generate("<<MenuStart>>")

    def opt_open(self):
        self.canvas.itemconfigure(self.id_opt, state='normal')
        self.canvas.bind("<ButtonPress-1>", self.opt_close)

        options = self.get_options()

        volume_music = options[0]
        volume_sfx = options[1]

        self.slider_opt_volume_music.set(volume_music)
        self.slider_opt_volume_sfx.set(volume_sfx)

    def opt_close(self, event):
        self.canvas.itemconfigure(self.id_opt, state='hidden')
        self.canvas.unbind("<ButtonPress-1>")

        with open(file="data\options.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.value_vol_music.get(), self.value_vol_sfx.get()])

    def get_options(self):
        # OPTIONS [VOLUME MUSIC, VOLUME SFX]

        try:
            with open(file="data\options.csv", mode="r") as file:
                reader = csv.reader(file)
                data = []
                for row in reader:
                    for column in row:
                        data.append(column)
                return data

        except FileNotFoundError as error:
            with open(file="data\options.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([50, 50])
            return self.get_options()
    
    def update_music_label(self, var_name, index, mode):
        current_volume = self.value_vol_music.get()
        self.label_opt_volume_music.config(text=str(current_volume))

    def update_sfx_label(self, var_name, index, mode):
        current_volume = self.value_vol_sfx.get()
        self.label_opt_volume_sfx.config(text=str(current_volume))