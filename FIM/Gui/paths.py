import tkinter as tk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from paths_handler import paths_handler as PathsHandler


class Paths(tk.Frame):
    def __init__(self, parent, paths_handler):
        super().__init__(parent, bg="#0f1117")
        self.handler = paths_handler
        self.build()
        self.load_saved_paths()

    def build(self):
        # Title
        tk.Label(self, text="Monitored Paths", fg="white", bg="#0f1117",
                 font=("Courier New", 13, "bold")).pack(anchor="w", padx=20, pady=(20, 10))

        # Paths list frame
        list_frame = tk.Frame(self, bg="#1a1d27", highlightbackground="#2a2d3e",
                              highlightthickness=1)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        scrollbar = tk.Scrollbar(list_frame, bg="#1a1d27", troughcolor="#0f1117",
                                 relief="flat", bd=0)
        scrollbar.pack(side="right", fill="y")

        self.path_list = tk.Listbox(
            list_frame,
            bg="#1a1d27",
            fg="#c9d1d9",
            font=("Courier New", 10),
            selectbackground="#2a2d3e",
            selectforeground="#4f8ef7",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            activestyle="none"
        )
        self.path_list.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.config(command=self.path_list.yview)

        # Bottom bar
        bottom_bar = tk.Frame(self, bg="#0f1117")
        bottom_bar.pack(fill="x", padx=20, pady=(0, 20))

        tk.Button(
            bottom_bar,
            text="x Remove Selected",
            bg="#2a2d3e",
            fg="#f87171",
            font=("Courier New", 10),
            relief="flat",
            padx=14, pady=8,
            cursor="hand2",
            borderwidth=0,
            command=self.remove_path
        ).pack(side="left")

        tk.Button(
            bottom_bar,
            text="+ Add File",
            bg="#2a2d3e",
            fg="white",
            font=("Courier New", 10),
            relief="flat",
            padx=14, pady=8,
            cursor="hand2",
            borderwidth=0,
            command=self.add_file
        ).pack(side="right", padx=(6, 0))

        tk.Button(
            bottom_bar,
            text="+ Add Folder",
            bg="#4f8ef7",
            fg="white",
            font=("Courier New", 10),
            relief="flat",
            padx=14, pady=8,
            cursor="hand2",
            borderwidth=0,
            command=self.add_folder
        ).pack(side="right")

    def load_saved_paths(self):
        for path in self.handler.paths:
            icon = "📁  " if os.path.isdir(path) else "📄  "
            self.path_list.insert(tk.END, f"{icon}{path}")

    def add_folder(self):
        path = self.handler.add_folder()
        if path:
            self.path_list.insert(tk.END, f"📁  {path}")

    def add_file(self):
        path = self.handler.add_file()
        if path:
            self.path_list.insert(tk.END, f"📄  {path}")

    def remove_path(self):
        selected = self.path_list.curselection()
        if selected:
            display = self.path_list.get(selected[0])
            self.handler.remove_path(display)
            self.path_list.delete(selected[0])