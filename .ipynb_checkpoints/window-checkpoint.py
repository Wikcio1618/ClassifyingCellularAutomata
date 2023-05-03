from automaton import radius, nextGeneration

import sys
from tkinter import *
from tkinter import ttk
import numpy as np

# libs for figure display
import time
import asyncio



# Define the size of the canvas
WIDTH = 300
HEIGHT = 300

# Define the size of each cell
CELL_SIZE = 10

# Define the color for the cells
CELL_COLOR = "gold"

def initWindow():

	# Init window
	root = Tk()
	root.geometry("900x600") # Window size
	root.title("1D Cellular Automata")
	root.resizable(0, 0) # No full-screen

	# create top panel with widgets
	top_frame = Frame(root, height=100)
	top_frame.configure(bg="midnightblue")
	ttk.Style().configure('BarWik.TCheckbutton', background="midnightblue", foreground="gold")
	# create vaiables to store checkbutton states 		
	button_vars = [IntVar() for i in range(2**(2*automaton.radius+1))]
	for rule in button_vars:
		rule.set(IntVar(self.rule_book[0])) # TODO
	for i in range(2**(2*self.radius+1)-1, -1, -1):
		# checkbutton is initialized and connected with a variable
		button=ttk.Checkbutton(top_frame, style='BarWik.TCheckbutton', state='normal', variable=self.rule_book[i]) 
		button.grid(column=2**(2*self.radius+1)-i, row=0, padx=5,pady=(20,0))
	Button(top_frame, padx=10, pady=10, text="Run", command="").grid(column=8, row=0, pady=20, sticky=W) # to be changed for proper buttons
	top_frame.pack(fill=BOTH, expand=True)

	# create center panel with widgets
	center_frame = Frame(root, height=500)
	center_frame.configure(bg="blue")
	center_frame.pack(fill=BOTH, expand=True) 
	canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="blue")
	canvas.pack()

	root.mainloop() # display window


async def runEvolution(self):
	# TODO implement image update
	while(1):
		self.curr_disp[self.i,:]=self.evolution[self.i,:]
		self.im.set_data(self.curr_disp)
		self.canvas.draw()
		self.i+=1
		await asyncio.sleep(1)

# function to draw a cell at a given (x, y) position
def draw_cell(x, y):
    x1 = x * CELL_SIZE
    y1 = y * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=CELL_COLOR)