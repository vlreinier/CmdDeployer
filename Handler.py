import tkinter
import Progression
import Selection


class FrameHandler(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = tkinter.Frame(self)
        container.grid(sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for i in (Selection.Selection, Progression.Progression):
            frame = i(parent=container, controller=self)
            self.frames[i.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def start_frame(self, page):
        self.frames[page].tkraise()
