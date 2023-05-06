import automaton

from tkinter import Canvas
import time
from threading import Thread, Event
import numpy as np

class CustomCanvas(Canvas):
	def __init__(self, root, primary_col, bg_color):
		self.WIDTH = 500
		self.HEIGHT = 500

		# Define the size of each cell
		self.CELL_SIZE = 5

		# Define the number of cells in each direction
		self.NUM_CELLS_X = self.WIDTH // self.CELL_SIZE # double slash works as floor division
		self.NUM_CELLS_Y = self.HEIGHT // self.CELL_SIZE

		# Define the color for the cells
		self.CELL_COLOR = "gold"
		self.NO_CELL_COLOR = "midnightblue"
		
		super().__init__(root, width=self.WIDTH, height=self.HEIGHT, bg=bg_color, bd=1, scrollregion=(0, 0, np.inf, 0))
		# Define the size of the canvas
		
		self.currGen = np.random.randint(2, size=self.NUM_CELLS_X)
		self.rowToUpdate = 0
		self.canvasUpdating = False
		self.thread_running_event = Event()
		self.canvasThread = Thread(target=self.animateRows)
		self.canvasThread.start()
	
	# make the canvas being updated
	def start_update(self):
		self.thread_running_event.set()
	
	# stop the canvas from updating
	def stop_update(self):
		self.thread_running_event.clear()		
	
	# function to draw a cell at a given (x, y) position
	def drawCell(self, x, y, is_alive):
		x1 = x * self.CELL_SIZE
		y1 = y * self.CELL_SIZE
		x2 = x1 + self.CELL_SIZE
		y2 = y1 + self.CELL_SIZE
		if is_alive:
			self.create_rectangle(x1, y1, x2, y2, fill=self.CELL_COLOR, outline="")
		else:
			self.create_rectangle(x1, y1, x2, y2, fill=self.NO_CELL_COLOR, outline="")


	def updateRow(self):
		self.currGen = automaton.nextGen(self.NUM_CELLS_X, self.currGen)
		for x in range(self.NUM_CELLS_X):
			self.drawCell(x, self.rowToUpdate, self.currGen[x])
		if self.rowToUpdate > self.NUM_CELLS_Y:
			self.move("all", 0, -self.CELL_SIZE)
		self.update()

	def animateRows(self):
		while self.thread_running_event.is_set():
			self.updateRow()
			if self.rowToUpdate <= self.NUM_CELLS_Y:
				self.rowToUpdate += 1
			time.sleep(0.01)
