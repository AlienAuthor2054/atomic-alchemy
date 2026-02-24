import tkinter as tk
from tkinter.font import Font as TkFont
from random import randrange
from typing import NamedTuple

WINDOW_X = 640
WINDOW_Y = 360

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

# TODO: Use Canvas objects instead of widgets
class Atom():
    next_id = 1

    def __init__(self, canvas: tk.Canvas):
        center = Point(randrange(0, WINDOW_X), randrange(0, WINDOW_Y))
        radius = 36
        self.canvas = canvas
        self.id = Atom.next_id
        Atom.next_id += 1
        self.tag = "atom" + str(self.id)
        canvas.create_rectangle(
            center.x - radius, center.y - radius,
            center.x + radius, center.y + radius,
            fill="black",
            tags=self.tag,
        )
        label_font = TkFont(size=radius)
        canvas.create_text(
            center.x,
            center.y,
            text="H",
            font=label_font,
            fill="gray",
            tags=self.tag,
            state=tk.DISABLED,
        )
        #super().__init__(root, width=2, height=1, text="H", font=label_font, bg="white", fg="gray")
        self.dragging = False
        self.pos = Point(center.x - radius, center.y - radius)
        self.last_mouse_pos = Point(0, 0)
        canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_click)
        canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.on_release)
        canvas.tag_bind(self.tag, "<B1-Motion>", self.on_drag)

    def on_click(self, event):
        self.dragging = True
        self.last_mouse_pos = Point(event.x, event.y)
    
    def on_release(self, event):
        self.dragging = False
    
    def on_drag(self, event):
        if not self.dragging:
            return
        self.pos = Point(
            self.pos.x + (event.x - self.last_mouse_pos.x),
            self.pos.y + (event.y - self.last_mouse_pos.y)
        )
        self.canvas.moveto(
            self.tag, self.pos.x, self.pos.y
        )
        self.last_mouse_pos = Point(event.x, event.y)
        canvas.update()
    
    
root = tk.Tk(className="Crown Jewels Python")
#root.title("Crown Jewels Python")
root.geometry(f"{WINDOW_X}x{WINDOW_Y}")
root.resizable(width=False, height=False)

DEFAULT_FONT = TkFont(size=50)

canvas = tk.Canvas(root, width=WINDOW_X, height=WINDOW_Y)
canvas.pack()

button = tk.Button(root, text="Spawn Atom", command=lambda: Atom(canvas), font=DEFAULT_FONT)
button.place(x=100, y=50)

root.mainloop()
