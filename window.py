import automata

import sys
from tkinter import *
from tkinter import ttk
import numpy as np

# libs for figure display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import matplotlib as mpl
import time


class GUI():
	
	#FIELDS OF THIS CLASS
	#radius - What radius is set by user
	#rule_book - What rule is set by user
	#evolution - 2D array to be displayed as evolution
	
	def __init__(self):
		# Set initial rules
		self.radius = 1
		self.rule_book = [0 for _ in range (2**(2*self.radius+1))] # start with 90?
		self.evolution = automata.getEvolution(self.radius, self.rule_book)
		
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
		button_vars = [IntVar() for i in range(2**(2*self.radius+1))]
		for rule in button_vars:
			rule.set(IntVar(self.rule_book[0])) # TODO
		for i in range(2**(2*self.radius+1)-1, -1, -1):
			# checkbutton is initialized and connected with a variable
			button=ttk.Checkbutton(top_frame, style='BarWik.TCheckbutton', state='normal', variable=self.rule_book[i]) 
			button.grid(column=2**(2*self.radius+1)-i, row=0, padx=5,pady=(20,0))
		Button(top_frame, padx=10, pady=10, text="sth", command=self.runEvolution).grid(column=8, row=0, pady=20, sticky=W) # to be changed for proper buttons
		top_frame.pack(fill=BOTH, expand=True)

		# create center panel with widgets
		center_frame = Frame(root, height=500)
		center_frame.configure(bg="blue")
		fig = plt.figure(figsize=(5,5), facecolor='red')
		ax=plt.axes()
		# ax.set_axis_off()
		cmap = (mpl.colors.ListedColormap(['midnightblue', 'gold']))
		bounds = [0, 1]
		norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
		self.im = ax.imshow(np.ones((100,100)), cmap=cmap, vmax=1)
		self.canvas = FigureCanvasTkAgg(fig, master=center_frame)  
		self.canvas.get_tk_widget().pack() # put plot on the screen
		center_frame.pack(fill=BOTH, expand=True) 

		root.mainloop() # display window


	def runEvolution(self):
		print(self.rule_book)
		# TODO implement image update
		self.canvas.draw()
