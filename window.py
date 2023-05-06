import automaton
from canvas import CustomCanvas

from tkinter import *
from tkinter import ttk
import numpy as np

# ________________________________________ CONSTANTS _______________________________________________

# Define lead colors for windows
PRIMARY_COLOR = "gold"
BG_COLOR = "midnightblue"

# _________________________________________ METHODS ________________________________________________

def initWindow():

	# Init window
	global root
	root = Tk()
	root.geometry("900x600") # Window size
	root.title("1D Cellular Automata")
	root.resizable(0, 0) # No full-screen
	root.protocol("WM_DELETE_WINDOW", on_close) # stop thread on close

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
	canvas = CustomCanvas(root, PRIMARY_COLOR, BG_COLOR)
	
	canvas.pack(in_=center_frame)
	center_frame.pack(fill=BOTH, expand=True)
	
	root.mainloop() # display window

	
def start_stop_thread():
	global start_stop_button
	global canvas
	
	if canvas.thread_running_event.is_set():
		canvas.stop_update()
		start_stop_button.config(text='Run')
	else:
		canvas.start_update()
		start_stop_button.config(text='Stop')
		canvas.animateRows()
		
	
def on_close():
	global canvas
	canvas.stop_update()
	global root
	root.destroy()