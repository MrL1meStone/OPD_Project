from tkinter import Canvas, PhotoImage
from Widgets.BaseWindow import BaseWindow


class InfoWindow(BaseWindow):
    def __init__(self, warning=False):
        super().__init__(0.2, 0.3)

        canvas = Canvas(self, bg=self.style.bg, height=100, width=100, borderwidth=0, highlightthickness=0)
        canvas.pack()

        if warning:
            image = PhotoImage(file="pics/warning.png")
        else:
            image = PhotoImage(file="pics/info.png")

        canvas.create_image(0, 0, image=image, anchor="nw")

