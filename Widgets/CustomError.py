from tkinter import Tk,ttk
from Widgets.StylishText import StylishText
from Widgets.CustomStyle import CustomStyle

class CustomError(Tk):
    def __init__(self,text,style):
        super().__init__()
        screen_weight, screen_height = self.wm_maxsize()
        size = (int(screen_weight // 1.4), int(screen_height // 2.3))
        self.geometry(f"{size[0]}x{size[1]}"
                      f"+{(screen_weight - size[0]) // 2}"
                      f"+{(screen_height - size[1]) // 2}")
        self.title("Ошибка!")
        self.resizable(width=False, height=False)
        self.configure(bg=style.bg)

        StylishText(self,style, height=15, width=100,
                    fg=style.error, bg=style.second_bg, disabled=True, text=text).pack(fill='both', expand=True,padx=10, pady=10)
        ttk.Button(self,text="Ок",
                   command=self.destroy, width=15, style='Custom.TButton').pack(pady=10)