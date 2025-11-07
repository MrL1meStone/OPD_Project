import re

from tkinter import END, INSERT, TclError
from Widgets.StylishText import StylishText


def disable_scroll(event):
	return "break"


QUOTES = ("'", '"')

CLEANERS = ("BackSpace", "Delete", "Return")

BRACKET_EVENTS = ('<KeyPress-parenleft>',
                  '<KeyPress-bracketleft>',
                  '<KeyPress-braceleft>')

BRACKETS = ('(', ')', '[', ']', '{', '}')

KEYS = ("<Button-4>", "<Button-5>", "<MouseWheel>",
        "<Up>", "<Down>", "<Prior>", "<Next>")

OPERATIONS = ('+', '-', '/', '//', '%', '*',
                  '**', '=', '==', '!=', '>',
                  '<', '>=', '<=', '[', ']',
                  '{', '}', '(', ')', '"', "'",' ')

KEYWORDS = ('False', 'class', 'from', 'or',
            'None', 'continue', 'global',
            'pass', 'True', 'def', 'if',
            'raise', 'and', 'del', 'import',
            'return', 'as', 'elif', 'in',
            'try', 'assert', 'else', 'is',
            'while', 'async', 'except',
            'lambda', 'with', 'await',
            'finally', 'nonlocal',
            'yield', 'break', 'for', 'not')


class IDE(StylishText):
	def __init__(self, widget, style):
		super().__init__(widget, height=15,
		                 width=70, fg=style.fg,
		                 style=style, disabled=False)

		self.style = style

		self.bind("<Return>", self.indents)
		self.bind("<Tab>", self.move_right)
		self.bind("<KeyPress>", self.on_key)
		self.bind("<KeyPress-ISO_Left_Tab>", self.move_left)
		self.bind("<KeyPress-BackSpace>", self.delete_spaces)
		self.bind("<KeyPress-space>", self.color_keywords)
		self.bind("<KeyPress-quotedbl>", self.color_strings)
		self.bind("<KeyPress-apostrophe>", self.color_strings)
		self.bind("<KeyPress-parenleft>", self.color_funcs)
		self.bind("<KeyPress-quotedbl>", self.replace_quotes, add=True)
		self.bind("<KeyPress-apostrophe>", self.replace_quotes, add=True)
		self.bind("<KeyPress-quotedbl>", self.wrap_selected, add=True)
		self.bind("<KeyPress-apostrophe>", self.wrap_selected, add=True)
		self.bind("<KeyPress-period>", self.color_int, add=True)

		for i in range(10):
			self.bind(f'<KeyPress-{i}>', self.color_int, add=True)

		for i in BRACKET_EVENTS:
			self.bind(i, self.wrap_selected, add=True)
			self.bind(i, self.pair_brackets, add=True)

		for i in KEYS:
			self.bind(i, disable_scroll)

	def insert_index(self):
		return self.index(INSERT).split(".")

	def indents(self, event):
		""" Автоматически создает отступы в
		 соответвии с требованиями python """
		line = self.insert_index()[0]
		if int(line) >= 20:
			return "break"
		rows = self.get('1.0', END)
		last_row = rows.split("\n")[-2]
		indent = "    " * last_row.count("    ")
		extra_indent = (":\n" == rows[-2:]) * "    "
		self.insert(INSERT, "\n" + extra_indent + indent)
		return "break"

	def color_keywords(self, event):
		line, char = map(int, self.index("insert").split('.'))
		row = self.get(f'{line}.0', f'{line}.{char}').strip()
		word = row.split(" ")[-1]
		last_char = row.rfind(word)

		if word in KEYWORDS:
			self.color_index(f'{line}.{last_char}',INSERT,self.style.keyword_color)

	def on_key(self, event):
		line = self.insert_index()[0]
		if event.keysym not in CLEANERS and int(line) >= 21:
			return "break"
		return None

	def color_strings(self, event):
		try:
			self.index('sel.first')
			return None
		except TclError:
			self.insert(INSERT, event.char * 2)
			line, char = map(int, self.insert_index())
			row = self.get(f'{line}.0', INSERT)

			for quote in QUOTES:
				matches = [match.start() for match in re.finditer(quote, row)]
				if len(matches) % 2 == 0 and len(matches) >= 2:
					matches = matches[-2:]
					self.color_index(f'{line}.{matches[0]}', f'{line}.{matches[1] + 1}', self.style.str)
			self.mark_set(INSERT, f'{line}.{char-1}')
			return "break"

	def replace_quotes(self, event):
		try:
			sel_start = self.index("sel.first")
			sel_end = self.index("sel.last")

			selection = self.get(sel_start, sel_end)

			for i in (0, 1):
				if (selection.startswith(QUOTES[i]) and selection.endswith(QUOTES[i])
						and event.char == QUOTES[i - 1]):
					selection = selection[1:-1]
					self.replace(sel_start, sel_end, f"{QUOTES[i - 1]}{selection}{QUOTES[i - 1]}")
					self.color_index(float(sel_start) - 1.0, float(sel_end) + 1.0, self.style.str)
				elif i==1:
					self.wrap_selected(event)
		finally:
			return "break"

	def color_int(self, event):
		self.insert(INSERT, event.char)
		line, char = map(int, self.insert_index())
		row = self.get(f'{line}.0', END)
		self.color_index(f"{line}.{char-1}", f"{line}.{char}", self.style.int)
		for quote in QUOTES:
			matches = [match.start() for match in re.finditer(quote, row)]
			if len(matches) % 2 == 0 and len(matches) >= 2:
				matches = matches[-2:]
				self.color_index(f'{line}.{matches[0]}', f'{line}.{matches[1] + 1}', self.style.str)
		return "break"

	def color_funcs(self,event):
		line,char = self.insert_index()
		row = self.get(f'{line}.0', INSERT)
		func = row.strip().replace("def ","")
		indexes = [row.rfind(func.split(i)[-1]) for i in OPERATIONS]
		char = max(indexes)
		self.color_index(f'{line}.{char}',INSERT,self.style.func)

	def pair_brackets(self, event):
		self.insert(INSERT, event.char)
		line,char = self.insert_index()
		next_char = self.get(INSERT, f'{line}.{int(char) + 1}')

		if not next_char or next_char in OPERATIONS:
			for i in range(0, 6, 2):
				if BRACKETS[i] == event.char:
					self.insert(INSERT, BRACKETS[i + 1])
			self.mark_set(INSERT, f'{line}.{int(char)}')

		return "break"

	def move_right(self, event):
		try:
			sel_start = self.index("sel.first")
			sel_end = self.index("sel.last")

			start_line = int(sel_start.split('.')[0])
			end_line = int(sel_end.split('.')[0])
			for line in range(start_line, end_line + 1):
				self.insert(f"{line}.0", "    ")
		except TclError:
			self.insert(INSERT,"    ")

		return "break"

	def move_left(self, event):
		try:
			sel_start = self.index("sel.first")
			sel_end = self.index("sel.last")

			start_line = int(sel_start.split('.')[0])
			end_line = int(sel_end.split('.')[0])
			for line in range(start_line, end_line + 1):
				self.delete(f"{line}.0", f"{line}.4")
		finally:
			return "break"

	def delete_spaces(self,event):
		line,char = map(int, self.index("insert").split('.'))
		if char<4:
			return
		if self.get(f'{line}.{char-4}', f'{line}.{char}') == "    ":
			self.delete(f"{line}.{char-3}", f"{line}.{char}")

	def wrap_selected(self,event):
		try:
			sel_start = self.index("sel.first")
			sel_end = self.index("sel.last")
			selection = self.get(sel_start, sel_end)

			if event.char in QUOTES:
				self.replace(sel_start, sel_end, f"{event.char}{selection}{event.char}")
				self.color_index(sel_start, sel_end+0.2, self.style.str)
				return "break"

			for i in range(0,6,2):
				if event.char == BRACKETS[i]:
					self.insert(sel_start, event.char)
					self.insert(sel_end+0.2, BRACKETS[i + 1])
					return "break"

		except TclError as e:
			return None
		return "break"