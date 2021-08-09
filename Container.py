import tkinter
import Progression
import Selection


class FrameContainer(tkinter.Tk):
    
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for i in (Selection.Selection, Progression.Progression):
            frame = i(parent=container, controller=self)
            self.frames[i.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.start_frame("Selection")

    def start_frame(self, page):
        self.frames[page].tkraise()