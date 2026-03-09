import tkinter as tk
# In progress...

class Settings(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f1117")
        self.build()

    def build(self):
        tk.Label(self, text="Settings", fg="white", bg="#0f1117").pack(pady=20)