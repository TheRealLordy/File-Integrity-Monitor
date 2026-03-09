import tkinter as tk
from dashboard import Dashboard
from paths import Paths
from settings import Settings
from paths_handler import paths_handler

window = tk.Tk()
shared_paths = paths_handler()
window.title("FIM")
window.geometry("800x500")

sidebar = tk.Frame(window, bg="#1a1d27", width=160)
sidebar.pack_propagate(False)
sidebar.pack(side="left", fill="y")

main = tk.Frame(window, bg="#0f1117")
main.pack(side="right", fill="both", expand=True)

page1 = Dashboard(main, shared_paths)
page2 = Paths(main, shared_paths)
page3 = Settings(main)

for page in (page1, page2, page3):
    page.place(relwidth=1, relheight=1)

def show_page(page):
    page.tkraise()

tk.Frame(sidebar, bg="#1a1d27").pack(fill="both", expand=True)

tk.Button(sidebar, text="Dashboard",
          bg="#2a2d3e", fg="white", relief="solid",
          highlightbackground="#4f8ef7", highlightthickness=1, borderwidth=0,
          command=lambda: show_page(page1)).pack(fill="x", padx=10, pady=5, ipady=8)

tk.Button(sidebar, text="Paths",
          bg="#2a2d3e", fg="white", relief="solid",
          highlightbackground="#4f8ef7", highlightthickness=1, borderwidth=0,
          command=lambda: show_page(page2)).pack(fill="x", padx=10, pady=5, ipady=8)

tk.Button(sidebar, text="Settings",
          bg="#2a2d3e", fg="white", relief="solid",
          highlightbackground="#4f8ef7", highlightthickness=1, borderwidth=0,
          command=lambda: show_page(page3)).pack(fill="x", padx=10, pady=5, ipady=8)

tk.Frame(sidebar, bg="#1a1d27").pack(fill="both", expand=True)

show_page(page1)
window.mainloop()