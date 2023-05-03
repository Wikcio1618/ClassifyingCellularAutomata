import automaton

import sys
from tkinter import *
from tkinter import ttk
import numpy as np

# libs for figure display
import time
import asyncio



# Define the size of the canvas
WIDTH = 500
HEIGHT = 500

# Define the size of each cell
CELL_SIZE = 10

# Define the number of cells in each direction
NUM_CELLS_X = WIDTH // CELL_SIZE # double slash works as floor division
NUM_CELLS_Y = HEIGHT // CELL_SIZE

# Define the color for the cells
CELL_COLOR = "gold"
NO_CELL_COLOR = "green"

# Define lead colors for windows
PRIMARY_COLOR = "gold"
BG_COLOR = "midnightblue"

def initWindow():

	# Init window
	root = Tk()
	root.geometry("900x600") # Window size
	root.title("1D Cellular Automata")
	root.resizable(0, 0) # No full-screen

	# create top panel with widgets
	top_frame = Frame(root, height=100)
	top_frame.configure(bg=BG_COLOR)
	ttk.Style().configure('BarWik.TCheckbutton', background=BG_COLOR, foreground=PRIMARY_COLOR)
	# create vaiables to store checkbutton states 		
	button_vars = [IntVar() for i in range(2**(2*automaton.radius+1))]
	for rule in button_vars:
		rule.set(IntVar(automaton.rule_book[0])) # TODO
	for i in range(2**(2*automaton.radius+1)-1, -1, -1):
		# checkbutton is initialized and connected with a variable
		button=ttk.Checkbutton(top_frame, style='BarWik.TCheckbutton', state='normal', variable=automaton.rule_book[i]) 
		button.grid(column=2**(2*automaton.radius+1)-i, row=0, padx=5,pady=(20,0))
	Button(top_frame, padx=10, pady=10, text="Run", command="").grid(column=8, row=0, pady=20, sticky=W) # to be changed for proper buttons
	top_frame.pack(fill=BOTH, expand=True)

	# create center panel with widgets
	center_frame = Frame(root, height=500)
	center_frame.configure(bg="red")
	canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="blue")
	canvas.pack(in_=center_frame)
	center_frame.pack(fill=BOTH, expand=True)

	root.mainloop() # display window


# async def runEvolution():
# 	# TODO implement image update
# 	while(1):
# 		self.curr_disp[self.i,:]=self.evolution[self.i,:]
# 		self.im.set_data(self.curr_disp)
# 		self.canvas.draw()
# 		self.i+=1
# 		await asyncio.sleep(1)

# function to draw a cell at a given (x, y) position
def drawCell(x, y, is_alive):
	x1 = x * CELL_SIZE
	y1 = y * CELL_SIZE
	x2 = x1 + CELL_SIZE
	y2 = y1 + CELL_SIZE
	if is_alive:
		canvas.create_rectangle(x1, y1, x2, y2, fill=CELL_COLOR)
	else:
		canvas.create_rectangle(x1, y1, x2, y2, fill=NO_CELL_COLOR)
		
def drawRow(generation: np.ndarray, row: int):
	for i in range(NUM_CELLS_X):
		drawCell(i, row, generation[i])
	
def runAnimation():
	pass