import tkinter
from write_log import *
from gui import Camera_GUI
from find_ip_camera import Find_ip_camera



class App:
    def __init__(self, parent, title, sources):

        self.parent = parent
        self.parent.iconbitmap(".camera_app/image/app.ico")
        self.parent.title(title)

        self.stream_widgets = []
        columns = 3
        for number, (text, source, camera) in enumerate(sources):
            widget = Camera_GUI(self.parent, text, source, camera)
            row = number // columns
            col = number % columns
            self.parent.columnconfigure(col, weight =1, uniform="a")
            self.parent.rowconfigure(row, weight =1, uniform="a")
            widget.grid(row=row, column=col, sticky=tkinter.NSEW)
            self.stream_widgets.append(widget)

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.parent.mainloop()
    
    def on_closing(self, event=None):

        print("[App] stoping threads")
        for widget in self.stream_widgets:
            # widget.vid.running = False
            widget.vid.release_function()

        print("[App] exit")
        self.parent.destroy()


if __name__ == "__main__":

    Find_ip_camera(App)