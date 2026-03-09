import os
import json
from tkinter import filedialog

PATHS_FILE = os.path.join(os.path.dirname(__file__), "paths.json")


class paths_handler:
    def __init__(self):
        self.paths = []
        self.load_paths()

    def add_file(self):
        path = filedialog.askopenfilename(title="Select a file")
        if path and path not in self.paths:
            self.paths.append(path)
            self.save_paths()
        return path

    def add_folder(self):
        path = filedialog.askdirectory(title="Select a folder")
        if path and path not in self.paths:
            self.paths.append(path)
            self.save_paths()
        return path

    def remove_path(self, path):
        clean = path.replace("📁  ", "").replace("📄  ", "")
        if clean in self.paths:
            self.paths.remove(clean)
            self.save_paths()

    def save_paths(self):
        with open(PATHS_FILE, "w") as f:
            json.dump(self.paths, f, indent=2)

    def load_paths(self):
        if os.path.exists(PATHS_FILE):
            with open(PATHS_FILE, "r") as f:
                self.paths = json.load(f)