#
# main.py
#
# Created by Mariano Arselan at 01-12-20
#

import render
import tkinter as tki
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
import numpy as np

root = tki.Tk()

def draw(ax, triangles, color='b', camera_az=0.0):
    ext = 2.0
    ax.plot([-ext, ext], [0, 0], [0, 0], '--', color='gray')
    ax.plot([0, 0], [-ext, ext], [0, 0], '--', color='gray')
    ax.plot([0, 0], [0, 0], [-ext, ext], '--', color='gray')
    dir1 = render.Vector3D(math.cos(camera_az), math.sin(camera_az), 0)
    dir2 = render.Vector3D(-math.sin(camera_az), math.cos(camera_az), 0)
    dir3 = render.Vector3D(0, 0, 1)
    dir1.draw(ax, color='r')
    dir2.draw(ax, color='g')
    dir3.draw(ax, color='b')
    for triangle in triangles:
        triangle.draw(ax, color=color, camera_az=camera_az)

def project(ax, triangles,color='b', camera_az=0.0, camera_elev=0.0):
    for triangle in triangles:
        triangle.project(ax, color=color, camera_az=camera_az, camera_elev=camera_elev)


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
plt2 = fig2.add_subplot(111, aspect=1.0)
c2.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)

camera_az = 0.0
camera_elev = 0.0

def on_elevation_changed(value):
    global camera_elev
    camera_elev = float(value)
    plt1.clear()
    plt2.clear()
    draw(plt1, [t1, t2, t3, t4, t5, t6, t7, t8], color='k')
    plt2.plot([-2, 2, 2, -2, -2], [-2, -2, 2, 2, -2], color='r')
    project(plt2, [t1, t2, t3, t4, t5, t6, t7, t8], color='k', camera_az=camera_az, camera_elev=camera_elev)
    canvas1.draw()
    c2.draw()

def on_azimuth_changed(value):
    global camera_az
    camera_az = float(value)
    plt1.clear()
    plt2.clear()
    draw(plt1, [t1, t2, t3, t4, t5, t6, t7, t8], color='k', camera_az=camera_az)
    plt2.plot([-2, 2, 2, -2, -2], [-2, -2, 2, 2, -2], color='r')
    project(plt2, [t1, t2, t3, t4, t5, t6, t7, t8], color='k', camera_az=camera_az, camera_elev=camera_elev)
    canvas1.draw()
    c2.draw()


azimuth = tki.Scale(top2, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL, command=on_azimuth_changed)
azimuth.pack(side=tki.BOTTOM)
elevation = tki.Scale(top2, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL, command=on_elevation_changed)
elevation.pack(side=tki.BOTTOM)

def on_closing():
    root.quit()
    root.destroy()

top1.protocol("WM_DELETE_WINDOW", on_closing)
top2.protocol("WM_DELETE_WINDOW", on_closing)
root.withdraw()


draw(plt1, [t1, t2, t3, t4, t5, t6, t7, t8], color='k')
plt2.plot([-5, 5, 5, -5, -5], [-5, -5, 5, 5, -5], color='r')
project(plt2, [t1, t2, t3, t4, t5, t6, t7, t8], color='k')

tki.mainloop()
