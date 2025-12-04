import json
from tkinter import ttk


class CustomStyle(ttk.Style):
    def __init__(self, style_name=None):
        super().__init__()

        def get_rgb(background):
            return [int(background[i:i + 2], 16) for i in range(1, 6, 2)]

        def get_fg(background):
            return 'white' if sum(get_rgb(background)) <= 256 * 3 / 2 else "black"

        with open('Widgets/Styles.json') as file:
            styles = json.load(file)

        if style_name is None:
            style_name = styles['selected']

        style = styles[style_name]
        font = style['font']
        # --- Основные поля ---#
        self.name = style_name
        self.all_styles = styles
        self.font = (font['name'], font['size'])
        self.header = (font['name'], font['size'] + 2)
        self.bg = style['bg']
        self.second_bg = style['second_bg']
        self.fg = get_fg(self.bg)
        self.second_fg = get_fg(self.second_bg)
        # --- Синтаксис и его подсветка ---#
        syntax = style['syntax']
        self.keyword = syntax['keywords']
        self.int = syntax['int']
        self.str = syntax['str']
        self.func = syntax['func']
        self.error = syntax['error']
        self.comment = syntax['comment']

        # --- Внешний вид виджетов ---#
        self.theme_use('clam')
        self.configure('.', font=self.font, bg=self.bg, foreground=self.fg)
        self.configure('TLabel', background=self.bg, font=self.font)
        self.configure('TFrame', background=self.bg)
        self.configure('Combobox', background=self.bg,
                       font=self.font, foreground=self.fg, )
        self.map('TButton',
                 background=[("active", self.second_bg), ("!disabled", self.bg)],
                 foreground=[("active", self.second_fg), ("!disabled", self.fg)])

        self.configure('Green.TButton', font=self.font)
        self.map(style='Green.TButton',
                 background=[("active", '#269b40'), ("!disabled", '#1c7f31')],
                 foreground=[("active", "white"), ("!disabled", "#a0a0a0")])
