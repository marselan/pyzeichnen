#
# cube_scene.py
#
# Created by Mariano Arselan at 10-12-20
#


import render
import tkinter as tki
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import numpy as np

root = tki.Tk()

box_size = 4

camera_dist = 5.0

light = render.Vector3D(0.3, 0.5, 0.8)
frustum = render.Frustum(100, 100, camera_dist, -100.0)


def draw(ax, cubes, color='b', camera_az=0.0, camera_elev=0.0, camera_ang=0.0):
    ext = 2.0
    ax.plot([-ext, ext], [0, 0], [0, 0], '--', color='gray')
    ax.plot([0, 0], [-ext, ext], [0, 0], '--', color='gray')
    ax.plot([0, 0], [0, 0], [-ext, ext], '--', color='gray')
    dir1 = render.Vector3D(1, 0, 0)
    dir2 = render.Vector3D(0, 1, 0)
    dir3 = render.Vector3D(0, 0, 1)
    dir1.draw(plt1, color='r', camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
    dir2.draw(plt1, color='g', camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
    dir3.draw(plt1, color='b', camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
    a = dir1.add(dir2).add(dir3)
    a.draw(plt1, color='k', camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
    for cube in cubes:
        cube.draw(ax, color=color, camera_az=camera_az)

top1 = tki.Toplevel()
top1.title("Control Panel")
top1.wm_geometry("400x800+20+50")
fig1 = Figure(figsize=(10, 5), dpi=100)
canvas1 = FigureCanvasTkAgg(fig1, master=top1)

top2 = tki.Toplevel()
top2.title('Render')
top2.wm_geometry("800x800+1200+50")
fig2 = Figure(figsize=(10, 5), dpi=100)
c2 = FigureCanvasTkAgg(fig2, master=top2)
plt2 = fig2.add_subplot(111, aspect=1.0)
c2.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)

scene = render.Scene3D('sphere2.obj', plt2, frustum, light)
scene.parse_file()
scene.camera_distance = camera_dist


def on_distance_changed(value):
    global camera_dist
    camera_dist = float(value)
    plt2.clear()
    plt2.plot([-box_size, box_size, box_size, -box_size, -box_size],
              [-box_size, -box_size, box_size, box_size, -box_size], color='w')
    scene.set_camera_distance(camera_dist)
    c2.draw()


def on_angle_changed(value):
    camera_ang = float(value)
    plt2.clear()
    plt2.plot([-box_size, box_size, box_size, -box_size, -box_size],
              [-box_size, -box_size, box_size, box_size, -box_size], color='w')
    scene.set_angle(camera_ang)
    c2.draw()


def on_elevation_changed(value):
    camera_elev = float(value)
    plt2.clear()
    plt2.plot([-box_size, box_size, box_size, -box_size, -box_size],
              [-box_size, -box_size, box_size, box_size, -box_size], color='w')
    scene.set_elevation(camera_elev)
    scene.project()
    c2.draw()


def on_azimuth_changed(value):
    camera_az = float(value)
    plt2.clear()
    plt2.plot([-box_size, box_size, box_size, -box_size, -box_size],
              [-box_size, -box_size, box_size, box_size, -box_size], color='w')
    scene.set_azimuth(camera_az)
    c2.draw()


camera_label = tki.Label(top1, text="Camera")
camera_label.grid(row=0, column=0, columnspan=2)

az_label = tki.Label(top1, text="Azimuth")
az_label.grid(row=1, column=0, sticky=W)
azimuth = tki.Scale(top1, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL,
                    command=on_azimuth_changed)
azimuth.grid(row=1, column=1, sticky=W)

elev_label = tki.Label(top1, text="Elevation")
elev_label.grid(row=2, column=0, sticky=W)
elevation = tki.Scale(top1, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL,
                      command=on_elevation_changed)
elevation.grid(row=2, column=1, sticky=W)

ang_label = tki.Label(top1, text="Angle")
ang_label.grid(row=3, column=0, sticky=W)
angle = tki.Scale(top1, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL,
                  command=on_angle_changed)
angle.grid(row=3, column=1, sticky=W)

dist_label = tki.Label(top1, text="Distance")
dist_label.grid(row=4, column=0, sticky=W)
distance = tki.Scale(top1, from_=camera_dist, to=8.0, resolution=.01, length=300, orient=tki.HORIZONTAL,
                     command=on_distance_changed)
distance.grid(row=4, column=1, sticky=W)


def on_closing():
    root.quit()
    root.destroy()


top1.protocol("WM_DELETE_WINDOW", on_closing)
top2.protocol("WM_DELETE_WINDOW", on_closing)
root.withdraw()

plt2.plot([-box_size, box_size, box_size, -box_size, -box_size], [-box_size, -box_size, box_size, box_size, -box_size],
          color='w')
scene.project()

tki.mainloop()
