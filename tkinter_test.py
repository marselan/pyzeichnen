#
# tkinter_test.py
#
# Created by Mariano Arselan at 13-02-21
#

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu


win = tk.Tk()
win.title("Python GUI")

# create a menu bar
def _quit():
    win.quit()
    win.destroy()
    exit()
    
menu_bar = Menu(win)
win.config(menu=menu_bar)

# create menu and add menu items
file_menu = Menu(menu_bar)
file_menu.add_command(label="New")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=_quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = Menu(menu_bar)
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=help_menu)


mighty = ttk.LabelFrame(win, text="Mighty Python")
mighty.grid(column=0, row=0, padx=8, pady=4)

a_label = ttk.Label(mighty, text="Enter a number:")
a_label.grid(column=0, row=0, sticky=tk.W)

def click_me():
    action.configure(text="Hello " + name.get() + " " + number.get())

name = tk.StringVar()
name_entered = ttk.Entry(mighty, width=12, textvariable=name)
name_entered.focus()
name_entered.grid(column=0, row=1, sticky=tk.W)

number = tk.StringVar()
number_chosen = ttk.Combobox(mighty, width=12, textvariable=number, state="readonly")
number_chosen['values'] = (1, 2, 4, 42, 100)
number_chosen.grid(column=1, row=0)
number_chosen.current(0)

action=ttk.Button(mighty, text="Click me!", command=click_me)
action.grid(column=1, row=1)
action.configure(state="enabled")

chVarDis = tk.IntVar()
chVarUn = tk.IntVar()
chVarEn = tk.IntVar()

check1 = tk.Checkbutton(mighty, text="Disabled", variable=chVarDis, state="disabled")
check1.select()
check1.grid(column=0, row=2, sticky=tk.W)

check2 = tk.Checkbutton(mighty, text="UnChecked", variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=2, sticky=tk.W)

check3 = tk.Checkbutton(mighty, text="Enabled", variable=chVarEn)
check3.select()
check3.grid(column=2, row=2, sticky=tk.W)

COLOR1 = "Blue"
COLOR2 = "Gold"
COLOR3 = "Red"

def radCall():
    radSel = radVar.get()
    if radSel == 1: win.configure(background=COLOR1)
    if radSel == 2: win.configure(background=COLOR2)
    if radSel == 3: win.configure(background=COLOR3)

radVar = tk.IntVar()

rad1 = tk.Radiobutton(mighty, text=COLOR1, variable=radVar, value=1, command=radCall)
rad2 = tk.Radiobutton(mighty, text=COLOR2, variable=radVar, value=2, command=radCall)
rad3 = tk.Radiobutton(mighty, text=COLOR3, variable=radVar, value=3, command=radCall)


rad1.grid(column=0, row=3)
rad2.grid(column=1, row=3)
rad3.grid(column=2, row=3)

scroll_w = 30
scroll_h = 3
scr = scrolledtext.ScrolledText(mighty, width=scroll_w, height=scroll_h, wrap=tk.WORD)
scr.grid(column=0, row=4, columnspan=3, sticky=tk.W + tk.E, padx=20, pady=20)

buttons_frame = ttk.LabelFrame(mighty, text='Labels in a Frame')
buttons_frame.grid(column=0, row=5, padx=20, pady=40)
ttk.Label(buttons_frame, text="Label 1 with a title much looooonger...").grid(column=0, row=0, sticky=tk.W)
ttk.Label(buttons_frame, text="Label 2").grid(column=0, row=1, sticky=tk.W)
ttk.Label(buttons_frame, text="Label 3").grid(column=0, row=2, sticky=tk.W)

for child in buttons_frame.winfo_children():
    child.grid_configure(padx=8, pady=4)

win.title("Mariano")
win.resizable(False, False)
win.mainloop()