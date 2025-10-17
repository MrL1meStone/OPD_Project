from tkinter import *
from tkinter import ttk
import re


class MainWindow(Tk):
	def __init__(self,size: tuple[int,int] = (800,600)):
		super().__init__()
		self.size = size
		screen_weight, screen_height = self.wm_maxsize()
		self.geometry(f"{size[0]}x{size[1]}"
		              f"+{(screen_weight-size[0])//2}"
		              f"+{(screen_height-size[1])//2}")
		self.title("Тест по знанию Python")
		self.configure(bg='#4387A8')

	def add_text(self):
		text=Text(self,height=15,width=70)
		text.pack(anchor='center',pady=10)
		text.config(font=('Calibre', 12))
		def check(event):
			rows=text.get('1.0', END)
			if ":\n" == rows[-2:] or re.match(r'\\n',rows):
				text.insert(END,"\n    ")

		text.bind("<Return>", check)
		button=ttk.Button(self,text='Проверить')
		button.pack()

def main():
	window=MainWindow()
	window.add_text()
	window.mainloop()

if __name__=="__main__":
	main()