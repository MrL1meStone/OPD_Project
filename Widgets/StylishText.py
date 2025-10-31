from tkinter import Text
from Testing.randfuncs import randstr


class StylishText(Text):
	def __init__(self, widget, style, height, width, text=None, disabled=True, selection=True,fg=None):
		if not fg:
			fg = style.fg

		super().__init__(widget, height=height, width=width, border=0.0,
		                 bd=0, highlightthickness=0, bg=style.second_bg,
		                 font=style.font, foreground=fg)

		self.style = style
		if text:
			self.insert("1.0", text)

		if disabled:
			self.configure(state='disabled', exportselection=False)

		if not selection:
			def disable_selection(event):
				self.tag_remove("sel", "1.0", "end")
				return "break"

			self.bind("<<Selection>>", disable_selection)
			self.bind("<ButtonRelease-1>", disable_selection)
			self.bind("<B1-Motion>", disable_selection)
			self.bind("<Shift-Left>", disable_selection)
			self.bind("<Shift-Right>", disable_selection)
			self.bind("<Control-a>", disable_selection)

	def color_text(self, row, index, word, color):
		tag_name = randstr()
		self.tag_add(tag_name, f'{row}.{index - len(word)}', f'{row}.{index}')
		self.tag_configure(tag_name, font=self.style.font, foreground=color)

	def color_index(self, index1, index2, color):
		tag_name = randstr()
		self.tag_add(tag_name, f'{index1}', f'{index2}')
		self.tag_configure(tag_name, font=self.style.font, foreground=color)
