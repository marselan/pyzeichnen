#
# cube.py.py
#
# Created by Mariano Arselan at 10-12-20
#


import render
import tkinter as tki
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
import numpy as np

root = tki.Tk()

def draw(ax, cubes, color='b', camera_az=0.0):
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
    for cube in cubes:
        cube.draw(ax, color=color, camera_az=camera_az)

def project(ax, cubes,color='b', camera_az=0.0, camera_elev=0.0, camera_ang=0.0, camera_dist=1.0):
    for cube in cubes:
        cube.project(ax, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang, camera_dist=camera_dist)


p1 = render.Vector3D(1, 1, 1)
p2 = render.Vector3D(1, 1, -1)
p3 = render.Vector3D(-1, 1, -1)
p4 = render.Vector3D(-1, 1, 1)
s1 = render.Polygon3D([p1, p2, p3, p4])

p1 = render.Vector3D(-1, 1, 1)
p2 = render.Vector3D(-1, 1, -1)
p3 = render.Vector3D(-1, -1, -1)
p4 = render.Vector3D(-1, -1, 1)
s2 = render.Polygon3D([p1, p2, p3, p4])

p1 = render.Vector3D(1, -1, 1)
p2 = render.Vector3D(1, -1, -1)
p3 = render.Vector3D(-1, -1, -1)
p4 = render.Vector3D(-1, -1, 1)
s3 = render.Polygon3D([p1, p2, p3, p4])

p1 = render.Vector3D(1, 1, 1)
p2 = render.Vector3D(1, 1, -1)
p3 = render.Vector3D(1, -1, -1)
p4 = render.Vector3D(1, -1, 1)
s4 = render.Polygon3D([p1, p2, p3, p4])

p1 = render.Vector3D(1, 1, 1)
p2 = render.Vector3D(-1, 1, 1)
p3 = render.Vector3D(-1, -1, 1)
p4 = render.Vector3D(1, -1, 1)
s5 = render.Polygon3D([p1, p2, p3, p4])

p1 = render.Vector3D(1, 1, -1)
p2 = render.Vector3D(-1, 1, -1)
p3 = render.Vector3D(-1, -1, -1)
p4 = render.Vector3D(1, -1, -1)
s6 = render.Polygon3D([p1, p2, p3, p4])

top1 = tki.Toplevel()
top1.title("3D render")
top1.wm_geometry("800x800+200+50")
fig1 = Figure(figsize=(10,5), dpi=100)
canvas1 = FigureCanvasTkAgg(fig1, master=top1)
plt1 = fig1.add_subplot(111, projection="3d")
canvas1.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)

top2 = tki.Toplevel()
top2.title('Flat render')
top2.wm_geometry("800x800+1200+50")
fig2 = Figure(figsize=(10,5), dpi=100)
c2 = FigureCanvasTkAgg(fig2, master=top2)
plt2 = fig2.add_subplot(111, aspect=1.0)
c2.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)

camera_az = 0.0
camera_elev = 0.0
camera_ang = 0.0
camera_dist = 1.0

def on_distance_changed(value):
    global camera_dist
    camera_dist = float(value)
    plt1.clear()
    plt2.clear()
    draw(plt1, [], color='k')
    plt2.plot([-2, 2, 2, -2, -2], [-2, -2, 2, 2, -2], color='r')
    project(plt2, [s1, s2, s3, s4, s5, s6], color='k', camera_az=camera_az, camera_elev=camera_elev,
            camera_ang=camera_ang, camera_dist=camera_dist)
    canvas1.draw()
    c2.draw()

def on_angle_changed(value):
    global camera_ang
    camera_ang = float(value)
    plt1.clear()
    plt2.clear()
    draw(plt1, [], color='k')
    plt2.plot([-2, 2, 2, -2, -2], [-2, -2, 2, 2, -2], color='r')
    project(plt2, [s1, s2, s3, s4, s5, s6], color='k', camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang, camera_dist=camera_dist)
    canvas1.draw()
    c2.draw()

def on_elevation_changed(value):
    global camera_elev
    camera_elev = float(value)
    plt1.clear()
    plt2.clear()
    draw(plt1, [], color='k')
    plt2.plot([-2, 2, 2, -2, -2], [-2, -2, 2, 2, -2], color='r')
    project(plt2, [s1, s2, s3, s4, s5, s6], color='k', camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang, camera_dist=camera_dist)
    canvas1.draw()
    c2.draw()

def on_azimuth_changed(value):
    global camera_az
    camera_az = float(value)
    plt1.clear()
    plt2.clear()
    draw(plt1, [s1, s2, s3, s4, s5, s6], color='k', camera_az=camera_az)
    plt2.plot([-2, 2, 2, -2, -2], [-2, -2, 2, 2, -2], color='r')
    project(plt2, [s1, s1, s3, s4, s5, s6], color='k', camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang, camera_dist=camera_dist)
    canvas1.draw()
    c2.draw()


distance = tki.Scale(top2, from_=1.0, to=8.0, resolution=.01, length=300, orient=tki.HORIZONTAL, command=on_distance_changed)
distance.pack(side=tki.BOTTOM)
angle = tki.Scale(top2, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL, command=on_angle_changed)
angle.pack(side=tki.BOTTOM)
elevation = tki.Scale(top2, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL, command=on_elevation_changed)
elevation.pack(side=tki.BOTTOM)
azimuth = tki.Scale(top2, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL, command=on_azimuth_changed)
azimuth.pack(side=tki.BOTTOM)

def on_closing():
    root.quit()
    root.destroy()

top1.protocol("WM_DELETE_WINDOW", on_closing)
top2.protocol("WM_DELETE_WINDOW", on_closing)
root.withdraw()


draw(plt1, [s1, s2, s3, s4, s5, s6], color='k')
plt2.plot([-2, 2, 2, -2, -2], [-2, -2, 2, 2, -2], color='r')
project(plt2, [s1, s2, s3, s4, s5, s6], color='k')

tki.mainloop()
