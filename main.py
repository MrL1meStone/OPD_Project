import json

from tkinter import ttk
from tkinter import IntVar, StringVar, Variable
from tkinter import Tk, Listbox
from tkinter import END, SINGLE

from tkinter.colorchooser import askcolor

from Testing.module_tests import check_output
from Testing.module_writer import make_module
from Questions.Easy import *
from Questions.Normal import *
from Widgets.CustomStyle import CustomStyle
from Widgets.StylishText import StylishText
from Widgets.CustomError import CustomError
from Widgets.IDE import IDE


QUESTIONS = [easy_questions, normal_questions]#hard_questions


class MainWindow(Tk):
    def __init__(self, size = None):
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

        self.style = CustomStyle()
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

    # Менюшка с вопросами
    def add_text(self):
        for widget in self.winfo_children():
            widget.destroy()

        def check():
            """ Проверяет написанный код через stdin / stdout """
            make_module(ide.get('1.0', END))
            question = QUESTIONS[self.difficulty.get()][self.current_question.get()]
            right,error = check_output(input_func=question['args'], output_func=question['func'])
            if right:
                errors_tab.write_text(text="Все верно!",clear=True,color='green')
            if error:
                errors_tab.write_text(text=error,clear=True)
                CustomError(error,self.style)
    
        def move_question(step):
            """ Навигация по вопросам """
            current_question = self.current_question.get()
            if -1 < current_question + step < 11:
                self.current_question.set(current_question + step)

        # --- Весь фрейм включая вопрос, кнопку меню и результат тестов --- #
        
        main_frame = ttk.Frame(self)
        ttk.Button(main_frame,text='< Меню', command=self.menu
                   ).pack(pady=(100, 0), padx=(100, 0), anchor='w')

        questions_frame = ttk.Frame(main_frame)
        # --- Редактор кода вместе с кнопками --- #
        code_space = ttk.Frame(questions_frame)

        # --- Полоса нумерации строк --- #
        code_frame = ttk.Frame(code_space)
        numbers = StylishText(code_frame, height=20,
                              width=3, style=self.style,
                              fg = 'gray',selection=False)
        numbers.pack(side='left',fill='y')
        numbers.configure(state='normal')
        for i in range(19):
            numbers.insert(END, f'{i + 1: ^3}\n')
        numbers.insert(END, '20 ')
        numbers.configure(state='disabled')
        # --- Полоса нумерации строк --- #

        # --- Сам редактор кода --- #
        self.question_text.set(QUESTIONS[self.difficulty.get()][self.current_question.get()]['text'])
        label = ttk.Label(code_space,textvariable=self.question_text, font = self.style.header)
        label.pack(pady=40)
        ide = IDE(code_frame,style=self.style)
        ide.pack(anchor='center',side='left',fill="both")
        # --- Сам редактор кода --- #

        code_frame.pack()
        # --- Редактор кода вместе с кнопками --- #

        # --- Полоса кнопок для вопросов --- #
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
        # --- Полоса кнопок для вопросов --- #
        code_space.pack(side='left', fill='y', expand=True, padx=10)

        # --- Фрейм ошибок --- #
        error_frame = ttk.Frame(questions_frame)
        ttk.Label(error_frame, text='Ошибки', font=self.style.header).pack(pady=40)
        errors_tab = StylishText(error_frame, height=20, width=30, fg=self.style.error, style=self.style)
        errors_tab.pack()
        ttk.Button(error_frame, text='Сдать',style = 'Green.TButton',takefocus=False).pack(pady=10)
        error_frame.pack(side='left', expand=True, padx=0, fill='y')
        # --- Фрейм ошибок --- #

        questions_frame.pack(anchor='center')

        main_frame.pack(anchor='center',expand=True)
        # --- Весь фрейм включая вопрос, кнопку меню и результат тестов --- #

    def styles(self):
        for widget in self.winfo_children():
            widget.destroy()

        def menu_wrapper():
            with open('Styles.json', 'r', encoding='utf-8') as file:
                style_name = json.load(file)['selected']

            self.style = CustomStyle(style_name)
            self.configure(bg=self.style.bg)
            self.menu()

        def set_theme(event):
            theme = combo.get(*combo.curselection())
            if theme == self.style.name:
                return

            #--- Изменение текущей темы ---#
            with open('Styles.json',"r") as file:
                styles = json.load(file)
                styles['selected'] = theme

            with open('Styles.json', "w") as file:
                file.write(json.dumps(styles,indent=2))

            for i in widgets_frame.winfo_children():
                i.destroy()

            self.style=CustomStyle(theme)
            self.configure(bg=self.style.bg)
            self.styles()

        ttk.Button(self,text='< Меню',
                   command=menu_wrapper).pack(pady=(100, 0), padx=(100, 0), anchor='w')

        main_frame = ttk.Frame(self)
        # --- Выбор тем ---#
        style_frame=ttk.Frame(main_frame)
        themes = tuple(self.style.all_styles.keys())
        variable = Variable(value=themes[1:])
        combo=Listbox(style_frame,background=self.style.bg,font=self.style.font,
                      foreground=self.style.fg,listvariable=variable,
                      selectmode=SINGLE,height=min(4,len(themes)-1))

        combo.bind("<<ListboxSelect>>",set_theme)
        combo.pack(pady=10)
        style_frame.pack(fill='y',side='left',padx=10)
        # --- Выбор тем ---#

        # --- Превью темы ---#
        widgets_frame = ttk.Frame(main_frame)
        StylishText(widgets_frame, text=f'\n{'Пример текста': ^20}\n',
                    style=self.style,height=3, width=20,
                    disabled=True,selection=False).pack(side='top', fill='x')

        bottom_frame = ttk.Frame(widgets_frame)
        ttk.Button(bottom_frame, text='Кнопка').pack(side='left')
        ttk.Label(bottom_frame, text='Текст').pack(side='left', padx=20)
        bottom_frame.pack(fill='x')
        widgets_frame.pack(side='left',fill='y', padx=10)
        # --- Превью темы ---#

        main_frame.pack(anchor='center')

def main():
    window = MainWindow()
    window.menu()
    window.mainloop()


if __name__ == "__main__":
    main()