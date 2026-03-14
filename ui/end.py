from constants import WINDOW_X, WINDOW_Y
from core.scene import Scene
from core.window import Window

import tkinter as tk
from tkinter import messagebox

class GameOver(Scene):
    def __init__(self, root, game):
        super().__init__(root)

        self.game = game
        self.points = None

        #  FONTS & COLORS (Sampled from gameplay screenshot)
        font_title = ("Courier", 70, "bold")
        font_points = ("Courier", 24, "bold")
        font_normal = ("Courier", 10, "bold")
        font_button_large = ("Courier", 16, "bold")

        BG_COLOR = "#FDF6E3"     
        TEXT_COLOR = "#333333"    
        TITLE_COLOR = "#FA5C5C"    
        POINTS_COLOR = "#909B4E"   
        self.btn_BG = "#3A8686"       
        self.btn_FG = "white"          
        self.btn_ACTIVE_BG = "#2B6666" 

        self.root_frame = tk.Frame(self.canvas, width=WINDOW_X, height=WINDOW_Y)
        self.window = tk.Frame(self.root_frame, width=WINDOW_X, height=WINDOW_Y)
        
        self.window.pack_propagate(False)
        self.window.pack(fill="both", expand=True)

        #  UI ELEMENTS: TOP SECTION (TITLE & SCORE) 
        self.lbl_title = tk.Label(self.window, text="GAME OVER", font=font_title, fg=TITLE_COLOR, bg=BG_COLOR)
        self.lbl_title.place(x=480, y=108, anchor="center")

        self.lbl_points = tk.Label(self.window, text=f"{self.points} POINTS", font=font_points, fg=POINTS_COLOR, bg=BG_COLOR)
        self.lbl_points.place(x=480, y=189, anchor="center")

        #  UI ELEMENTS: LEFT SECTION (NAME ENTRY) 
        self.lbl_enter_name = tk.Label(
            self.window, 
            text="ENTER YOUR NAME\nBELOW TO SEND\nYOUR SCORE TO\nTHE LEADERBOARD", 
            font=font_normal, fg=TEXT_COLOR, bg=BG_COLOR, justify="center"
        )
        self.lbl_enter_name.place(x=240, y=270, anchor="center")

        name_entry = tk.Entry(self.window, font=font_normal, justify="center", width=18, fg="#333333", bg="white", insertbackground="black")
        name_entry.place(x=240, y=334, anchor="center")

        self.btn_send = tk.Button(
            self.window, text="SEND", font=font_normal, bg=self.btn_BG, fg=self.btn_FG, 
            activebackground=self.btn_ACTIVE_BG, activeforeground="white", relief="flat", command=self.send_score, width=8
        )
        self.btn_send.place(x=240, y=378, anchor="center")

        #  UI ELEMENTS: CENTER SECTION (MAIN BUTTONS) 
        self.btn_try_again = tk.Button(
            self.window, text="TRY AGAIN", font=font_button_large, bg=self.btn_BG, fg=self.btn_FG,
            activebackground=self.btn_ACTIVE_BG, activeforeground="white", relief="flat", command=self.try_again, width=15, height=2
        )
        self.btn_try_again.place(x=480, y=334, anchor="center")

        # Made the quit button RED to match the red blocks and indicate an exit action
        self.btn_quit = tk.Button(
            self.window, text="MENU", font=font_button_large, bg="#FA5C5C", fg="white",
            activebackground="#D94C4C", activeforeground="white", relief="flat", command=self.back_to_menu, width=15, height=1
        )
        self.btn_quit.place(x=480, y=400, anchor="center")

        self.btn_credits = tk.Button(
            self.window, text="Credits", font=font_normal, bg=self.btn_BG, fg=self.btn_FG,
            activebackground=self.btn_ACTIVE_BG, activeforeground="white", relief="flat", command=self.show_credits, width=15, height=1
        )
        self.btn_credits.place(x=480, y=448, anchor="center")

        #  UI ELEMENTS: RIGHT SECTION (LEADERBOARD) 
        self.btn_view_leaderboard = tk.Button(
            self.window, text="VIEW LEADERBOARD", font=font_normal, bg=self.btn_BG, fg=self.btn_FG,
            activebackground=self.btn_ACTIVE_BG, activeforeground="white", relief="flat", command=self.view_leaderboard, width=18, height=1
        )
        self.btn_view_leaderboard.place(x=720, y=334, anchor="center")

        self.window.configure(bg=BG_COLOR)

        self.add_widget(self.root_frame, 0.5, 0.5, "center")
    
    def update_points(self):
        self.points = self.game.points_var.get()
        self.lbl_points.config(text=f"{self.points} POINTS")

    #  BUTTON FUNCTIONS 
    def send_score(self):
        pass

    def show_credits(self):
        messagebox.showinfo("Credits", "Game Developers:\n- Denison Matthew N. Sampang (rep)\n- Francis Andrei A. Diongco\n- Damian Rovic M. Lopez\n- Emmanuel Juri D. Estrella")

    def view_leaderboard(self):
        pass

    def try_again(self):
        self.root.event_generate("<<EndRetry>>")

    def back_to_menu(self):
        self.root.event_generate("<<EndMenu>>")
