#
# tkinter_test.py
#
# Created by Mariano Arselan at 13-02-21
#

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

win = tk.Tk()
a_label = ttk.Label(win, text="Enter a number:")
a_label.grid(column=0, row=0)

def click_me():
    action.configure(text="Hello " + name.get() + " " + number.get())

name = tk.StringVar()
name_entered = ttk.Entry(win, width=12, textvariable=name)
name_entered.focus()
name_entered.grid(column=0, row=1)

number = tk.StringVar()
number_chosen = ttk.Combobox(win, width=12, textvariable=number, state="readonly")
number_chosen['values'] = (1, 2, 4, 42, 100)
number_chosen.grid(column=1, row=0)
number_chosen.current(0)

action=ttk.Button(win, text="Click me!", command=click_me)
action.grid(column=1, row=1)
action.configure(state="enabled")

chVarDis = tk.IntVar()
chVarUn = tk.IntVar()
chVarEn = tk.IntVar()

check1 = tk.Checkbutton(win, text="Disabled", variable=chVarDis, state="disabled")
check1.select()
check1.grid(column=0, row=2, sticky=tk.W)

check2 = tk.Checkbutton(win, text="UnChecked", variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=2, sticky=tk.W)

check3 = tk.Checkbutton(win, text="Enabled", variable=chVarEn)
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

rad1 = tk.Radiobutton(win, text=COLOR1, variable=radVar, value=1, command=radCall)
rad2 = tk.Radiobutton(win, text=COLOR2, variable=radVar, value=2, command=radCall)
rad3 = tk.Radiobutton(win, text=COLOR3, variable=radVar, value=3, command=radCall)


rad1.grid(column=0, row=3)
rad2.grid(column=1, row=3)
rad3.grid(column=2, row=3)

scroll_w = 30
scroll_h = 3
scr = scrolledtext.ScrolledText(win, width=scroll_w, height=scroll_h, wrap=tk.WORD)
scr.grid(column=0, row=4, columnspan=3)

win.title("Mariano")
win.resizable(False, False)
win.mainloop()