import hashlib
import json
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASELINE_FILE = os.path.join(os.path.dirname(__file__), "baseline.json")
ALERTS_LOG    = os.path.join(os.path.dirname(__file__), "alerts_log.json")


# ── Hashing ──────────────────────────────────────────────────────────────────

def hash_file(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def shorten(hash_str):
    return hash_str[:10] + "..." if hash_str else "unknown"


# ── Baseline ─────────────────────────────────────────────────────────────────

def build_baseline(paths):
    baseline = {}
    for path in paths:
        p = Path(path)
        if p.is_file():
            h = hash_file(path)
            if h:
                baseline[path] = h
        elif p.is_dir():
            for file in p.rglob("*"):
                if file.is_file():
                    h = hash_file(str(file))
                    if h:
                        baseline[str(file)] = h
    save_baseline(baseline)
    print(f"Baseline captured: {len(baseline)} files")
    return baseline

def save_baseline(baseline):
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=2)

def load_baseline():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    return {}

def baseline_exists():
    return os.path.exists(BASELINE_FILE) and os.path.getsize(BASELINE_FILE) > 2


# ── Alerts log ───────────────────────────────────────────────────────────────

def save_alert(event_type, path, detail=""):
    import datetime
    alerts = load_alerts()
    alerts.insert(0, {   # insert at front instead of append
        "time":   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type":   event_type,
        "path":   path,
        "detail": detail
    })
    with open(ALERTS_LOG, "w") as f:
        json.dump(alerts, f, indent=2)

def load_alerts():
    if os.path.exists(ALERTS_LOG):
        with open(ALERTS_LOG, "r") as f:
            return json.load(f)
    return []


# ── Watchdog handler ─────────────────────────────────────────────────────────

class FIMEventHandler(FileSystemEventHandler):
    def __init__(self, callback, baseline):
        super().__init__()
        self.callback = callback
        self.baseline = baseline

    def on_created(self, event):
        if event.is_directory:
            return
        if "New Text Document" in event.src_path:
            return
        new_hash = hash_file(event.src_path)
        if new_hash:
            self.baseline[event.src_path] = new_hash
        save_alert("CREATED", event.src_path)
        self.callback("CREATED", event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        new_hash = hash_file(event.src_path)
        if new_hash is None:
            return
        old_hash = self.baseline.get(event.src_path)
        if old_hash == new_hash:
            return  # metadata touch, not a real change
        detail = f"{shorten(old_hash)} -> {shorten(new_hash)}"
        self.baseline[event.src_path] = new_hash
        save_alert("MODIFIED", event.src_path, detail)
        self.callback("MODIFIED", event.src_path, detail=detail)

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.baseline.pop(event.src_path, None)
        save_alert("DELETED", event.src_path)
        self.callback("DELETED", event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        old_hash = self.baseline.pop(event.src_path, None)
        new_hash = hash_file(event.dest_path)
        if new_hash:
            self.baseline[event.dest_path] = new_hash
        detail = f"{event.src_path} -> {event.dest_path}"
        save_alert("RENAMED", event.src_path, detail)
        self.callback("RENAMED", event.src_path, event.dest_path)


# ── Monitor class ─────────────────────────────────────────────────────────────

class monitor:
    def __init__(self):
        self.observers = []
        self.baseline  = {}

    def capture_baseline(self, paths):
        self.baseline = build_baseline(paths)
        return len(self.baseline)

    def start_monitoring(self, paths, callback):
        if not baseline_exists():
            callback("WARNING", "No baseline found. Capture a baseline first.")
            return False

        self.baseline = load_baseline()
        print(f"Baseline loaded: {len(self.baseline)} files")

        handler = FIMEventHandler(callback, self.baseline)
        for path in paths:
            observer = Observer()
            observer.schedule(handler, path, recursive=True)
            observer.start()
            self.observers.append(observer)

        print("Monitoring started.")
        return True

    def stop_monitoring(self):
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.observers.clear()
        print("Monitoring stopped.")