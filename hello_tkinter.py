#
# hello_tkinter.py
#
# Created by Mariano Arselan at 04-12-20
#

from tkinter import *


class HelloView(Frame):
    """A friendly little module"""

    def on_change(self):
        if self.name.get().strip():
            self.hello_string.set("Hello " + self.name.get())
        else:
            self.hello_string.set("Hello World")

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.name = StringVar()
        self.hello_string = StringVar()
        self.hello_string.set("Hello World")
        name_label = Label(self, text="Name:")
        name_entry = Entry(self, textvariable=self.name)
        ch_button = Button(self, text="Change", command=self.on_change)
        hello_label = Label(self, textvariable=self.hello_string, font=("TkDefaultFont", 64), wraplength=600)
        name_label.grid(row=0, column=0, sticky=W)
        name_entry.grid(row=0, column=1, sticky=(W + E))
        ch_button.grid(row=0, column=2, sticky=E)
        hello_label.grid(row=1, column=0, columnspan=3)
        self.columnconfigure(1, weight=1)

class MyApplication(Tk):
    """Hello World Main Application"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hello Tkinter")
        self.geometry("800x600")
        self.resizable(width=False, height=False)
        HelloView(self).grid(sticky=(E + W + N + S))
        self.columnconfigure(0, weight=1)

if __name__ == '__main__':
    app = MyApplication()
    app.mainloop()
