#
# gui_tabbed.py
#
# Created by Mariano Arselan at 03-03-21
#

import tkinter as tk
from tkinter import ttk
win = tk.Tk()
win.title("Python GUI")
tab_control = ttk.Notebook(win)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Tab 1")
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Tab 2")
tab_control.pack(expand=1, fill="both")

mighty = ttk.LabelFrame(tab1, text="Might Python")
mighty.grid(column=0, row=0, padx=8, pady=8)

a_label = ttk.Label(mighty, text="Enter a name:")
a_label.grid(column=0, row=0, sticky="W")

name = tk.StringVar()
name_entered = ttk.Entry(mighty, width=12, textvariable=name)
name_entered.focus()
name_entered.grid(column=0, row=1, sticky="W")

def click_me():
    second_label.configure(text="Hello " + name.get() + " ")
    name.set("")
    name_entered.focus()

action=ttk.Button(mighty, text="Click me!", command=click_me)
action.grid(column=0, row=2, sticky="W")
action.configure(state="enabled")

second_label = ttk.Label(mighty)
second_label.grid(column=0, row=3, sticky="W")

# second Tab
mighty2 = ttk.LabelFrame(tab2, text="The Snake")
mighty2.grid(column=0, row=0, padx=8, pady=4)

chVarDis = tk.IntVar()
chVarUn = tk.IntVar()
chVarEn = tk.IntVar()

check1 = tk.Checkbutton(mighty2, text="Disabled", variable=chVarDis, state="disabled")
check1.select()
check1.grid(column=0, row=0, sticky="W", padx=5)

check2 = tk.Checkbutton(mighty2, text="UnChecked", variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=0, sticky="W", padx=5)

check3 = tk.Checkbutton(mighty2, text="Enabled", variable=chVarEn)
check3.select()
check3.grid(column=2, row=0, sticky="W", padx=5)

COLOR1 = "Blue"
COLOR2 = "Gold"
COLOR3 = "Red"

def radCall():
    radSel = radVar.get()
    if radSel == 1: mighty2.configure(text=COLOR1)
    if radSel == 2: mighty2.configure(text=COLOR2)
    if radSel == 3: mighty2.configure(text=COLOR3)

radVar = tk.IntVar()

rad1 = tk.Radiobutton(mighty2, text=COLOR1, variable=radVar, value=1, command=radCall)
rad2 = tk.Radiobutton(mighty2, text=COLOR2, variable=radVar, value=2, command=radCall)
rad3 = tk.Radiobutton(mighty2, text=COLOR3, variable=radVar, value=3, command=radCall)

rad1.grid(column=0, row=3, padx=5)
rad2.grid(column=1, row=3, padx=5)
rad3.grid(column=2, row=3, padx=5)

win.mainloop()