#
# render_2_windows.py
#
# Created by Mariano Arselan at 06-12-20
#

import tkinter as tki

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

root = tki.Tk()



t = np.arange(0, 3, .01)

top1 = tki.Toplevel()
top1.title("3D render")
top1.wm_geometry("800x600+200+50")
fig1 = Figure(figsize=(10,5), dpi=100)

canvas1 = FigureCanvasTkAgg(fig1, master=top1)
plt1 = fig1.add_subplot(111, projection="3d")
plt1.plot(t, 2 * np.sin(2 * np.pi * t))
canvas1.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)
canvas1.draw()


top2 = tki.Toplevel()
top2.title('Flat render')
top2.wm_geometry("800x600+1200+50")
fig2 = Figure(figsize=(10,5), dpi=100)
c2 = FigureCanvasTkAgg(fig2, master=top2)
plt2 = fig2.add_subplot(111)
plt2.plot(t, 2 * np.cos(2 * np.pi * t))
c2.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)
c2.draw()

def on_closing():
    root.quit()
    root.destroy()

top1.protocol("WM_DELETE_WINDOW", on_closing)
top2.protocol("WM_DELETE_WINDOW", on_closing)
root.withdraw()
tki.mainloop()