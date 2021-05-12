from tkinter import *

class RavenMinerGUISettingsWindow():
    def __init__(self, master):
        self.master = master
        self.window = ""
        return
        
    def open(self):
        if not self.window:
            self.window = Toplevel(self.master)
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
            label = Label(self.window, text="This is a window")
            label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

    def on_closing(self):
        self.window.destroy()
        self.window = ""
