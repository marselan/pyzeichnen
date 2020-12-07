#
# render_example.py
#
# Created by Mariano Arselan at 03-12-20
#

import tkinter as tki

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

root = tki.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(15,10), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(121, projection="3d").plot(t, 2 * np.sin(2 * np.pi * t))
fig.add_subplot(122).plot(t, 2 * np.cos(2 * np.pi * t))


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)




tki.mainloop()