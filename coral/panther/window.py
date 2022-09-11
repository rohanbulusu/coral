
import tkinter as tk


class Window(tk.Canvas):

	def __init__(self, width, height, background_color='#255255255'):
		super().__init__(width=width, height=height, bg=background_color)
		self.perpetuate = True
		self.create_rectangle(100, 100, 150, 150, fill='#255000000')
		self.pack(fill=tk.BOTH, expand=tk.TRUE)

	def run(self):
		while True:
			self.update_idletasks()
			self.update()


if __name__ == '__main__':

	w = Window(200, 200, background_color='#255000255')
	w.run()
	w.perpetuate = False

