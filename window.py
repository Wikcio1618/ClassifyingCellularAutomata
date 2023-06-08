from automaton import Automaton
from canvas import CustomCanvas

from customtkinter import CTkSlider, CTkButton, BooleanVar, CTkSwitch, CTkCheckBox, CTkRadioButton
from tkinter import BOTH, DISABLED, E, NORMAL, W, Frame, IntVar, ttk, DoubleVar
import customtkinter as ctk
import numpy as np

# ________________________________________ CONSTANTS _______________________________________________

# Define lead colors for windows
PRIMARY_COLOR = "gold"
BG_COLOR = "midnightblue"

# _________________________________________ METHODS ________________________________________________

def initWindow():

	# Init window
	global root
	root = ctk.CTk()
	root.geometry("900x700") # Window size
	root.title("1D Cellular Automata")
	root.resizable(0, 0) # No full-screen
	root.protocol("WM_DELETE_WINDOW", on_close) # stop thread on close

	top_frame = Frame(root, bg=BG_COLOR, height=200)
	top_frame.pack(fill=BOTH)
	top_frame.columnconfigure(0, weight=2)
	top_frame.columnconfigure(1, weight=2)
	top_frame.columnconfigure(2, weight=1)

	# configure 3 Frames to contain widgets
	classical_frame=Frame(top_frame, bg=BG_COLOR, highlightbackground=PRIMARY_COLOR, highlightthickness=2)
	classical_frame.grid(column=0, row=0, sticky='WENS')

	non_class_frame=Frame(top_frame, bg=BG_COLOR, highlightbackground=PRIMARY_COLOR, highlightthickness=2)
	non_class_frame.grid(column=1, row=0, sticky='WENS')
	non_class_frame.columnconfigure(0)

	button_frame=Frame(top_frame, bg=BG_COLOR, highlightbackground=PRIMARY_COLOR, highlightthickness=2)
	button_frame.grid(column=2, row=0, sticky='WENS')
	button_frame.columnconfigure(0)


	# ------------------------------------------------------ BUTTON FRAME ---------------------------------------------------------

	# configure swith to choose mode
	swith_mode_var = BooleanVar(value=False)

	def swith_mode_event():
		if swith_mode_var.get():
			Automaton.radius=radio_var.get()
			slider_event(langton_slider.get())
			for box in checkbox_list:
				box.configure(state=DISABLED, border_color='grey')
			for label in checkbox_label_list:
				label.configure(foreground='grey')
			classical_label.configure(foreground='grey')

			langton_slider.configure(state=NORMAL, progress_color=PRIMARY_COLOR, button_color=PRIMARY_COLOR)
			slider_value_label.configure(foreground=PRIMARY_COLOR)
			radiobutton_1.configure(state=NORMAL, fg_color=PRIMARY_COLOR)
			radiobutton_2.configure(state=NORMAL, fg_color=PRIMARY_COLOR)
			slider_label.configure(foreground=PRIMARY_COLOR)
			radius_label.configure(foreground=PRIMARY_COLOR)

		else:
			Automaton.radius=1
			checkbox_event()
			for box in checkbox_list:
				box.configure(state=NORMAL, border_color=PRIMARY_COLOR)
			for label in checkbox_label_list:
				label.configure(foreground=PRIMARY_COLOR)
			classical_label.configure(foreground=PRIMARY_COLOR)

			langton_slider.configure(state=DISABLED, progress_color='grey', button_color='grey')
			slider_value_label.configure(foreground='grey')
			radiobutton_1.configure(state=DISABLED, fg_color='grey')
			radiobutton_2.configure(state=DISABLED, fg_color='grey')
			slider_label.configure(foreground='grey')
			radius_label.configure(foreground='grey')

		
	switch = CTkSwitch(master=button_frame, text="Switch mode", font=('Arial', 14), text_color=PRIMARY_COLOR, button_color=PRIMARY_COLOR
		    , progress_color="grey",fg_color="grey", hover=False
			, variable=swith_mode_var, onvalue=1, offvalue=0, command=swith_mode_event)
	switch.grid(column=0, row=0, pady=(15,25), padx=(10, 0))

	# configure run-stop button
	global start_stop_button
	start_stop_button = CTkButton(button_frame, width=80, height=50, corner_radius=10, font=("Arial", 14)
			       , text_color=BG_COLOR, fg_color=PRIMARY_COLOR, hover=False, text="Run", command=start_stop_thread)
	start_stop_button.grid(column=0, row=1, pady=(0, 10))

	# configure reset button
	CTkButton(
		button_frame, width=80, height=50, corner_radius=10, font=("Arial", 14)
			       , text_color=BG_COLOR, fg_color=PRIMARY_COLOR, hover=False, text="Reset", command=reset_canvas
				   ).grid(column=0, row=2, pady=(0,10))


	# -------------------------------------------------------  CLASSICAL FRAME ----------------------------------------------------------

	# checkboxes
	classical_label = ttk.Label(master=classical_frame, text="Pick a rule", font=('Arial', 14)
	    , foreground=PRIMARY_COLOR, background=BG_COLOR)
	classical_label.grid(column=0, row=0, columnspan=8, pady=(10, 5))
	checkbox_var_list = [IntVar(value=Automaton.rule_book[i]) for i in range (8)]

	def checkbox_event():
		Automaton.rule_book=[var.get() for var in checkbox_var_list]

	checkbox_list = []
	checkbox_label_list = []
	for i in range(8):
		checkbox_list.append(
			CTkCheckBox(master=classical_frame
	       , fg_color=BG_COLOR, hover=False, bg_color=BG_COLOR, checkmark_color=PRIMARY_COLOR, border_color=PRIMARY_COLOR, border_width=1
	       , checkbox_width=20, checkbox_height=20, width=20
		   , text=None, variable=checkbox_var_list[i], onvalue=1, offvalue=0, command=checkbox_event))
		checkbox_list[i].grid(row=1, column=i, padx=(8,0), pady=(15,15))
		checkbox_label_list.append(
			ttk.Label(master=classical_frame, text=f'{7-i:03b}'
	    , foreground=PRIMARY_COLOR, background=BG_COLOR, font=("Arial", 14))
		)
		checkbox_label_list[i].grid(row=2, column=i, padx=4)


	# ------------------------------------------ NON CLASSICAL FRAME -----------------------------------------------

	# Langton slider
	slider_label=ttk.Label(master=non_class_frame, text="Choose Langton factor to get a rule", font=('Arial', 14)
	   , foreground='grey', background=BG_COLOR)
	slider_label.grid(column=0, row=0, columnspan=2, pady=(10, 15))
	langton_val = DoubleVar(value=0.5)

	def slider_event(value):
		slider_value_label.configure(text=f'{value:.2f}')
		Automaton.rule_book=Automaton.getRuleByLangton(value)

	langton_slider = CTkSlider(master=non_class_frame, fg_color='grey', progress_color='grey', hover=False, button_color='grey'
			    , state=DISABLED, from_=0, to=1, variable=langton_val, command=slider_event)
	langton_slider.grid(column=0, row=1, padx=(20,0))
	slider_value_label = ttk.Label(master=non_class_frame, font=('Arial', 12), text=f"{langton_val.get():.2f}"
	   , foreground='grey', background=BG_COLOR)
	slider_value_label.grid(column=1, row=1, pady=(10, 5))

	# Radius radio buttons
	radius_label=ttk.Label(master=non_class_frame, text="Choose the radius", font=('Arial', 14)
	   , foreground='grey', background=BG_COLOR)
	radius_label.grid(column=0, row=2, columnspan=2, pady=(25,15))

	radio_var=IntVar(0)
	def radiobutton_event():
		Automaton.radius=radio_var.get()
		slider_event(langton_slider.get())

	radiobutton_1=CTkRadioButton(master=non_class_frame, hover_color='yellow', font=("Arial", 14)
			       , state=DISABLED ,text_color='grey', text_color_disabled='grey', fg_color='grey'
				   , variable=radio_var, value=2, text="2", command=radiobutton_event)
	radiobutton_2=CTkRadioButton(master=non_class_frame, hover_color='yellow', font=("Arial", 14)
			        , state=DISABLED ,text_color='grey', text_color_disabled='grey', fg_color='grey'
					, variable=radio_var, value=3, text="3", command=radiobutton_event)
	radiobutton_1.grid(column=0, row=3, pady=(0,5))
	radiobutton_2.grid(column=1, row=3, pady=(0,5))
	radiobutton_1.select()
	


		# create top panel with widgets
# 	ttk.Style().configure('BarWik.TCheckbutton', background=BG_COLOR, foreground=PRIMARY_COLOR)
# 	# create vaiables to store checkbutton states 		

# 	for rule in button_vars:
# 		rule.set(IntVar(automaton.rule_book[0])) # TODO
# 	for i in range(2**(2*automaton.radius+1)-1, -1, -1):
# 		# checkbutton is initialized and connected with a variable
# 		button=ttk.Checkbutton(top_frame, style='BarWik.TCheckbutton', state='normal', variable=automaton.rule_book[i]) 

# 	global start_stop_button
# 	start_stop_button = Button(top_frame, padx=10, pady=10, text="Run", command=start_stop_thread)
# 	start_stop_button.grid(column=8, row=0, pady=20, sticky=W) # to be changed for proper buttons
# 	top_frame.pack(fill=BOTH, expand=True)

	
	# create center panel with widgets
	center_frame = Frame(root, height=500)
	center_frame.configure(bg=BG_COLOR)
	center_frame.pack(fill=BOTH, expand=True)
	
	global canvas
	root.update()
	center_frame.update()
	canvas = CustomCanvas(center_frame, PRIMARY_COLOR, BG_COLOR, root.winfo_screenwidth(), center_frame.winfo_height())
	canvas.pack(in_=center_frame, side='top')

	root.mainloop() # display window

# -------------------------------------------------------------------------------------------------
	
def start_stop_thread():
	global start_stop_button
	global canvas
	
	if canvas.thread_running_event.is_set():
		canvas.stop_update()
		start_stop_button.configure(text='Run')
	else:
		changes_made=False
		canvas.start_update()
		start_stop_button.configure(text='Stop')
		canvas.animateRows()

def reset_canvas():
	canvas.reset()

	
def on_close():
	global canvas
	canvas.stop_update()
	global root
	root.destroy()