import json
from tkinter import *
from tkinter import ttk
from modules.randfuncs import randstr

from Questions.Easy import easy_questions
from modules.module_writer import make_module

# from modules.module_tests import check_output

QUESTIONS = [easy_questions]#,normal_questions,hard_questions

KEYWORDS=('False', 'class', 'from', 'or', 'None', 'continue', 'global', 'pass',
             'True', 'def', 'if', 'raise', 'and', 'del', 'import', 'return', 'as',
             'elif', 'in', 'try', 'assert', 'else', 'is', 'while', 'async', 'except',
             'lambda', 'with', 'await', 'finally', 'nonlocal', 'yield', 'break', 'for', 'not')


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
        self.all_styles=styles
        self.font = (font['name'], font['size'])
        self.header = (font['name'], font['size']+2)
        self.bg = style['bg']
        self.second_bg = style['second_bg']
        self.fg = get_fg(self.bg)
        self.second_fg = get_fg(self.second_bg)
        syntax = style['syntax']
        self.keyword_color = syntax['keywords']
        self.int = syntax['int']
        self.str = syntax['str']
        self.configure(style = '.', font=self.font, bg=self.bg, foreground=self.fg)
        self.configure(style = 'TLabel', background=self.bg, font=self.font)
        self.configure(style = 'TFrame', background=self.bg)
        self.configure(style = 'TCombobox', background=self.bg,
                       font=self.font,foreground=self.fg)
        self.map(style='TButton',
                 background=[("active", self.second_bg), ("!disabled", self.bg)],
                 foreground=[("active", self.second_fg), ("!disabled", self.fg)])

    def get(self, parameters: list[str] = None):
        return dict(zip(parameters, [self.__getattribute__(i) for i in parameters]))


class StylishText(Text):
    def __init__(self,widget,style,fg,height,width,text=None,disabled=True):
        super().__init__(widget,
        height = height, width = width, border = 0.0,
        bd = 0, highlightthickness = 0,
        bg = style.second_bg,
        font = style.font,
        foreground = fg)
        self.style=style
        if text:
            self.insert("1.0",text)
        if disabled:
            self.configure(state = 'disabled',exportselection=False)

    def color_text(self,row, index,word,color):
        tag_name = randstr()
        self.tag_add(tag_name, f'{row}.{index - len(word)}', f'{row}.{index}')
        self.tag_configure(tag_name, font=self.style.font, foreground=color)


class MainWindow(Tk):
    def __init__(self, size = None, style = 'PyCharm'):
        super().__init__()
        # Центрирование и название
        screen_weight, screen_height = self.wm_maxsize()
        if not size:
            size = (int(screen_weight//1.5), int(screen_height//1.7))
        self.size = size
        self.geometry(f"{size[0]}x{size[1]}"
                      f"+{(screen_weight - size[0]) // 2}"
                      f"+{(screen_height - size[1]) // 2}")
        self.title("Тест по знанию Python")

        # Визуал
        self.style = CustomStyle(style)
        self.configure(bg=self.style.bg)

        # Переменные
        self.current_question = IntVar(value=-1)  # от 0 до 9, -1 если не задан
        self.difficulty = IntVar(value=-1)  # от 0 до 2, -1 если не задан
        self.question_text = StringVar()

    def menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        def set_difficulty(difficulty):
            self.difficulty.set(difficulty)
            self.current_question.set(0)
            self.add_text()

        #Само меню
        ttk.Label(text='Выберите уровень сложности', font = self.style.header).pack(pady=(100, 70))
        for i,text in enumerate(['Легкий','Средний','Сложный']):
            ttk.Button(self, text=text, command=lambda x=i: set_difficulty(x), width=20).pack(pady=10)

        # Выбор темы
        ttk.Label(text='Или посмотрите темы',font = self.style.header).pack(pady=(100, 70))
        ttk.Button(text='Темы', width=20,command=self.styles).pack(pady=10)

    def add_text(self):
        for widget in self.winfo_children():
            widget.destroy()

        def indents(event):
            """ Автоматически создает отступы в
             соответвии с требованиями python """
            rows = ide.get('1.0', END)
            last_row = rows.split("\n")[-2]
            indent = "    " * last_row.count("    ")
            extra_indent = (":\n" == rows[-2:]) * "    "
            ide.insert(END, "\n" + extra_indent + indent)
            color_syntax(event)
            return "break"

        def check():
            """ Проверяет написанный код через stdin / stdout """
            make_module(ide.get('1.0', END))
            # is_right=check_output(question['args'],question['func'](question['args']))
            # ^-- хз потом допишу функцию, щас хочу делать само меню

        def move_question(step):
            """ Навигация по вопросам """
            current_question = self.current_question.get()
            if -1 < current_question + step < 10:
                self.current_question.set(current_question + step)

        def color_syntax(event):
            row, index = map(int, ide.index(INSERT).split('.'))
            word = ide.get(f'{row}.0', f'{row}.{index}').strip().split(" ")[-1]
            if word in KEYWORDS:
                ide.color_text(row,index,word,self.style.keyword_color)
            if len(word)>1 and word[-1]=="(":
                ide.color_text(row,index-1,word,self.style.int)
            if word.startswith("'") and word.endswith("'") or word.startswith('"') and word.endswith('"'):
                ide.color_text(row,index,word,self.style.str)
            try:
                print(word)
                for j in ("+","-","/","//","%","*","**","="):
                    for char in word.split(j):
                        int(char)
                        ide.color_text(row,index-len(word)+word.index(char),char,self.style.int)
            except ValueError:
                pass

        def disable_scroll(event):
            return "break"

        def on_key(event):
            # Получаем все строки
            text_lines = ide.get("1.0", "end-1c").split("\n")
            if len(text_lines) >= 16 and event.keysym not in ("BackSpace", "Delete", "Return"):
                current_index = ide.index(INSERT)
                line, col = map(int, current_index.split('.'))
                if line >= 16:
                    return "break"

        ttk.Button(text='< Меню', command=lambda: self.menu()).pack(pady=(100, 0), padx=(100, 0), anchor='w')

        main_frame = ttk.Frame(self)

        code_space = ttk.Frame(main_frame)

        error_frame=ttk.Frame(main_frame)
        ttk.Label(error_frame,text='Ошибки',font=self.style.header).pack(pady=40)
        errors = StylishText(error_frame,height=20, width=30,fg='red',style=self.style)
        errors.pack()
        ttk.Button(error_frame,text='Сдать').pack(pady=10)


        code_frame = ttk.Frame(code_space)
        numbers = StylishText(code_frame, height=20, width=3, style=self.style, fg = 'gray')
        numbers.pack(side='left',fill='y')
        numbers.configure(state='normal')
        for i in range(20):
            numbers.insert(END, f'{i + 1}\n')
        numbers.configure(state='disabled')

        self.question_text.set(QUESTIONS[self.difficulty.get()][self.current_question.get()]['text'])
        label = ttk.Label(code_space,textvariable=self.question_text, font = self.style.header)
        label.pack(pady=40)
        ide = StylishText(code_frame,height=15, width=70,
                          fg=self.style.fg,style=self.style, disabled=False)

        ide.bind("<Return>", indents)
        ide.bind("<KeyPress>", on_key)
        ide.bind("<space>", color_syntax)
        ide.bind("<KeyPress>", color_syntax, add=True)

        ide.bind("<Button-4>", disable_scroll)
        ide.bind("<Button-5>", disable_scroll)
        ide.bind("<MouseWheel>", disable_scroll)

        ide.bind("<Up>", disable_scroll)
        ide.bind("<Down>", disable_scroll)
        ide.bind("<Prior>", disable_scroll)
        ide.bind("<Next>", disable_scroll)

        ide.pack(anchor='center',side='left',fill="both")
        code_frame.pack()

        button_menu = ttk.Frame(code_space)
        button_menu.columnconfigure(3)
        check_button = ttk.Button(button_menu, text='Проверить', takefocus=False,
                                  command=check, width=15)

        next_question = ttk.Button(button_menu, text='Вперед >', takefocus=False,
                                   command=lambda: move_question(1), width=10)

        previous = ttk.Button(button_menu, text='< Назад', takefocus=False,
                              command=lambda: move_question(-1), width=10)

        previous.grid(row=0, column=0, pady=10,padx=10)
        check_button.grid(row=0, column=1, pady=10,padx=10)
        next_question.grid(row=0, column=2, pady=10,padx=10)
        button_menu.pack(ipady=10, ipadx=5, pady=0, padx=10, anchor='center')

        code_space.pack(side='left', fill='y', expand=True, padx=10)
        error_frame.pack(side='left', expand=True, padx=0,fill='y')
        main_frame.pack(anchor='center', expand=True)

    def styles(self):
        for widget in self.winfo_children():
            widget.destroy()

        def set_theme():
            theme = combo.curselection()[0]
            theme = combo.get(theme, theme)[0]

            for i in widgets_frame.winfo_children():
                i.destroy()

            self.style=CustomStyle(theme)
            self.styles()

        def preview_theme(event):
            for i in widgets_frame.winfo_children():
                i.destroy()

            theme = combo.curselection()[0]
            theme = combo.get(theme, theme)[0]
            style=CustomStyle(theme)
            self.configure(bg=style.bg)
            StylishText(widgets_frame, text=f'\n{'Пример текста': ^20}\n',
                        fg=style.fg, style=style,
                        height=3, width=20,disabled=True).pack(side='top', fill='x')
            bottom_frame = ttk.Frame(widgets_frame)
            ttk.Button(bottom_frame, text='Кнопка').pack(side='left')
            ttk.Label(bottom_frame, text='Текст').pack(side='left', padx=20)
            bottom_frame.pack(fill='x')

        ttk.Button(self,text='< Меню',
                   command=lambda: self.menu()
                   ).pack(pady=(100, 0), padx=(100, 0), anchor='w')

        main_frame = ttk.Frame(self)

        style_frame=ttk.Frame(main_frame)
        themes = tuple(self.style.all_styles.keys())
        variable = Variable(value=themes[:-1])
        combo=Listbox(style_frame,background=self.style.bg,font=self.style.font,
                      foreground=self.style.fg,listvariable=variable,
                      selectmode=SINGLE,height=len(themes)-1)
        combo.bind("<<ListboxSelect>>",preview_theme)
        combo.pack(pady=10)
        ttk.Button(style_frame,command=set_theme,text='Установить стиль',width=20).pack(pady=10)
        style_frame.pack(fill='y',side='left',padx=10)

        widgets_frame = ttk.Frame(main_frame)
        StylishText(widgets_frame, text=f'\n{'Пример текста': ^20}\n',
                    fg=self.style.fg, style=self.style,
                    height=3, width=20,disabled=True).pack(side='top', fill='x')
        bottom_frame = ttk.Frame(widgets_frame)
        ttk.Button(bottom_frame, text='Кнопка').pack(side='left')
        ttk.Label(bottom_frame, text='Текст').pack(side='left', padx=20)
        bottom_frame.pack(fill='x')
        widgets_frame.pack(side='left',fill='y', padx=10)

        main_frame.pack(anchor='center',expand=True)

def main():
    window = MainWindow()
    window.menu()
    window.mainloop()


if __name__ == "__main__":
    main()
