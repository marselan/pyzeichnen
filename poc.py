#
# poc.py
#
# Created by Mariano Arselan at 07-12-20
#

import render
import tkinter as tki
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import math
import numpy as np

root = tki.Tk()

def draw(ax, dir1, dir2, dir3, triangles, color='b'):
    ext = 2.0
    ax.plot([-ext, ext], [0, 0], [0, 0], '--', color='gray')
    ax.plot([0, 0], [-ext, ext], [0, 0], '--', color='gray')
    ax.plot([0, 0], [0, 0], [-ext, ext], '--', color='gray')
    dir1.draw(ax, color='r')
    dir2.draw(ax, color='g')
    dir3.draw(ax, color='b')
    for triangle in triangles:
        triangle.draw(ax, dir1, dir2, dir3, color=color)

def project(ax, dir1, dir2, dir3, triangles,color='b'):
    for triangle in triangles:
        triangle.project(ax, dir1, dir2, dir3, color=color)


p1 = render.Vector3D(1, 1, 0)
p2 = render.Vector3D(1, -1, 0)
p3 = render.Vector3D(0, 0, 1)
t1 = render.Triangle3D(p1, p2, p3)


p1 = render.Vector3D(1, 1, 0)
p2 = render.Vector3D(1, -1, 0)
p3 = render.Vector3D(0, 0, -1)
t2 = render.Triangle3D(p1, p2, p3)


p1 = render.Vector3D(-1, 1, 0)
p2 = render.Vector3D(-1, -1, 0)
p3 = render.Vector3D(0, 0, 1)
t3 = render.Triangle3D(p1, p2, p3)


p1 = render.Vector3D(-1, 1, 0)
p2 = render.Vector3D(-1, -1, 0)
p3 = render.Vector3D(0, 0, -1)
t4 = render.Triangle3D(p1, p2, p3)


p1 = render.Vector3D(1, -1, 0)
p2 = render.Vector3D(-1, -1, 0)
p3 = render.Vector3D(0, 0, 1)
t5 = render.Triangle3D(p1, p2, p3)


p1 = render.Vector3D(1, -1, 0)
p2 = render.Vector3D(-1, -1, 0)
p3 = render.Vector3D(0, 0, -1)
t6 = render.Triangle3D(p1, p2, p3)


p1 = render.Vector3D(1, 1, 0)
p2 = render.Vector3D(-1, 1, 0)
p3 = render.Vector3D(0, 0, 1)
t7 = render.Triangle3D(p1, p2, p3)


p1 = render.Vector3D(1, 1, 0)
p2 = render.Vector3D(-1, 1, 0)
p3 = render.Vector3D(0, 0, -1)
t8 = render.Triangle3D(p1, p2, p3)

dir1 = render.Vector3D(1, 0, 0)
dir3 = render.Vector3D(0, 0, 1)
dir2 = dir3.cross_prod(dir1)



top1 = tki.Toplevel()
top1.title("3D render")
top1.wm_geometry("800x600+200+50")
fig1 = Figure(figsize=(10,5), dpi=100)
canvas1 = FigureCanvasTkAgg(fig1, master=top1)
plt1 = fig1.add_subplot(111, projection="3d")
canvas1.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)

top2 = tki.Toplevel()
top2.title('Flat render')
top2.wm_geometry("800x600+1200+50")
fig2 = Figure(figsize=(10,5), dpi=100)
c2 = FigureCanvasTkAgg(fig2, master=top2)
plt2 = fig2.add_subplot(111)
c2.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)

def on_elevation_changed(value):
    print(value)
elevation = tki.Scale(top2, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL, command=on_elevation_changed)
elevation.pack(side=tki.BOTTOM)

def on_azimuth_changed(value):
    print(value)

azimuth = tki.Scale(top2, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL, command=on_azimuth_changed)
azimuth.pack(side=tki.BOTTOM)


def on_closing():
    root.quit()
    root.destroy()

top1.protocol("WM_DELETE_WINDOW", on_closing)
top2.protocol("WM_DELETE_WINDOW", on_closing)
root.withdraw()

draw(plt1, dir1, dir2, dir3, [t1, t2, t3, t4, t5, t6, t7, t8], color='k')
project(plt2, dir1, dir2, dir3, [t1, t2, t3, t4, t5, t6, t7, t8], color='k')

tki.mainloop()
