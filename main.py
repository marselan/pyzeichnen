#
# main.py
#
# Created by Mariano Arselan at 07-02-21
#

import render
import tkinter as tki
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import ttk
import numpy as np

root = tki.Tk()

box_size = 4

initial_camera_dist = 5.0
camera_dist = initial_camera_dist

azimuth = None
elevation = None
angle = None
distance = None
light_azimuth_var = None
light_elevation_var = None

top1 = tki.Toplevel()
top1.title("Control Panel")
top1.wm_geometry("400x800+20+50")
fig1 = Figure(figsize=(10, 5), dpi=100)
canvas1 = FigureCanvasTkAgg(fig1, master=top1)

top2 = tki.Toplevel()
top2.title('Render')
top2.wm_geometry("800x800+500+50")
fig2 = Figure(figsize=(10, 5), dpi=100)
c2 = FigureCanvasTkAgg(fig2, master=top2)
plt2 = fig2.add_subplot(111, aspect=1.0)
c2.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)

def createScene(file_name):
    light = render.Vector3D(1.0, 0.0, 0.0)
    frustum = render.Frustum(6, 6, camera_dist, -100.0, 80, 80, plt2, light)
    scene = render.Scene3D(file_name, plt2, frustum, light)
    scene.parse_file()
    scene.camera_distance = initial_camera_dist
    return scene

scene = createScene("sphere2.obj")

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
    c2.draw()


def on_azimuth_changed(value):
    camera_az = float(value)
    plt2.clear()
    plt2.plot([-box_size, box_size, box_size, -box_size, -box_size],
              [-box_size, -box_size, box_size, box_size, -box_size], color='w')
    scene.set_azimuth(camera_az)
    c2.draw()

def on_object_changed(event):
    global scene
    selection = event.widget.curselection()
    if selection[0] == 0:
        scene = createScene("sphere2.obj")
    elif selection[0] == 1:
        scene = createScene("box.obj")
    elif selection[0] == 2:
        scene = createScene("chair.obj")
    else:
        scene = createScene("cylinder.obj")

    azimuth.set(0)
    elevation.set(0)
    angle.set(0)
    distance.set(initial_camera_dist)
    light_azimuth_var.set(0)
    light_elevation_var.set(0)

    plt2.clear()
    plt2.plot([-box_size, box_size, box_size, -box_size, -box_size],
              [-box_size, -box_size, box_size, box_size, -box_size], color='w')
    scene.project_fast()
    c2.draw()

def on_light_azimuth_changed(value):
    scene.set_light(float(value), light_elevation_var.get())
    plt2.clear()
    plt2.plot([-box_size, box_size, box_size, -box_size, -box_size],
              [-box_size, -box_size, box_size, box_size, -box_size], color='w')
    scene.project_fast()
    c2.draw()

def on_light_elevation_changed(value):
    scene.set_light(light_azimuth_var.get(), float(value))
    plt2.clear()
    plt2.plot([-box_size, box_size, box_size, -box_size, -box_size],
              [-box_size, -box_size, box_size, box_size, -box_size], color='w')
    scene.project_fast()
    c2.draw()

def build_object_frame():
    object_label_frame = tki.LabelFrame(top1, text="  Object  ")
    object_label_frame.grid(row=0, column=0, columnspan=2)

    object_list = tki.Listbox(object_label_frame, height=10, width=20)
    object_list.insert(0, "Sphere")
    object_list.insert(1, "Box")
    object_list.insert(2, "Chair")
    object_list.insert(3, "Cylinder")
    object_list.select_set(0, 0)
    object_list.grid(row=0, column=0)
    object_list.bind("<<ListboxSelect>>", on_object_changed)

def build_camera_frame():
    global azimuth
    global elevation
    global angle
    global distance
    camera_label_frame = tki.LabelFrame(top1, text="  Camera  ")
    camera_label_frame.grid(row=1, column=0, columnspan=2)

    az_label = tki.Label(camera_label_frame, text="Azimuth")
    az_label.grid(row=0, column=0, sticky=W)
    azimuth = tki.Scale(camera_label_frame, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL,
                        command=on_azimuth_changed)
    azimuth.grid(row=0, column=1, sticky=E)

    elev_label = tki.Label(camera_label_frame, text="Elevation")
    elev_label.grid(row=1, column=0, sticky=W)
    elevation = tki.Scale(camera_label_frame, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL,
                          command=on_elevation_changed)
    elevation.grid(row=1, column=1, sticky=W)

    ang_label = tki.Label(camera_label_frame, text="Angle")
    ang_label.grid(row=2, column=0, sticky=W+S)
    angle = tki.Scale(camera_label_frame, from_=-np.pi, to=np.pi, resolution=.01, length=300, orient=tki.HORIZONTAL,
                      command=on_angle_changed)
    angle.grid(row=2, column=1, sticky=W)

    dist_label = tki.Label(camera_label_frame, text="Distance")
    dist_label.grid(row=3, column=0, sticky=W+S)
    distance = tki.Scale(camera_label_frame, from_=camera_dist, to=8.0, resolution=.01, length=300, orient=tki.HORIZONTAL,
                         command=on_distance_changed)
    distance.grid(row=3, column=1, sticky=W)

def build_light_frame():
    global light_azimuth_var
    global light_elevation_var
    light_label_frame = tki.LabelFrame(top1, text="  Light  ")
    light_label_frame.grid(row=2, column=0, columnspan=2, sticky=W+E)

    light_azimuth_label = tki.Label(light_label_frame, text="Azimuth")
    light_azimuth_label.grid(row=0, column=0, sticky=S)
    light_azimuth_var = tki.DoubleVar()
    light_azimuth_var.set(0)
    light_azimuth = tki.Scale(light_label_frame, from_=0, to=2*np.pi, resolution=.1, length=300, orient=tki.HORIZONTAL,
                         command=on_light_azimuth_changed, var=light_azimuth_var)
    light_azimuth.grid(row=0, column=1)

    light_elevation_label = tki.Label(light_label_frame, text="Elevation")
    light_elevation_label.grid(row=1, column=0, sticky=S)
    light_elevation_var = tki.DoubleVar()
    light_elevation_var.set(0)
    light_elevation = tki.Scale(light_label_frame, from_=-np.pi/2, to=np.pi/2, resolution=.1, length=300, orient=tki.HORIZONTAL,
                         command=on_light_elevation_changed, var=light_elevation_var)
    light_elevation.grid(row=1, column=1)


def on_closing():
    root.quit()
    root.destroy()

build_object_frame()
build_camera_frame()
build_light_frame()

top1.protocol("WM_DELETE_WINDOW", on_closing)
top2.protocol("WM_DELETE_WINDOW", on_closing)
root.withdraw()

plt2.plot([-box_size, box_size, box_size, -box_size, -box_size], [-box_size, -box_size, box_size, box_size, -box_size],
          color='w')
scene.project_fast()

tki.mainloop()
