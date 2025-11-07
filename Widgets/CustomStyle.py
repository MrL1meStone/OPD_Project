import json
from tkinter import ttk

class CustomStyle(ttk.Style):
    def __init__(self, style_name="PyCharm"):
        super().__init__()

        def get_rgb(background):
            return [int(background[i:i + 2], 16) for i in range(1, 6, 2)]

        def get_fg(background):
            return 'white' if sum(get_rgb(background)) <= 256 * 3 / 2 else "black"

        with open('Styles.json') as file:
            styles = json.load(file)

        style=styles[style_name]
        font = style['font']
        #--- Основные поля ---#
        self.name=style_name
        self.all_styles=styles
        self.font = (font['name'], font['size'])
        self.header = (font['name'], font['size']+2)
        self.bg = style['bg']
        self.second_bg = style['second_bg']
        self.fg = get_fg(self.bg)
        self.second_fg = get_fg(self.second_bg)
        # --- Синтаксис и его подсветка ---#
        syntax = style['syntax']
        self.keyword_color = syntax['keywords']
        self.int = syntax['int']
        self.str = syntax['str']
        self.func = syntax['func']
        self.error = syntax['error']

        # --- Внешний вид виджетов ---#
        self.theme_use('clam')
        self.configure(style = '.', font=self.font, bg=self.bg, foreground=self.fg)
        self.configure(style = 'TLabel', background=self.bg, font=self.font)
        self.configure(style = 'TFrame', background=self.bg)
        self.configure(style = 'TCombobox', background=self.bg,
                       font=self.font,foreground=self.fg,)
        self.map(style='TButton',
                 background=[("active", self.second_bg), ("!disabled", self.bg)],
                 foreground=[("active", self.second_fg), ("!disabled", self.fg)])

        self.configure(style='Green.TButton', font=self.font)
        self.map(style='Green.TButton',
                  background=[("active", '#269b40'), ("!disabled", '#1c7f31')],
                  foreground=[("active", "white"), ("!disabled", "#a0a0a0")])
