import tkinter as tk
from tkinter import messagebox

WINDOW_X = 960
WINDOW_Y = 540

#  BUTTON FUNCTIONS 
def show_credits():
    messagebox.showinfo("Credits", "Game Developers:\n- Denison Matthew N. Sampang (rep)\n- Francis Andrei A. Diongco\n- Damian Rovic M. Lopez\n- Emmanuel Juri D. Estrella")

def view_leaderboard():
    pass

def try_again():
    pass

#  MAIN WINDOW SETUP 
root = tk.Tk()
root.title("Game Over Screen")
root.geometry(f"{WINDOW_X}x{WINDOW_Y}")
root.configure(bg="black")
root.resizable(False, False)

#  FONTS & COLORS 
font_title = ("Courier", 70, "bold")
font_points = ("Courier", 24, "bold")
font_normal = ("Courier", 10, "bold")
font_button_large = ("Courier", 16, "bold")

BG_COLOR = "black"
TEXT_COLOR = "white"
BTN_BG = "white"
BTN_FG = "black"
BTN_ACTIVE_BG = "#DDDDDD"

#  UI ELEMENTS: TOP SECTION (TITLE & SCORE) 
lbl_title = tk.Label(root, text="GAME OVER", font=font_title, fg=TEXT_COLOR, bg=BG_COLOR)
lbl_title.place(x=480, y=110, anchor="center")

lbl_points = tk.Label(root, text="0 POINTS !", font=font_points, fg=TEXT_COLOR, bg=BG_COLOR)
lbl_points.place(x=480, y=189, anchor="center")

#  UI ELEMENTS: CENTER SECTION (MAIN BUTTONS) 
btn_try_again = tk.Button(
    root, text="TRY AGAIN", font=font_button_large, bg=BTN_BG, fg=BTN_FG,
    activebackground=BTN_ACTIVE_BG, relief="flat", command=try_again, width=15, height=2
)
btn_try_again.place(x=480, y=320, anchor="center")

btn_view_leaderboard = tk.Button(
    root, text="VIEW LEADERBOARD", font=font_normal, bg=BTN_BG, fg=BTN_FG,
    activebackground=BTN_ACTIVE_BG, relief="flat", command=view_leaderboard, width=18, height=1
)
btn_view_leaderboard.place(x=480, y=390, anchor="center")

btn_credits = tk.Button(
    root, text="Credits", font=font_normal, bg=BTN_BG, fg=BTN_FG,
    activebackground=BTN_ACTIVE_BG, activeforeground="black", relief="flat", command=show_credits, width=18, height=1
)
btn_credits.place(x=480, y=440, anchor="center")

#  START MAIN LOOP 
root.mainloop()
