import automaton

import sys
from tkinter import *
from tkinter import ttk
import numpy as np

# libs for figure display
import time
import asyncio
from threading import Thread, Event

# ________________________________________ CONSTANTS _______________________________________________

# Define the size of the canvas
WIDTH = 500
HEIGHT = 500

# Define the size of each cell
CELL_SIZE = 6

# Define the number of cells in each direction
NUM_CELLS_X = WIDTH // CELL_SIZE # double slash works as floor division
NUM_CELLS_Y = HEIGHT // CELL_SIZE

# Define the color for the cells
CELL_COLOR = "gold"
NO_CELL_COLOR = "midnightblue"

# Define lead colors for windows
PRIMARY_COLOR = "gold"
BG_COLOR = "midnightblue"

# __________________________________________ VARIABLES ________________________________________________


# _________________________________________ METHODS ________________________________________________

def initWindow():

	# Init window
	global root
	root = Tk()
	root.geometry("900x600") # Window size
	root.title("1D Cellular Automata")
	root.resizable(0, 0) # No full-screen
	root.protocol("WM_DELETE_WINDOW", on_close) # stop thread

	# create top panel with widgets
	top_frame = Frame(root, height=60)
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
	global start_stop_button
	start_stop_button = Button(top_frame, padx=10, pady=10, text="Run", command=start_stop_thread)
	start_stop_button.grid(column=8, row=0, pady=20, sticky=W) # to be changed for proper buttons
	top_frame.pack(fill=BOTH, expand=True)

	# create center panel with widgets
	center_frame = Frame(root, height=500)
	center_frame.configure(bg=BG_COLOR)
	
	global canvas
	canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, bd=1, confine=False)
	yscrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
	canvas.configure(yscrollcommand=yscrollbar.set)
	global currGen	
	currGen=np.random.randint(2, size=NUM_CELLS_X)
	global rowToUpdate
	rowToUpdate=0
	global canvasUpdating
	canvasUpdating=False
	canvasThread = Thread(target=animateRows)
	global thread_running_event
	thread_running_event = Event()
	canvasThread.start()
	
	canvas.pack(in_=center_frame, pady=10)
	center_frame.pack(fill=BOTH, expand=True)

	root.mainloop() # display window


# function to draw a cell at a given (x, y) position
def drawCell(x, y, is_alive):
	x1 = x * CELL_SIZE
	y1 = y * CELL_SIZE
	x2 = x1 + CELL_SIZE
	y2 = y1 + CELL_SIZE
	if is_alive:
		canvas.create_rectangle(x1, y1, x2, y2, fill=CELL_COLOR, outline="")
	else:
		canvas.create_rectangle(x1, y1, x2, y2, fill=NO_CELL_COLOR, outline="")
		

def updateRow():
	global currGen
	global canvas
	currGen = automaton.nextGen(NUM_CELLS_X, currGen)
	if rowToUpdate > NUM_CELLS_Y:
		canvas.yview_moveto(rowToUpdate-NUM_CELLS_Y)
	for x in range(NUM_CELLS_X):
		drawCell(x, rowToUpdate, currGen[x])

	canvas.update()
	
def animateRows():
	global thread_running_event
	while thread_running_event.is_set():
		updateRow()
		global rowToUpdate
		rowToUpdate+=1
		time.sleep(0.01)
	
	
def start_stop_thread():
	global start_stop_button
	global thread_running_event
	
	if thread_running_event.is_set():
		thread_running_event.clear()
		start_stop_button.config(text='Run')
	else:
		thread_running_event.set()
		start_stop_button.config(text='Stop')
		animateRows()
		
	
def on_close():
	global thread_running_event
	thread_running_event.clear()
	global root
	root.destroy()