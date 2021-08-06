from tkinter import Tk, Frame

from Progression import Progression
from Selection import Selection


class FrameContainer(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for i in (Selection, Progression):
            frame = i(parent=container, controller=self)
            self.frames[i.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.start_frame("Selection")

    def start_frame(self, page):
        self.frames[page].tkraise()