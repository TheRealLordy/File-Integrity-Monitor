import tkinter as tk
import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from monitor import monitor, load_alerts, baseline_exists
from tkinter import messagebox

ALERT_COLORS = {
    "CREATED":  "#34d399",
    "MODIFIED": "#f0a500",
    "DELETED":  "#f87171",
    "RENAMED":  "#a78bfa",
    "WARNING":  "#facc15",
}

class Dashboard(tk.Frame):
    def __init__(self, parent, paths_handler):
        super().__init__(parent, bg="#0f1117")
        self.paths_handler = paths_handler
        self.monitor = monitor()
        self.monitoring = False
        self.build()
        self.load_previous_alerts()

    def build(self):
        # Top bar
        top_bar = tk.Frame(self, bg="#0f1117")
        top_bar.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(top_bar, text="Dashboard", fg="white", bg="#0f1117",
                 font=("Courier New", 13, "bold")).pack(side="left")

        self.monitor_btn = tk.Button(
            top_bar,
            text="START MONITORING",
            bg="#7171f8",
            fg="white",
            font=("Courier New", 11, "bold"),
            relief="flat",
            padx=20, pady=10,
            cursor="hand2",
            borderwidth=0,
            command=self.toggle_monitoring
        )
        self.monitor_btn.pack(side="right")

        self.capture_btn = tk.Button(
            top_bar,
            text="CAPTURE BASELINE",
            bg="#2a2d3e",
            fg="#34d399",
            font=("Courier New", 11, "bold"),
            relief="flat",
            padx=20, pady=10,
            cursor="hand2",
            borderwidth=0,
            command=self.capture_baseline
        )
        self.capture_btn.pack(side="right", padx=(0, 10))

        # Status label
        self.status_label = tk.Label(
            self, text="● No baseline captured",
            fg="#facc15", bg="#0f1117",
            font=("Courier New", 9)
        )
        self.status_label.pack(anchor="w", padx=20, pady=(0, 6))

        # Legend
        legend = tk.Frame(self, bg="#0f1117")
        legend.pack(fill="x", padx=20, pady=(0, 6))
        for label, color in ALERT_COLORS.items():
            tk.Label(legend, text=f"● {label}", fg=color, bg="#0f1117",
                     font=("Courier New", 9)).pack(side="left", padx=(0, 14))

        # Alerts header
        alerts_header = tk.Frame(self, bg="#0f1117")
        alerts_header.pack(fill="x", padx=20, pady=(0, 4))
        tk.Label(alerts_header, text="Alerts", fg="white", bg="#0f1117",
                 font=("Courier New", 11, "bold")).pack(side="left")
        tk.Button(alerts_header, text="Clear",
                  bg="#2a2d3e", fg="#f87171",
                  font=("Courier New", 9), relief="flat",
                  padx=10, pady=4, cursor="hand2", borderwidth=0,
                  command=self.clear_alerts).pack(side="right")

        # Alerts list
        alerts_container = tk.Frame(self, bg="#1a1d27",
                                    highlightbackground="#2a2d3e",
                                    highlightthickness=1)
        alerts_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar = tk.Scrollbar(alerts_container, bg="#1a1d27",
                                 troughcolor="#0f1117", relief="flat", bd=0)
        scrollbar.pack(side="right", fill="y")

        self.alerts_list = tk.Listbox(
            alerts_container,
            bg="#1a1d27",
            fg="#c9d1d9",
            font=("Courier New", 10),
            selectbackground="#2a2d3e",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            activestyle="none"
        )
        self.alerts_list.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.config(command=self.alerts_list.yview)

    def load_previous_alerts(self):
        alerts = load_alerts()
        # newest on top — reverse the list from disk
        for a in reversed(alerts):
            text = f"[{a['time']}]  {a['type']:<10}  {a['path']}"
            if a.get("detail"):
                text += f"  [{a['detail']}]"
            color = ALERT_COLORS.get(a["type"], "white")
            self.alerts_list.insert(0, text)
            self.alerts_list.itemconfig(0, fg=color)

        if alerts:
            self.status_label.config(
                text=f"● {len(alerts)} alerts loaded from history",
                fg="#c9d1d9"
            )

    def capture_baseline(self):
        if not self.paths_handler.paths:
            messagebox.showwarning("No Paths", "Add at least one path before capturing a baseline.")
            return
        count = self.monitor.capture_baseline(self.paths_handler.paths)
        self.status_label.config(
            text=f"● Baseline captured: {count} files — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            fg="#34d399"
        )

    def add_alert(self, event_type, path, new_path=None, detail=None):
        self.after(0, self._insert_alert, event_type, path, new_path, detail)

    def _insert_alert(self, event_type, path, new_path=None, detail=None):
        color = ALERT_COLORS.get(event_type, "white")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if new_path:
            text = f"[{timestamp}]  {event_type:<10}  {path}  ->  {new_path}"
        elif detail:
            text = f"[{timestamp}]  {event_type:<10}  {path}  [{detail}]"
        else:
            text = f"[{timestamp}]  {event_type:<10}  {path}"
        self.alerts_list.insert(0, text)
        self.alerts_list.itemconfig(0, fg=color)

        if event_type == "WARNING":
            self.status_label.config(text=f"● {path}", fg="#facc15")

    def clear_alerts(self):
        self.alerts_list.delete(0, tk.END)

    def toggle_monitoring(self):
        if self.monitoring:
            self.monitoring = False
            self.monitor.stop_monitoring()
            self.monitor_btn.config(text="START MONITORING", bg="#7171f8")
            self.status_label.config(text="● Monitoring stopped.", fg="#c9d1d9")
        else:
            if not self.paths_handler.paths:
                messagebox.showwarning("No Paths", "Add at least one path before starting monitoring.")
                return
            if not baseline_exists():
                messagebox.showwarning("No Baseline", "No baseline found. Capture a baseline first.")
                return
            started = self.monitor.start_monitoring(self.paths_handler.paths, self.add_alert)
            if started:
                self.monitoring = True
                self.monitor_btn.config(text="STOP MONITORING", bg="#f87171")
                self.status_label.config(text="● Monitoring active...", fg="#34d399")